#!/usr/bin/env python3
"""Map Darkmoon native findings JSON to GitLab report formats.

Consumes `darkmoon-findings.json` (contract/1.0, see CONTRACT.md) and emits:
  - gl-code-quality-report.json  (CodeClimate, artifacts:reports:codequality)
  - gl-sast-report.json          (GitLab SAST security-report-schemas)

Design constraints (threat model §4):
  - Only the redaction-safe `summary` field reaches shared surfaces. The full
    `description`/`evidence` are NEVER copied into these reports.
  - Stdlib only. Runs anywhere python3 >= 3.8 exists (default GitLab runners).
  - Degrades gracefully: missing/invalid input -> valid EMPTY reports + warn,
    never a traceback (the findings *gate* is enforced by the CLI exit code, not
    by this mapper, so an empty report must not silently "pass" a real scan).

This is part of the GitLab component. It is not the darkmoon-ci CLI.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re as _re
import sys
from typing import Any, Dict, List

# SAST schema version this mapper was written against. Read live from
# security-report-schemas at build time (see README / test/validate_schemas.py);
# overridable with --sast-schema-version so the pinned schema and the emitted
# report never drift.
DEFAULT_SAST_SCHEMA_VERSION = "15.2.5"

# native severity -> CodeClimate severity
CQ_SEVERITY = {
    "info": "info",
    "low": "minor",
    "medium": "major",
    "high": "critical",
    "critical": "blocker",
}
# native severity -> GitLab SAST severity (Title-case, per live schema enum)
SAST_SEVERITY = {
    "info": "Info",
    "low": "Low",
    "medium": "Medium",
    "high": "High",
    "critical": "Critical",
}


def _warn(msg: str) -> None:
    sys.stderr.write("darkmoon-gitlab-report: %s\n" % msg)


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sast_time(value: Any) -> str:
    """GitLab SAST schema requires 'yyyy-mm-ddThh:mm:ss' (no timezone suffix)."""
    s = str(value or "").strip()
    m = _re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", s)
    if m:
        return m.group(1)
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def _norm_sev(value: Any) -> str:
    s = str(value or "").strip().lower()
    return s if s in CQ_SEVERITY else "info"


def _clean_path(p: Any) -> str:
    p = str(p or "").strip()
    if not p:
        return ".darkmoon/report.md"  # sentinel: no file locus (DAST-style)
    while p.startswith("./"):
        p = p[2:]
    return p.lstrip("/") or ".darkmoon/report.md"


def _line(loc: Dict[str, Any]) -> int:
    try:
        n = int(loc.get("line") or 0)
        return n if n > 0 else 1
    except (TypeError, ValueError):
        return 1


def _fingerprint(f: Dict[str, Any], path: str) -> str:
    basis = "|".join([
        str(f.get("id") or ""),
        path,
        str(f.get("title") or ""),
    ])
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()


def _shared_text(f: Dict[str, Any]) -> str:
    """Redaction-safe text only. Never description/evidence."""
    summary = str(f.get("summary") or "").strip()
    if not summary:
        # Fall back to the title (also author-controlled, non-infra) — never the
        # full description or evidence.
        summary = str(f.get("title") or "Darkmoon finding").strip()
    return summary


def load_findings(path: str) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        _warn("findings file not found: %s -> emitting empty reports" % path)
        return {}
    except (OSError, ValueError) as exc:
        _warn("cannot parse findings file (%s) -> emitting empty reports" % exc)
        return {}
    if not isinstance(data, dict):
        _warn("findings file is not an object -> emitting empty reports")
        return {}
    return data


def to_code_quality(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for f in data.get("findings") or []:
        if not isinstance(f, dict):
            continue
        loc = f.get("location") if isinstance(f.get("location"), dict) else {}
        path = _clean_path(loc.get("path"))
        sev = _norm_sev(f.get("severity"))
        category = str(f.get("category") or "finding").strip() or "finding"
        owasp = str(f.get("owasp") or "").strip()
        tag = " [Darkmoon %s%s]" % (category, (" · " + owasp) if owasp else "")
        out.append({
            "description": _shared_text(f) + tag,
            "check_name": "darkmoon/%s" % category,
            "fingerprint": _fingerprint(f, path),
            "severity": CQ_SEVERITY[sev],
            "location": {"path": path, "lines": {"begin": _line(loc)}},
        })
    return out


def _identifiers(f: Dict[str, Any]) -> List[Dict[str, Any]]:
    ids: List[Dict[str, Any]] = []
    category = str(f.get("category") or "finding").strip() or "finding"
    ids.append({
        "type": "darkmoon_category",
        "name": "Darkmoon: %s" % category,
        "value": category,
    })
    cwe = str(f.get("cwe") or "").strip()
    if cwe:
        num = cwe.upper().replace("CWE-", "").strip()
        ident = {"type": "cwe", "name": cwe, "value": num or cwe}
        if num.isdigit():
            ident["url"] = "https://cwe.mitre.org/data/definitions/%s.html" % num
        ids.append(ident)
    owasp = str(f.get("owasp") or "").strip()
    if owasp:
        ids.append({"type": "owasp", "name": owasp, "value": owasp})
    return ids


def to_sast(data: Dict[str, Any], schema_version: str) -> Dict[str, Any]:
    tool = data.get("tool") if isinstance(data.get("tool"), dict) else {}
    tool_version = str(tool.get("version") or "unknown")
    edition = str(tool.get("edition") or data.get("mode") or "oss")
    started = _sast_time(data.get("started_at") or data.get("generated_at"))
    ended = _sast_time(data.get("generated_at"))

    vulns: List[Dict[str, Any]] = []
    for f in data.get("findings") or []:
        if not isinstance(f, dict):
            continue
        loc = f.get("location") if isinstance(f.get("location"), dict) else {}
        path = _clean_path(loc.get("path"))
        sev = _norm_sev(f.get("severity"))
        vuln = {
            "id": _fingerprint(f, path),  # unique, stable
            "name": (str(f.get("title") or "Darkmoon finding")[:255]),
            "description": _shared_text(f),  # redaction-safe only
            "severity": SAST_SEVERITY[sev],
            "identifiers": _identifiers(f),
            "location": {"file": path, "start_line": _line(loc)},
        }
        solution = str(f.get("remediation") or "").strip()
        if solution:
            vuln["solution"] = solution
        vulns.append(vuln)

    vendor = {"name": "ASC-IT — Darkmoon"}
    analyzer_scanner = {
        "id": "darkmoon",
        "name": "Darkmoon",
        "version": tool_version,
        "vendor": vendor,
    }
    return {
        "version": schema_version,
        "scan": {
            "type": "sast",
            "status": "success",
            "start_time": started,
            "end_time": ended,
            "analyzer": dict(analyzer_scanner),
            "scanner": dict(analyzer_scanner),
        },
        "vulnerabilities": vulns,
    }


def _write(path: str, obj: Any) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="Map Darkmoon findings to GitLab reports")
    ap.add_argument("--findings", required=True, help="path to darkmoon-findings.json")
    ap.add_argument("--codequality", required=True, help="output gl-code-quality-report.json")
    ap.add_argument("--sast", default="", help="output gl-sast-report.json (omit to skip)")
    ap.add_argument("--sast-schema-version", default=DEFAULT_SAST_SCHEMA_VERSION)
    args = ap.parse_args(argv)

    data = load_findings(args.findings)

    cq = to_code_quality(data)
    _write(args.codequality, cq)
    _warn("wrote %d code-quality entries -> %s" % (len(cq), args.codequality))

    if args.sast:
        sast = to_sast(data, args.sast_schema_version)
        _write(args.sast, sast)
        _warn("wrote %d SAST vulnerabilities -> %s" % (len(sast["vulnerabilities"]), args.sast))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
