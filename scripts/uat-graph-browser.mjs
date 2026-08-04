import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { extname, join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const mime = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
};

const server = createServer(async (req, res) => {
  const path = join(root, decodeURIComponent((req.url || "/").split("?")[0].replace(/^\//, "") || "graph.html"));
  try {
    const body = await readFile(path);
    res.writeHead(200, { "Content-Type": mime[extname(path)] || "application/octet-stream" });
    res.end(body);
  } catch {
    res.writeHead(404).end("not found");
  }
});

await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const { port } = server.address();
const base = `http://127.0.0.1:${port}`;
const failures = [];

function assert(condition, message) {
  if (!condition) failures.push(message);
}

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
const consoleErrors = [];
page.on("pageerror", (error) => consoleErrors.push(String(error)));
page.on("console", (msg) => {
  if (msg.type() === "error") consoleErrors.push(msg.text());
});

await page.goto(`${base}/graph.html`, { waitUntil: "networkidle" });
await page.waitForSelector("#graph");
await page.waitForTimeout(800);

const baseline = await page.evaluate(() => {
  const data = JSON.parse(document.getElementById("graph-data").textContent);
  const regulatoryNodes = data.nodes.filter((node) => node.labels.includes("ComponentRegulatoryMapping"));
  const regulatoryLinks = [...document.querySelectorAll("line.link.regulatory")].length;
  const complianceLinks = [...document.querySelectorAll("line.link.compliance")].length;
  return {
    title: document.title,
    nodeCount: data.nodes.length,
    linkCount: data.links.length,
    regulatoryMappingCount: regulatoryNodes.length,
    visibleCount: document.getElementById("visible-count")?.textContent || "",
    filterPresent: Boolean(document.getElementById("filter-component-regulatory-mappings")),
    regulatoryLinks,
    complianceLinks,
    arrowRegulatory: Boolean(document.querySelector("#arrow-regulatory")),
  };
});

assert(baseline.nodeCount === 393, `expected 393 nodes, got ${baseline.nodeCount}`);
assert(baseline.linkCount === 921, `expected 921 links, got ${baseline.linkCount}`);
assert(baseline.regulatoryMappingCount === 12, `expected 12 regulatory mappings, got ${baseline.regulatoryMappingCount}`);
assert(baseline.filterPresent, "component regulatory filter missing");
assert(baseline.arrowRegulatory, "arrow-regulatory marker missing");
assert(baseline.regulatoryLinks > 0, "no visible REGULATORY_CONTEXT edges styled as regulatory");
assert(baseline.complianceLinks > 0, "no visible compliance edges");

await page.uncheck("#filter-component-regulatory-mappings");
await page.waitForTimeout(400);
const afterHide = await page.evaluate(() => ({
  regulatoryLinks: [...document.querySelectorAll("line.link.regulatory")].length,
  regulatoryNodes: [...document.querySelectorAll("g.node")].filter((node) => {
    const fill = node.querySelector("circle")?.getAttribute("fill");
    return fill === "#8b5a2b";
  }).length,
}));
assert(afterHide.regulatoryLinks === 0, "regulatory edges still visible after filter off");
assert(afterHide.regulatoryNodes === 0, "regulatory nodes still visible after filter off");

await page.check("#filter-component-regulatory-mappings");
await page.selectOption("#component-select", { label: "Secure read access" });
await page.waitForTimeout(600);
const scoped = await page.evaluate(() => {
  const summary = document.getElementById("visible-count")?.textContent || "";
  const selected = document.querySelector("g.node.selected, g.node[aria-pressed='true']");
  const detail = document.querySelector(".details")?.textContent || "";
  const regulatoryVisible = [...document.querySelectorAll("g.node")].filter((node) => node.querySelector("circle")?.getAttribute("fill") === "#8b5a2b").length;
  return { summary, detail, regulatoryVisible, hasRequirementHint: /Requirement|GDPR|HIPAA|NIST|AC-3/i.test(detail + summary) };
});
assert(scoped.regulatoryVisible >= 1, "secure-read scope did not show regulatory mapping nodes");
assert(/Secure read access/i.test(scoped.summary) || scoped.regulatoryVisible >= 1, "pipeline scope summary missing secure read context");

// Click a regulatory node if present
const clicked = await page.evaluate(() => {
  const node = [...document.querySelectorAll("g.node")].find((item) => item.querySelector("circle")?.getAttribute("fill") === "#8b5a2b");
  if (!node) return false;
  node.dispatchEvent(new MouseEvent("click", { bubbles: true }));
  return true;
});
assert(clicked, "could not click a regulatory mapping node");
await page.waitForTimeout(300);
const detailAfterClick = await page.evaluate(() => document.querySelector(".details")?.textContent || "");
assert(/Requirement|CURATED_REGULATORY_RELEVANCE|Entropy Data|Article|AC-3|SI-|Principle/i.test(detailAfterClick), "details panel missing regulatory provenance after click");

await page.selectOption("#regulation-category-select", { index: 1 });
await page.waitForTimeout(500);
const categoryFiltered = await page.evaluate(() => document.getElementById("visible-count")?.textContent || "");
assert(Boolean(categoryFiltered), "regulation category filter produced empty summary unexpectedly");

await browser.close();
server.close();

const report = {
  baseline,
  afterHide,
  scoped: { ...scoped, detailSnippet: scoped.detail.slice(0, 240) },
  detailAfterClick: detailAfterClick.slice(0, 400),
  categoryFiltered,
  consoleErrors,
  failures,
  passed: failures.length === 0 && consoleErrors.length === 0,
};

console.log(JSON.stringify(report, null, 2));
if (!report.passed) process.exit(1);
