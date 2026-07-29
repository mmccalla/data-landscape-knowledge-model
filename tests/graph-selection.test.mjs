import test from "node:test";
import assert from "node:assert/strict";

import { dagLineageFor } from "../scripts/graph-selection.mjs";

test("selection includes DAG ancestors and descendants but excludes sibling branches", () => {
  const levels = new Map([
    ["pattern", 0], ["module", 1], ["sibling-module", 1],
    ["component", 2], ["sibling-component", 2], ["mapping", 3],
  ]);
  const links = [
    {id: "l1", source: "pattern", target: "module"},
    {id: "l2", source: "pattern", target: "sibling-module"},
    {id: "l3", source: "module", target: "component"},
    {id: "l4", source: "sibling-module", target: "sibling-component"},
    {id: "l5", source: "mapping", target: "component"},
    {id: "l6", source: "component", target: "sibling-component"},
  ];
  const result = dagLineageFor("component", links, id => levels.get(id));
  assert.deepEqual([...result.nodeIds].sort(), ["component", "mapping", "module", "pattern"]);
  assert.deepEqual([...result.linkIds].sort(), ["l1", "l3", "l5"]);
});

test("selection accepts D3-resolved object endpoints", () => {
  const result = dagLineageFor("a", [{id: "l1", source: {id: "a"}, target: {id: "b"}}], id => ({a: 0, b: 1})[id]);
  assert.deepEqual([...result.nodeIds].sort(), ["a", "b"]);
  assert.deepEqual([...result.linkIds], ["l1"]);
});
