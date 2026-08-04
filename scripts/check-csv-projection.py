#!/usr/bin/env python3
"""Validate Neo4j CSV projection integrity for this repository."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NODES = ROOT / "nodes.csv"
RELATIONSHIPS = ROOT / "relationships.csv"
REQUIRED_NODE_COLUMNS = {
    ":ID",
    "id",
    "name",
    "evidenceStatus",
    ":LABEL",
}
REQUIRED_RELATIONSHIP_COLUMNS = {
    ":START_ID",
    ":END_ID",
    ":TYPE",
    "evidenceStatus",
}


def load_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path.name}: missing header row")
        return list(reader.fieldnames), list(reader)


def validate() -> list[str]:
    errors: list[str] = []
    if not NODES.is_file() or not RELATIONSHIPS.is_file():
        return ["nodes.csv and relationships.csv are both required"]

    node_fields, nodes = load_rows(NODES)
    relationship_fields, relationships = load_rows(RELATIONSHIPS)

    missing_node_columns = sorted(REQUIRED_NODE_COLUMNS - set(node_fields))
    if missing_node_columns:
        errors.append(f"nodes.csv missing columns: {', '.join(missing_node_columns)}")
    missing_relationship_columns = sorted(REQUIRED_RELATIONSHIP_COLUMNS - set(relationship_fields))
    if missing_relationship_columns:
        errors.append(f"relationships.csv missing columns: {', '.join(missing_relationship_columns)}")
    if errors:
        return errors

    node_ids: set[str] = set()
    for index, row in enumerate(nodes, start=2):
        node_id = (row.get(":ID") or "").strip()
        if not node_id:
            errors.append(f"nodes.csv:{index}: empty :ID")
            continue
        if node_id in node_ids:
            errors.append(f"nodes.csv:{index}: duplicate :ID {node_id}")
        node_ids.add(node_id)
        if not (row.get(":LABEL") or "").strip():
            errors.append(f"nodes.csv:{index}: empty :LABEL for {node_id}")
        if not (row.get("evidenceStatus") or "").strip():
            errors.append(f"nodes.csv:{index}: empty evidenceStatus for {node_id}")

    for index, row in enumerate(relationships, start=2):
        start_id = (row.get(":START_ID") or "").strip()
        end_id = (row.get(":END_ID") or "").strip()
        rel_type = (row.get(":TYPE") or "").strip()
        if not start_id or not end_id or not rel_type:
            errors.append(f"relationships.csv:{index}: incomplete relationship")
            continue
        if start_id not in node_ids:
            errors.append(f"relationships.csv:{index}: dangling :START_ID {start_id}")
        if end_id not in node_ids:
            errors.append(f"relationships.csv:{index}: dangling :END_ID {end_id}")
        if not (row.get("evidenceStatus") or "").strip():
            errors.append(f"relationships.csv:{index}: empty evidenceStatus")

    return errors


def main() -> int:
    try:
        errors = validate()
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if not errors:
        return 0
    print("CSV projection integrity failed:", file=sys.stderr)
    for error in errors:
        print(f"  {error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
