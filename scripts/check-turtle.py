#!/usr/bin/env python3
"""Validate Turtle artefacts with Apache Jena riot."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TURTLE = (
    "ontology.ttl",
    "taxonomy.ttl",
    "shapes.ttl",
    "instances.ttl",
    "regulation-instances.ttl",
    "mapping-instances.ttl",
    "component-mappings.ttl",
    "component-regulatory-mappings.ttl",
)


def validate(paths: list[Path]) -> int:
    riot = shutil.which("riot")
    if riot is None:
        print("riot not found on PATH; install Apache Jena RIOT to validate Turtle.", file=sys.stderr)
        return 1
    failed = False
    for path in paths:
        result = subprocess.run(
            [riot, "--validate", str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            failed = True
            sys.stderr.write(result.stderr or result.stdout or f"riot failed for {path}\n")
            print(f"{path}: Turtle validation failed", file=sys.stderr)
    return 1 if failed else 0


def main(arguments: list[str]) -> int:
    selected = [Path(argument) for argument in arguments] if arguments else [ROOT / name for name in DEFAULT_TURTLE]
    existing = [path if path.is_absolute() else ROOT / path for path in selected]
    existing = [path for path in existing if path.suffix == ".ttl" and path.is_file()]
    if not existing:
        print("No Turtle files to validate.", file=sys.stderr)
        return 1
    return validate(existing)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
