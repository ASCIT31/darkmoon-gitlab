#!/usr/bin/env python3
"""Unit tests for the mapper: redaction (§4), degradation (§2.4), severity maps."""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
MAPPER = os.path.join(REPO, "src", "darkmoon_gitlab_report.py")
VALIDATE = os.path.join(HERE, "validate_schemas.py")

SECRET_DESC = "Real infra 10.0.0.5:22 root:Hunter2 — MUST NOT LEAK"
SECRET_EV = "GET /admin?token=glpat-SECRETSHOULDNOTLEAK HTTP/1.1"

n_pass = 0
n_fail = 0


def check(cond, msg):
    global n_pass, n_fail
    if cond:
        print("  PASS:", msg); n_pass += 1
    else:
        print("  FAIL:", msg); n_fail += 1


def run_mapper(findings_path, cq, sast):
    return subprocess.run(
        [sys.executable, MAPPER, "--findings", findings_path,
         "--codequality", cq, "--sast", sast],
        capture_output=True, text=True)


def test_redaction(tmp):
    native = {
        "schema_version": "contract/1.0",
        "tool": {"name": "darkmoon-ci", "version": "1.4.0", "edition": "pro"},
        "mode": "pro", "target": "app", "generated_at": "2026-09-24T10:00:00Z",
        "fail_on": "high",
        "findings": [{
            "id": "DM-1", "title": "SQLi in search", "severity": "critical",
            "category": "sqli", "summary": "Union-based SQLi in product search.",
            "description": SECRET_DESC, "evidence": SECRET_EV,
            "location": {"path": "rest/products/search", "line": 12},
            "cwe": "CWE-89", "owasp": "A03:2021-Injection", "remediation": "Parameterise.",
        }],
    }
    fp = os.path.join(tmp, "n.json")
    with open(fp, "w") as fh:
        json.dump(native, fh)
    cq, sast = os.path.join(tmp, "cq.json"), os.path.join(tmp, "sast.json")
    run_mapper(fp, cq, sast)
    cq_txt = open(cq).read()
    sast_txt = open(sast).read()
    check(SECRET_DESC not in cq_txt and SECRET_DESC not in sast_txt,
          "full description never appears in shared reports")
    check(SECRET_EV not in cq_txt and SECRET_EV not in sast_txt,
          "raw evidence never appears in shared reports")
    check("Union-based SQLi" in cq_txt and "Union-based SQLi" in sast_txt,
          "redaction-safe summary IS used in shared reports")
    cqd = json.loads(cq_txt)
    check(cqd[0]["severity"] == "blocker", "critical -> blocker (CodeClimate)")
    sd = json.loads(sast_txt)
    check(sd["vulnerabilities"][0]["severity"] == "Critical", "critical -> Critical (SAST)")
    check(sd["scan"]["start_time"].endswith("00") and "Z" not in sd["scan"]["start_time"],
          "SAST scan.start_time has no timezone suffix (schema pattern)")


def test_degradation(tmp):
    cq, sast = os.path.join(tmp, "cq2.json"), os.path.join(tmp, "sast2.json")
    # missing file
    r = run_mapper(os.path.join(tmp, "does-not-exist.json"), cq, sast)
    check(r.returncode == 0, "missing findings file -> mapper exits 0 (no crash)")
    check(json.loads(open(cq).read()) == [], "missing input -> empty code-quality array")
    empty_sast = json.loads(open(sast).read())
    check(empty_sast["vulnerabilities"] == [], "missing input -> empty SAST vulnerabilities")
    # malformed file
    bad = os.path.join(tmp, "bad.json")
    open(bad, "w").write("{not json")
    r = run_mapper(bad, cq, sast)
    check(r.returncode == 0, "malformed findings file -> mapper exits 0 (no crash)")
    # empty SAST still schema-valid
    v = subprocess.run([sys.executable, VALIDATE, cq, sast], capture_output=True, text=True)
    check(v.returncode == 0, "empty reports still validate against live schemas")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        print("== redaction (§4) =="); test_redaction(tmp)
        print("== degradation (§2.4) =="); test_degradation(tmp)
    print("\n== UNIT SUMMARY: %d passed, %d failed ==" % (n_pass, n_fail))
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
