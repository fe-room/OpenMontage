import { mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const repoRoot = resolve(root, "..");
const entry = resolve(root, "src/index.tsx");
const props = resolve(repoRoot, "output/finance-dossier-real-stress-test/render-props.json");
const out = resolve(repoRoot, "output/finance-dossier-real-stress-test");

const stills = [
  ["research/stills/01-document.png", 75],
  ["research/stills/02-expectation-gap.png", 195],
  ["research/stills/03-quality.png", 315],
  ["research/stills/04-watch-ending.png", 435],
  ["market/stills/01-hero-move.png", 555],
  ["market/stills/02-event-timeline.png", 675],
  ["market/stills/03-cross-asset.png", 795],
  ["market/stills/04-watch-next.png", 915],
  ["macro/stills/01-policy-document.png", 1035],
  ["macro/stills/02-long-yield-result.png", 1155],
  ["macro/stills/03-conditional-chain.png", 1275],
  ["macro/stills/04-chain-breaker.png", 1395],
  ["flow/stills/01-denominator.png", 1515],
  ["flow/stills/02-sankey-lite.png", 1635],
  ["flow/stills/03-value-capture.png", 1755],
  ["flow/stills/04-model-limitation.png", 1875],
  ["explain/stills/01-misconception.png", 1995],
  ["explain/stills/02-real-10k-example.png", 2115],
  ["explain/stills/03-worked-bridge.png", 2235],
  ["explain/stills/04-takeaway.png", 2355],
];

for (const [relative, frame] of stills) {
  const target = resolve(out, relative);
  mkdirSync(dirname(target), { recursive: true });
  const result = spawnSync(
    resolve(root, "node_modules/.bin/remotion"),
    ["still", entry, "Explainer", target, `--props=${props}`, `--frame=${frame}`],
    { cwd: root, encoding: "utf8", stdio: "inherit" },
  );
  if (result.status !== 0) throw new Error(`Failed to render ${relative}`);
}

console.log(`Rendered ${stills.length} real-topic Finance Dossier stills to ${out}`);
