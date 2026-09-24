#!/usr/bin/env bash
# Real GitLab Runner E2E for the Darkmoon scan component.
#
# Uses `gitlab-runner exec shell` (serverless single-job run) on a flattened
# copy of the component job, so the EXACT job body a user would get runs on a
# real runner. Findings come from a genuine Darkmoon engine report (replayed via
# the contract-faithful darkmoon-ci double). Asserts:
#   - the job emits gl-code-quality-report.json + gl-sast-report.json
#   - both validate against the LIVE GitLab schemas
#   - blocking mode: the job exits non-zero on the findings gate
#   - non-blocking mode: same gate exit code, tolerated via allow_failure:exit_codes
set -u

REPO=/home/mehdi/darkmoon-gitlab
VENDOR=$REPO/test/vendor
RUNNER=$VENDOR/gitlab-runner
FIXTURE=$REPO/test/fixtures/darkmoon-report-gitlab.md
WORK=$(mktemp -d /tmp/dm-runner-XXXXXX)
export PATH="$VENDOR:$PATH"
export DARKMOON_CI_REPLAY="$FIXTURE"
# Fake secrets so the run proves nothing is echoed (real license not needed for replay).
export DARKMOON_LICENSE_KEY="dm_live_TESTKEY_should_never_appear_in_logs"

pass=0; fail=0
ok(){ echo "  PASS: $1"; pass=$((pass+1)); }
ko(){ echo "  FAIL: $1"; fail=$((fail+1)); }

echo "== workspace: $WORK =="
cd "$WORK" || exit 1
git init -q; git config user.email t@t; git config user.name t; git config commit.gpgsign false

run_case(){
  local label=$1 afec=$2 expect_rc_nonzero=$3
  echo; echo "== CASE: $label (allow_failure_exit_codes=$afec) =="
  python3 "$REPO/test/render_flat.py" .gitlab-ci.yml \
    "target=http://juice-shop.local:8091" "fail-on=high" "mode=oss" \
    "allow_failure_exit_codes=$afec" >/dev/null
  git add -A; git commit -q -m "$label" >/dev/null
  # run the real runner; capture combined output + rc
  set +e
  "$RUNNER" exec shell \
    --env "PATH=$VENDOR:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
    --env "DARKMOON_CI_REPLAY=$DARKMOON_CI_REPLAY" \
    --env "DARKMOON_LICENSE_KEY=$DARKMOON_LICENSE_KEY" \
    darkmoon_scan >"$WORK/$label.log" 2>&1
  local rc=$?
  set -e
  echo "  runner exit code: $rc"
  # locate the build dir the runner used
  local bdir
  bdir=$(find "$WORK/builds" -maxdepth 3 -name gl-code-quality-report.json 2>/dev/null | head -1)
  bdir=$(dirname "$bdir" 2>/dev/null)
  if [ -n "$bdir" ] && [ -f "$bdir/gl-code-quality-report.json" ]; then
    ok "$label: emitted gl-code-quality-report.json"
  else
    ko "$label: no code-quality report found"; sed -n '1,40p' "$WORK/$label.log"; return
  fi
  [ -f "$bdir/gl-sast-report.json" ] && ok "$label: emitted gl-sast-report.json" || ko "$label: no SAST report"
  if python3 "$REPO/test/validate_schemas.py" "$bdir/gl-code-quality-report.json" "$bdir/gl-sast-report.json"; then
    ok "$label: both reports validate against LIVE schemas"
  else
    ko "$label: schema validation failed"
  fi
  # exit-code semantics: the job script exits 4 on the gate in BOTH cases
  if grep -q "darkmoon-ci exit code: 4" "$WORK/$label.log"; then
    ok "$label: findings gate produced exit code 4"
  else
    ko "$label: expected gate exit code 4 in job output"
  fi
  if [ "$expect_rc_nonzero" = yes ]; then
    [ "$rc" -ne 0 ] && ok "$label: runner reports FAILURE (blocking)" || ko "$label: expected non-zero runner rc"
  fi
  # secret hygiene: the license key must never appear in the job log
  if grep -q "TESTKEY_should_never_appear" "$WORK/$label.log"; then
    ko "$label: SECRET LEAKED into job log"
  else
    ok "$label: no secret leaked into job log"
  fi
  # threat model: full report/native JSON must be ABSENT by default (expose-full-report=false)
  if [ -f "$bdir/darkmoon/darkmoon-findings.json" ]; then
    ko "$label: native findings JSON exposed despite expose-full-report=false"
  else
    ok "$label: full report withheld by default (§4)"
  fi
}

# Blocking (default): gate code 4 not tolerated -> runner fails
run_case blocking "[250]" yes
# Non-blocking: gate code 4 tolerated via allow_failure:exit_codes
run_case nonblocking "[4]" no

echo; echo "== SUMMARY: $pass passed, $fail failed =="
echo "logs + build dir under: $WORK"
[ "$fail" -eq 0 ]
