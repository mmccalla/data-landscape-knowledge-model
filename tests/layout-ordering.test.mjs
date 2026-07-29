import test from "node:test";
import assert from "node:assert/strict";

import { optimiseLayerOrder } from "../scripts/layout-ordering.mjs";

test("relationship-aware ordering removes a simple avoidable crossing", () => {
  const nodes = [
    {id: "a1", level: 0, name: "A1"},
    {id: "a2", level: 0, name: "A2"},
    {id: "b1", level: 1, name: "B1"},
    {id: "b2", level: 1, name: "B2"},
  ];
  const links = [
    {source: "a1", target: "b2"},
    {source: "a2", target: "b1"},
  ];

  const levels = optimiseLayerOrder(nodes, links, node => node.level, node => node.name);

  assert.deepEqual(levels.get(0).map(node => node.id), ["a1", "a2"]);
  assert.deepEqual(levels.get(1).map(node => node.id), ["b2", "b1"]);
});

test("ordering accepts D3 links whose endpoints have been resolved to objects", () => {
  const nodes = [
    {id: "a", level: 0, name: "A"},
    {id: "b", level: 1, name: "B"},
  ];
  const levels = optimiseLayerOrder(
    nodes,
    [{source: nodes[0], target: nodes[1]}],
    node => node.level,
    node => node.name,
  );
  assert.equal(levels.get(1)[0].id, "b");
});

test("unconnected nodes follow connected nodes and remain alphabetically stable", () => {
  const nodes = [
    {id: "a", level: 0, name: "A"},
    {id: "z", level: 1, name: "Z connected"},
    {id: "b", level: 1, name: "B unconnected"},
    {id: "c", level: 1, name: "C unconnected"},
  ];
  const levels = optimiseLayerOrder(nodes, [{source: "a", target: "z"}], node => node.level, node => node.name);
  assert.deepEqual(levels.get(1).map(node => node.id), ["z", "b", "c"]);
});
