export function optimiseLayerOrder(nodes, links, levelFor, labelFor, passes = 4) {
  const levels = new Map();
  const levelById = new Map();
  const neighbours = new Map(nodes.map(node => [node.id, new Set()]));
  for (const node of nodes) {
    const level = levelFor(node);
    levelById.set(node.id, level);
    if (!levels.has(level)) levels.set(level, []);
    levels.get(level).push(node);
  }
  for (const members of levels.values()) members.sort((a, b) => labelFor(a).localeCompare(labelFor(b)));
  for (const link of links) {
    const source = typeof link.source === "object" ? link.source.id : link.source;
    const target = typeof link.target === "object" ? link.target.id : link.target;
    if (!neighbours.has(source) || !neighbours.has(target)) continue;
    neighbours.get(source).add(target);
    neighbours.get(target).add(source);
  }

  const levelNumbers = [...levels.keys()].sort((a, b) => a - b);
  function reorder(level, adjacentLevel) {
    const adjacentPositions = new Map((levels.get(adjacentLevel) || []).map((node, index) => [node.id, index]));
    levels.get(level).sort((a, b) => {
      function barycentre(node) {
        const positions = [...neighbours.get(node.id)]
          .filter(id => levelById.get(id) === adjacentLevel)
          .map(id => adjacentPositions.get(id));
        return positions.length ? positions.reduce((sum, value) => sum + value, 0) / positions.length : Number.POSITIVE_INFINITY;
      }
      const aPosition = barycentre(a);
      const bPosition = barycentre(b);
      if (Number.isFinite(aPosition) !== Number.isFinite(bPosition)) return Number.isFinite(aPosition) ? -1 : 1;
      const difference = aPosition - bPosition;
      return Number.isFinite(difference) && difference !== 0 ? difference : labelFor(a).localeCompare(labelFor(b));
    });
  }

  for (let pass = 0; pass < passes; pass += 1) {
    for (let index = 1; index < levelNumbers.length; index += 1) reorder(levelNumbers[index], levelNumbers[index - 1]);
    for (let index = levelNumbers.length - 2; index >= 0; index -= 1) reorder(levelNumbers[index], levelNumbers[index + 1]);
  }
  return levels;
}
