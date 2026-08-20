/**
 * Capture README hero screenshots from the standalone graph.
 * Usage: node scripts/capture-readme-heroes.mjs
 */
import { createServer } from "node:http";
import { readFile, mkdir } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const outPath = join(root, "docs", "images", "product-graph.png");

const server = createServer(async (_req, res) => {
  try {
    const body = await readFile(join(root, "graph.html"));
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    res.end(body);
  } catch {
    res.writeHead(404).end("not found");
  }
});

await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const { port } = server.address();

await mkdir(join(root, "docs", "images"), { recursive: true });

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1280, height: 820 }, deviceScaleFactor: 1 });
await page.goto(`http://127.0.0.1:${port}/graph.html`, { waitUntil: "networkidle" });
await page.waitForSelector("#graph g.node");

await page.addStyleTag({
  content: `
    header { display: none !important; }
    body { margin: 0 !important; overflow: hidden !important; }
    .layout {
      height: 780px !important;
      min-height: 780px !important;
      max-height: 780px !important;
      margin: 0 !important;
      overflow: hidden !important;
    }
    .sidebar { max-height: 780px !important; overflow: auto !important; }
    .workspace { height: 100% !important; min-height: 0 !important; }
    .graph-wrap { height: 100% !important; min-height: 560px !important; }
  `,
});

await page.selectOption("#product-select", "product:retail-stock-data-product");
await page.waitForTimeout(400);
await page.evaluate(() => window.dispatchEvent(new Event("resize")));
await page.waitForTimeout(2200);
if ((await page.getAttribute("#toggle-freeze", "aria-pressed")) !== "true") {
  await page.click("#toggle-freeze");
}
await page.waitForTimeout(250);

await page.screenshot({
  path: outPath,
  clip: { x: 0, y: 0, width: 1280, height: 800 },
  type: "png",
});

await browser.close();
server.close();
console.log(`Wrote ${outPath}`);
