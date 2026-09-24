# Darkmoon CI contract (frozen)

This document freezes the interface this GitLab component consumes. It mirrors
§2.2 (frozen contract) and §3.2 (GitLab) of the integrations plan. The component
here is built **only** against this interface — it never reimplements the
`darkmoon-ci` CLI, and the CLI is shipped separately (portable, one binary/script).

Version: `contract/1.0`. Any change is a new major of this document and of the
component.

## 1. The `darkmoon-ci` CLI

Single portable entrypoint on `PATH`, invoked as:

```
darkmoon-ci scan \
  --mode <auto|oss|pro> \
  --target "<target-spec>" \
  [--base-url <url>] \
  [--focus <csv>] \
  [--severity <info|low|medium|high|critical>] \
  [--fail-on <none|info|low|medium|high|critical>] \
  --output-dir <dir> \
  [--format json,markdown] \
  [--redact | --no-redact] \
  [--timeout <seconds>] \
  [--quiet]
```

- `--mode` — `oss` drives the local Darkmoon OSS engine (Docker CLI + markdown
  report → JSON). `pro` calls the Darkmoon Pro REST API at `--base-url`. `auto`
  (default) picks `pro` when `DARKMOON_API_TOKEN` + a base URL are present, else
  `oss`.
- `--target` — the assessment target. Accepts a bare URL/host or a full Darkmoon
  target line (`TARGET: http://host FOCUS=... SEVERITY=...`). The component
  passes a URL/host and lets `--focus`/`--severity` carry the rest.
- `--base-url` — Pro API base (`https://api.darkmoon.example`) or, in OSS mode,
  the client install base (default `https://client.dark-moon.org`).
- `--focus` — comma-separated attack focus (maps to Darkmoon `FOCUS=`).
- `--severity` — global max severity cap (Darkmoon `SEVERITY=`).
- `--fail-on` — minimum severity that trips the **findings gate** (see exit
  codes). `none` disables the gate.
- `--output-dir` — directory the CLI writes its artifacts into (created if
  absent).
- `--redact` (default) — the redaction-safe `summary` field is populated for
  every finding and `description`/`evidence` are still written to the native
  JSON, which is an **internal** artifact. `--no-redact` is a no-op on output
  shape; redaction of shared surfaces is the consumer's responsibility (this
  component only ever publishes `summary` on shared surfaces — see §4).

### 1.1 Secrets — env only, never argv

The CLI reads all secrets from the environment, never from flags, and never
echoes them:

- OSS: `DARKMOON_LICENSE_KEY`, plus the LLM provider config
  `OPENROUTER_PROVIDER`, `OPENCODE_MODEL`, `OPENROUTER_API_KEY`.
- Pro: `DARKMOON_API_TOKEN` (+ optional `DARKMOON_BASE_URL`).

### 1.2 Exit codes (frozen)

| Code | Meaning | Component behaviour |
|-----:|---------|---------------------|
| `0`  | Scan completed, **no** finding at/above `--fail-on` | job passes |
| `4`  | Scan completed, **at least one** finding at/above `--fail-on` (gate tripped) | job **fails**; non-blocking mode lists `4` in `allow_failure:exit_codes` |
| `2`  | Usage / configuration error (bad flags, missing input) | job fails (real error) |
| `3`  | Runtime / scan error (engine down, target unreachable) | job fails (real error) |
| `5`  | Authentication / license error | job fails (real error) |

The gate (`4`) is deliberately distinct from tool errors (`2`,`3`,`5`) so that
`allow_failure:exit_codes: [4]` makes **only the gate** non-blocking while a real
tool failure still fails the pipeline.

## 2. Native findings JSON (frozen schema `contract/1.0`)

Written to `<output-dir>/darkmoon-findings.json`. This is the single artifact the
component maps to GitLab report formats.

```jsonc
{
  "schema_version": "contract/1.0",
  "tool": { "name": "darkmoon-ci", "version": "1.4.0", "edition": "oss|pro" },
  "mode": "oss|pro",
  "target": "<redaction-safe target label>",
  "generated_at": "2026-09-24T12:00:00Z",
  "started_at": "2026-09-24T11:40:00Z",
  "severity_cap": "critical",
  "fail_on": "high",
  "summary": {
    "total": 13,
    "by_severity": {"critical":2,"high":4,"medium":5,"low":1,"info":1},
    "gate": "high",
    "gate_tripped": true
  },
  "findings": [
    {
      "id": "vuln_127baf",
      "title": "SQL injection in /rest/products/search",
      "severity": "critical",              // info|low|medium|high|critical
      "category": "sqli",                   // taxonomy slug → check_name
      "summary": "Union-based SQLi in the product search endpoint.",  // SHARED-SAFE
      "description": "<full detail; may quote infra — INTERNAL only>",
      "evidence": "<raw request/response — INTERNAL only>",
      "location": { "path": "rest/products/search", "line": 1, "url": "http://host/rest/products/search" },
      "cwe": "CWE-89",
      "owasp": "A03:2021-Injection",
      "cvss": 9.8,
      "confidence": "confirmed",            // confirmed|manual|probable
      "status": "exploited",                // exploited|confirmed|reported
      "remediation": "Use parameterised queries."
    }
  ]
}
```

Field contract for the consumer:

- `summary` is the **only** finding text allowed on shared surfaces (MR widget,
  Code Quality diff, SAST widget). `description` and `evidence` are internal.
- `location.path` is a repository-relative path when known, otherwise a URL path
  (no leading `./`). `location.line` is a 1-based integer or `null`.
- `severity` is one of the five ordered levels above.

## 3. Mapping to GitLab (done by this component, not the CLI)

- **Code Quality** (CodeClimate) — one entry per finding: `description` =
  `summary` (+ `[Darkmoon <category> · <owasp>]`), `check_name` =
  `darkmoon/<category>`, `fingerprint` = SHA-256 of `id|path|title`, `severity`
  mapped `info→info, low→minor, medium→major, high→critical, critical→blocker`,
  `location.path` + `location.lines.begin`.
- **SAST** (security-report-schemas, read live at build time) — `version` and the
  required `scan`/`vulnerabilities` shape taken from the live schema; severity
  mapped to Title-case `Info/Low/Medium/High/Critical`; `identifiers` carry the
  Darkmoon category and CWE; `location.file`/`start_line` from `location`;
  `description` = `summary` only.

## 4. Threat-model constraints honoured (§4)

- Shared surfaces publish `summary` only — never `evidence`/`description`.
- Full markdown report + native JSON are plain artifacts, marked internal,
  short expiry, and **opt-in** to expose on shared widgets.
- Secrets via masked+protected CI/CD variables, passed as env, never argv, never
  echoed; sensitive steps run with shell tracing off.
