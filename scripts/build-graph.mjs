import { readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { csvParse } from "d3";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const [template, d3Bundle, layoutOrdering, graphSelection, nodesCsv, linksCsv] = await Promise.all([
  readFile(join(root, "src", "graph.template.html"), "utf8"),
  readFile(join(root, "node_modules", "d3", "dist", "d3.min.js"), "utf8"),
  readFile(join(root, "scripts", "layout-ordering.mjs"), "utf8"),
  readFile(join(root, "scripts", "graph-selection.mjs"), "utf8"),
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
const graphData = JSON.stringify({ nodes, links }).replaceAll("</", "<\\/");

const output = template
  .replace("/*__D3__*/", () => d3Bundle)
  .replace("/*__LAYOUT_ORDERING__*/", () => layoutOrdering.replace("export function", "function"))
  .replace("/*__GRAPH_SELECTION__*/", () => graphSelection.replace("export function", "function"))
  .replace("/*__GRAPH_DATA__*/", () => graphData);

await writeFile(join(root, "graph.html"), output, "utf8");
console.log(`Built graph.html with ${nodes.length} nodes and ${links.length} relationships.`);
