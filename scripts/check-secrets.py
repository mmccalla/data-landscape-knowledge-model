#!/usr/bin/env python3
"""Reject common credential formats before they enter version control."""

from __future__ import annotations

import re
import sys
from pathlib import Path


PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----"),
    "AWS access key": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,255}|github_pat_[A-Za-z0-9_]{40,255})\b"),
    "GitLab token": re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"),
    "Stripe live key": re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{16,}\b"),
    "Google API key": re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    "assigned credential": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|password)\b"
        r"\s*[:=]\s*['\"](?!\$|\{|<|example|changeme|placeholder)[^'\"\s]{12,}['\"]"
    ),
}


def scan(path: Path) -> list[tuple[int, str]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    findings = []
    for line_number, line in enumerate(lines, start=1):
        if "pragma: allowlist secret" in line:
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(line):
                findings.append((line_number, label))
    return findings


def main(arguments: list[str]) -> int:
    failed = False
    for filename in arguments:
        for line_number, label in scan(Path(filename)):
            print(f"{filename}:{line_number}: possible {label}", file=sys.stderr)
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
