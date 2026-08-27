import { mkdirSync, rmSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repoRoot = resolve(root, "..");
const entry = resolve(root, "src/index.tsx");
const props = resolve(root, "test-fixtures/finance-dossier-v1.2.json");
const outDir = resolve(repoRoot, "output/finance-dossier-v1.2-stills");
rmSync(outDir, { recursive: true, force: true });
mkdirSync(outDir, { recursive: true });

const stills = [
  ["01-expectation-split.png", 90],
  ["02-expectation-stacked.png", 210],
  ["03-expectation-delta.png", 330],
  ["04-reveal-a.png", 390],
  ["05-reveal-b.png", 456],
  ["06-reveal-c.png", 510],
  ["07-moneyflow-horizontal.png", 600],
  ["08-moneyflow-sankey-lite.png", 720],
  ["09-title-long-chinese.png", 840],
  ["10-title-long-bilingual.png", 960],
  ["11-canvas-paper.png", 1080],
  ["12-canvas-document.png", 1200],
  ["13-canvas-data.png", 1320],
  ["14-canvas-margin-note.png", 1440],
  ["15-canvas-dark-ink.png", 1560],
  ["16-source-strip.png", 1680],
  ["17-node-long-label.png", 1800],
  ["18-annotation-example.png", 1920],
];

for (const [name, frame] of stills) {
  const result = spawnSync(resolve(root, "node_modules/.bin/remotion"), ["still", entry, "Explainer", resolve(outDir, name), `--props=${props}`, `--frame=${frame}`], { cwd: root, encoding: "utf8", stdio: "inherit" });
  if (result.status !== 0) throw new Error(`Failed to render ${name}`);
}

console.log(`Rendered ${stills.length} Finance Dossier V1.2 stills to ${outDir}`);
