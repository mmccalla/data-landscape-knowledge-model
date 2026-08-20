#!/usr/bin/env python3
"""Run SHACL validation over the repository Turtle data graph."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHAPES = ROOT / "shapes.ttl"
DATA_FILES = (
    ROOT / "ontology.ttl",
    ROOT / "taxonomy.ttl",
    ROOT / "instances.ttl",
    ROOT / "regulation-instances.ttl",
    ROOT / "mapping-instances.ttl",
    ROOT / "component-mappings.ttl",
    ROOT / "component-regulatory-mappings.ttl",
    ROOT / "product-instances.ttl",
)


def main() -> int:
    riot = shutil.which("riot")
    pyshacl = shutil.which("pyshacl")
    if riot is None or pyshacl is None:
        print("riot and pyshacl must both be on PATH for SHACL validation.", file=sys.stderr)
        return 1
    missing = [path.name for path in (SHAPES, *DATA_FILES) if not path.is_file()]
    if missing:
        print(f"Missing Turtle inputs: {', '.join(missing)}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as directory:
        bundle = Path(directory) / "bundle.ttl"
        riot_result = subprocess.run(
            [riot, "--formatted=turtle", *[str(path) for path in DATA_FILES]],
            capture_output=True,
            text=True,
            check=False,
        )
        if riot_result.returncode != 0:
            sys.stderr.write(riot_result.stderr or riot_result.stdout)
            print("Failed to build Turtle bundle for SHACL.", file=sys.stderr)
            return 1
        bundle.write_text(riot_result.stdout, encoding="utf-8")
        shacl_result = subprocess.run(
            [pyshacl, "-s", str(SHAPES), str(bundle)],
            capture_output=True,
            text=True,
            check=False,
        )
        output = (shacl_result.stdout or "") + (shacl_result.stderr or "")
        if shacl_result.returncode != 0 or "Conforms: True" not in output:
            sys.stderr.write(output)
            print("SHACL validation failed.", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
