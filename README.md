# Darkmoon — GitLab CI/CD Component

Run an AI-driven Darkmoon security assessment from a GitLab pipeline and surface
the results natively in GitLab: a **Code Quality** report (findings in the merge
request widget and the pipeline **Code Quality** tab) and, optionally, a **SAST**
report. Works against **Darkmoon OSS** (local CLI/Docker engine) and **Darkmoon
Pro** (REST API).

This repository ships one component: **`scan`**
(`templates/scan/template.yml`).

> The component wraps the portable `darkmoon-ci` CLI. It does not embed the
> scanning engine. See [`CONTRACT.md`](CONTRACT.md) for the exact CLI + JSON
> interface it consumes.

## Quick start

```yaml
include:
  - component: $CI_SERVER_FQDN/<your-namespace>/darkmoon/scan@1.0.0
    inputs:
      target: "https://staging.example.com"
      fail-on: high        # fail the job on a High+ finding
```

Replace `<your-namespace>` with the group/subgroup that hosts this project on
your GitLab instance (the component path is `<namespace>/darkmoon/scan`, i.e.
`<project-path>/<component-name>`). Pin `@<version>` to a released tag.

### Secrets

Set these as **masked + protected** CI/CD variables (Settings → CI/CD →
Variables). They are read from the environment; the component never places them
on the command line and never prints them.

| Mode | Required variables |
|------|--------------------|
| OSS  | `DARKMOON_LICENSE_KEY`, `OPENROUTER_PROVIDER`, `OPENCODE_MODEL`, `OPENROUTER_API_KEY` |
| Pro  | `DARKMOON_API_TOKEN` (+ `base-url` input, or `DARKMOON_BASE_URL`) |

### Non-blocking (report but don't fail the pipeline)

```yaml
include:
  - component: $CI_SERVER_FQDN/<your-namespace>/darkmoon/scan@1.0.0
    inputs:
      target: "https://staging.example.com"
      fail-on: high
      allow_failure_exit_codes: [4]   # tolerate the findings gate; real errors still fail
```

The findings gate is exit code **4**. The default `allow_failure_exit_codes`
(`[250]`, a code the CLI never emits) makes the job **block**. Listing `4` makes
the gate non-blocking while genuine tool errors (exit `2`/`3`/`5`) still fail the
pipeline.

## Inputs

| Input | Default | Description |
|-------|---------|-------------|
| `target` | *(required)* | Target URL/host, or a full Darkmoon target line. |
| `mode` | `auto` | `auto` (Pro if token+base-url present, else OSS), `oss`, or `pro`. |
| `base-url` | `""` | Pro REST API base URL, or OSS client install base. |
| `focus` | `""` | Comma-separated attack focus (Darkmoon `FOCUS=`). |
| `severity` | `""` | Global max severity cap (Darkmoon `SEVERITY=`). |
| `fail-on` | `high` | Minimum severity that trips the findings gate. `none` disables. |
| `timeout` | `""` | Scan timeout (seconds) passed to `darkmoon-ci`. |
| `sast-report` | `true` | Also emit `gl-sast-report.json`. |
| `expose-full-report` | `false` | Attach the full markdown report + native JSON as (internal) artifacts. |
| `artifacts-expire-in` | `1 week` | Artifact expiry. |
| `allow_failure_exit_codes` | `[250]` | Exit codes tolerated by the job. `[4]` = non-blocking gate. |
| `bootstrap-url` | `""` | If `darkmoon-ci` is absent, download & run this installer first. |
| `image` | `python:3.12-slim` | Image for docker-executor runners (shell runners ignore it). |
| `stage` | `test` | Stage for the job (must exist in the pipeline). |
| `job-name` | `darkmoon_scan` | Name of the generated job. |

## Outputs

- **Code Quality** — `gl-code-quality-report.json`
  (`artifacts:reports:codequality`). One entry per finding, mapped to the
  CodeClimate fields GitLab requires (`description`, `check_name`, `fingerprint`,
  `severity`, `location.path`, `location.lines.begin`).
- **SAST** — `gl-sast-report.json` (`artifacts:reports:sast`), conforming to the
  GitLab `security-report-schemas` SAST schema (validated in CI against the live
  schema; see `test/`). The MR SAST widget requires **Ultimate**.
- **Internal artifacts** (only when `expose-full-report: true`) — the full
  markdown report and native findings JSON, under `output-dir/`.

### What appears where (privacy)

Only a **redaction-safe summary** of each finding is placed on shared surfaces
(the MR/pipeline widgets). Full detail and raw evidence stay in the internal
report artifact, which is off by default. See `CONTRACT.md` §4.

## Runner requirements

- **Pro mode**: a runner whose image provides `darkmoon-ci` + `python3` (≥ 3.8),
  or set `bootstrap-url` to install the CLI. Network access to the Pro API.
- **OSS mode**: `darkmoon-ci` drives the local Darkmoon Docker engine, so use a
  runner with Docker access (a **shell** executor on a Docker host, or
  Docker-in-Docker). `python3` must be available for report mapping.

## Severity mapping

| Darkmoon | Code Quality | SAST |
|----------|--------------|------|
| critical | `blocker`  | `Critical` |
| high     | `critical` | `High` |
| medium   | `major`    | `Medium` |
| low      | `minor`    | `Low` |
| info     | `info`     | `Info` |

## Development & tests

```bash
python3 build/render_template.py      # regenerate templates/scan/template.yml from src/
python3 test/unit_tests.py            # redaction (§4) + degradation (§2.4) + severity maps
python3 test/check_schema_pin.py      # guard against SAST schema drift
bash    test/run_runner_e2e.sh        # REAL gitlab-runner (15.11) end-to-end, live-schema validation
```

`templates/scan/template.yml` is generated: it embeds `src/darkmoon_gitlab_report.py`
(base64) so the component is self-contained YAML. Edit `src/` and the `.yml.in`
skeleton, then re-render.

## Publishing to the CI/CD Catalog (human-only)

1. Make this a **public** project on your GitLab instance and set a project
   description.
2. Enable it as a catalog project (Settings → General → Visibility → *CI/CD
   Catalog project*).
3. Tag a **semantic version** and create a release with the `release` keyword
   (see this repo's own `.gitlab-ci.yml`). The pipeline for the tag publishes the
   component version to the catalog.

## License

MIT — see [`LICENSE`](LICENSE).
