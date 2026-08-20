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

/**
 * Scope visible nodes to curated data products and their sourced product mappings.
 * Returns null when no product typology filter is active.
 *
 * After collecting considered standards, expands (view-only) to CIM → component → CRM
 * neighbourhood. Does not invent product→regulation or product→CRM assertions.
 * Explicit ProductStandardRelevance no-coverage mappings stay visible but do not drive
 * the CIM/CRM walk.
 */
export function productScopeFor({verticalId = "all", productId = "all", postureId = "all"} = {}, nodes, links) {
  if (verticalId === "all" && productId === "all" && postureId === "all") return null;

  const linksFrom = new Map();
  const linksTo = new Map();
  for (const link of links) {
    const source = typeof link.source === "object" ? link.source.id : link.source;
    const target = typeof link.target === "object" ? link.target.id : link.target;
    if (!linksFrom.has(source)) linksFrom.set(source, []);
    if (!linksTo.has(target)) linksTo.set(target, []);
    linksFrom.get(source).push({...link, source, target});
    linksTo.get(target).push({...link, source, target});
  }

  function targets(startIds, type, direction = "out") {
    const result = new Set();
    for (const id of startIds) {
      const candidates = direction === "out" ? (linksFrom.get(id) || []) : (linksTo.get(id) || []);
      for (const link of candidates) {
        if (link.type === type) result.add(direction === "out" ? link.target : link.source);
      }
    }
    return result;
  }

  let products = nodes.filter((node) => (node.labels || []).includes("DataProduct"));
  if (productId !== "all") products = products.filter((node) => node.id === productId);
  if (verticalId !== "all") {
    const verticalKey = verticalId.startsWith("industry-vertical:") ? verticalId.slice("industry-vertical:".length) : verticalId;
    products = products.filter((node) => node.industryVertical === verticalKey || targets([node.id], "IN_INDUSTRY_VERTICAL").has(verticalId));
  }
  if (postureId !== "all") {
    const expectedPosture = (postureId === "personal-data-posture:pii" || postureId === "PII")
      ? "PII"
      : (postureId === "personal-data-posture:no-pii" || postureId === "NO_PII")
        ? "NO_PII"
        : null;
    const expectedPostureNode = expectedPosture === "PII"
      ? "personal-data-posture:pii"
      : expectedPosture === "NO_PII"
        ? "personal-data-posture:no-pii"
        : postureId;
    products = products.filter((node) =>
      node.personalDataPosture === expectedPosture
      || targets([node.id], "HAS_PERSONAL_DATA_POSTURE").has(expectedPostureNode)
    );
  }

  const productIds = new Set(products.map((node) => node.id));
  const scope = new Set(productIds);
  for (const id of targets(productIds, "HAS_PERSONAL_DATA_POSTURE")) scope.add(id);
  for (const id of targets(productIds, "IN_INDUSTRY_VERTICAL")) scope.add(id);

  const productMappings = targets(productIds, "FOR_DATA_PRODUCT", "in");
  for (const id of productMappings) scope.add(id);

  const noCoverageMappings = new Set();
  for (const mappingId of productMappings) {
    for (const link of linksFrom.get(mappingId) || []) {
      if (link.type === "HAS_MAPPING_RELATION" && link.target === "mapping-relation:no-coverage") {
        noCoverageMappings.add(mappingId);
      }
    }
  }

  const standards = targets(productMappings, "CONSIDERS_STANDARD");
  const regulations = targets(productMappings, "CONSIDERS_REGULATION");
  for (const id of [...standards, ...regulations]) scope.add(id);
  for (const id of targets(productMappings, "HAS_MAPPING_RELATION")) scope.add(id);

  const walkStandards = new Set();
  for (const mappingId of productMappings) {
    if (noCoverageMappings.has(mappingId)) continue;
    for (const standardId of targets([mappingId], "CONSIDERS_STANDARD")) walkStandards.add(standardId);
  }

  const cims = targets(walkStandards, "IMPLEMENTATION_OPTION", "in");
  for (const id of cims) scope.add(id);
  const components = targets(cims, "MAPS_COMPONENT_TYPE");
  for (const id of components) scope.add(id);

  const nodeById = new Map(nodes.map((node) => [node.id, node]));
  const crmCandidates = targets(components, "MAPS_COMPONENT_TYPE", "in");
  const crms = new Set();
  for (const id of crmCandidates) {
    const labels = nodeById.get(id)?.labels || [];
    if (!labels.includes("ComponentRegulatoryMapping")) continue;
    crms.add(id);
    scope.add(id);
  }
  const crmRegulations = targets(crms, "REGULATORY_CONTEXT");
  for (const id of crmRegulations) {
    scope.add(id);
    regulations.add(id);
  }

  for (const id of targets(standards, "IN_STANDARD_CATEGORY")) scope.add(id);
  for (const id of targets(regulations, "IN_REGULATION_CATEGORY")) scope.add(id);
  for (const id of targets(standards, "HAS_GOVERNANCE_TYPE")) scope.add(id);
  for (const id of targets(regulations, "HAS_GOVERNANCE_TYPE")) scope.add(id);

  return scope;
}
