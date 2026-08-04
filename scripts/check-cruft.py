#!/usr/bin/env python3
"""Reject Finder-style duplicate and editor junk files before they enter version control."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    "dist",
    "build",
}

CRUFT_NAME_PATTERNS = (
    re.compile(r"(?i)^\.ds_store$"),
    re.compile(r"(?i)^thumbs\.db$"),
    re.compile(r"(?i)^desktop\.ini$"),
    re.compile(r".* \d+\.[^.]+$"),  # "file 2.ttl", "script 3.mjs"
    re.compile(r"(?i).* copy(?: \d+)?\.[^.]+$"),  # "file copy.ttl", "file Copy 2.md"
    re.compile(r".*~$"),
    re.compile(r".*\.(?:orig|bak|swp|swo)$"),
)


def is_cruft_name(name: str) -> bool:
    return any(pattern.fullmatch(name) for pattern in CRUFT_NAME_PATTERNS)


def find_cruft(root: Path = ROOT) -> list[Path]:
    findings: list[Path] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.is_file() and is_cruft_name(path.name):
            findings.append(path.relative_to(root))
    return sorted(findings)


def main() -> int:
    findings = find_cruft()
    if not findings:
        return 0
    print("Cruft files must be removed before commit:", file=sys.stderr)
    for path in findings:
        print(f"  {path}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
