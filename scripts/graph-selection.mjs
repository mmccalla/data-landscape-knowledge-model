export function dagLineageFor(selectedNodeId, links, levelForId) {
  const nodeIds = new Set([selectedNodeId]);
  const linkIds = new Set();
  const outgoing = new Map();
  const incoming = new Map();
  for (const link of links) {
    const source = typeof link.source === "object" ? link.source.id : link.source;
    const target = typeof link.target === "object" ? link.target.id : link.target;
    const sourceLevel = levelForId(source);
    const targetLevel = levelForId(target);
    if (!Number.isFinite(sourceLevel) || !Number.isFinite(targetLevel) || sourceLevel === targetLevel) continue;
    const from = sourceLevel < targetLevel ? source : target;
    const to = sourceLevel < targetLevel ? target : source;
    if (!outgoing.has(from)) outgoing.set(from, []);
    if (!incoming.has(to)) incoming.set(to, []);
    outgoing.get(from).push({link, neighbour: to});
    incoming.get(to).push({link, neighbour: from});
  }

  function traverse(adjacency) {
    const visited = new Set([selectedNodeId]);
    const queue = [selectedNodeId];
    while (queue.length) {
      const nodeId = queue.shift();
      for (const {link, neighbour} of adjacency.get(nodeId) || []) {
        linkIds.add(link.id);
        nodeIds.add(neighbour);
        if (visited.has(neighbour)) continue;
        visited.add(neighbour);
        queue.push(neighbour);
      }
    }
  }
  traverse(outgoing);
  traverse(incoming);
  return {nodeIds, linkIds};
}
