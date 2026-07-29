import { readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { csvParse } from "d3";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const [template, d3Bundle, layoutOrdering, graphSelection, mappingExplanationsJson, nodesCsv, linksCsv] = await Promise.all([
  readFile(join(root, "src", "graph.template.html"), "utf8"),
  readFile(join(root, "node_modules", "d3", "dist", "d3.min.js"), "utf8"),
  readFile(join(root, "scripts", "layout-ordering.mjs"), "utf8"),
  readFile(join(root, "scripts", "graph-selection.mjs"), "utf8"),
  readFile(join(root, "src", "mapping-explanations.json"), "utf8"),
  readFile(join(root, "nodes.csv"), "utf8"),
  readFile(join(root, "relationships.csv"), "utf8"),
]);

function normaliseSources(value) {
  return value
    .split("|")
    .map((source) => source.trim())
    .filter(Boolean)
    .filter((source) => {
      try {
        return ["http:", "https:"].includes(new URL(source).protocol);
      } catch {
        return false;
      }
    });
}

const nodes = csvParse(nodesCsv).map((row) => ({
  ...row,
  id: row[":ID"],
  labels: row[":LABEL"].split(";"),
  authoritativeSources: normaliseSources(row.authoritativeSource),
}));
const links = csvParse(linksCsv).map((row, index) => ({
  id: `relationship-${index + 1}`,
  source: row[":START_ID"],
  target: row[":END_ID"],
  type: row[":TYPE"],
  evidenceStatus: row.evidenceStatus,
}));
const mappingExplanations = JSON.parse(mappingExplanationsJson);
const mappingIds = new Set(nodes.filter((node) => node.labels.includes("ComponentImplementationMapping")).map((node) => node.id));
const explanationIds = new Set(Object.keys(mappingExplanations));
const missingExplanations = [...mappingIds].filter((id) => !explanationIds.has(id));
const orphanedExplanations = [...explanationIds].filter((id) => !mappingIds.has(id));
if (missingExplanations.length || orphanedExplanations.length) {
  throw new Error(`Mapping explanation mismatch. Missing: ${missingExplanations.join(", ") || "none"}. Orphaned: ${orphanedExplanations.join(", ") || "none"}.`);
}
for (const [id, explanation] of Object.entries(mappingExplanations)) {
  if (!explanation.rationale || !explanation.boundary || !Array.isArray(explanation.sources) || !explanation.sources.length) {
    throw new Error(`Mapping explanation ${id} must provide rationale, boundary and at least one source.`);
  }
  const invalidSources = explanation.sources.filter((source) => {
    try {
      return !["http:", "https:"].includes(new URL(source).protocol);
    } catch {
      return true;
    }
  });
  if (invalidSources.length) throw new Error(`Mapping explanation ${id} has invalid sources: ${invalidSources.join(", ")}.`);
}
const graphData = JSON.stringify({ nodes, links, mappingExplanations }).replaceAll("</", "<\\/");

const output = template
  .replace("/*__D3__*/", () => d3Bundle)
  .replace("/*__LAYOUT_ORDERING__*/", () => layoutOrdering.replace("export function", "function"))
  .replace("/*__GRAPH_SELECTION__*/", () => graphSelection.replace("export function", "function"))
  .replace("/*__GRAPH_DATA__*/", () => graphData);

await writeFile(join(root, "graph.html"), output, "utf8");
console.log(`Built graph.html with ${nodes.length} nodes and ${links.length} relationships.`);
