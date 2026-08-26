import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const entry = resolve(root, "src/index.tsx");
const smokeProps = resolve(root, "test-fixtures/finance-dossier-smoke.json");
const legacyProps = resolve(root, "test-fixtures/legacy-explainer.json");
const outDir = resolve(root, "out/finance-smoke");
rmSync(outDir, { recursive: true, force: true });
mkdirSync(outDir, { recursive: true });

const run = (args, capture = false) => {
  const result = spawnSync(resolve(root, "node_modules/.bin/remotion"), args, {
    cwd: root,
    encoding: "utf8",
    stdio: capture ? "pipe" : "inherit",
  });
  if (result.status !== 0) throw new Error(result.stderr || `remotion ${args[0]} failed`);
  return `${result.stdout || ""}\n${result.stderr || ""}`.replace(/\u001b\[[0-9;]*m/g, "");
};

const assertResolution = (props, expected) => {
  const output = run(["compositions", entry, `--props=${props}`], true);
  const explainerLine = output.split("\n").find((line) => line.includes("Explainer")) || output;
  if (!explainerLine.includes(expected)) throw new Error(`Explainer did not resolve to ${expected}:\n${explainerLine}`);
};

assertResolution(legacyProps, "1920x1080");
assertResolution(smokeProps, "1080x1920");

const landscapeProps = resolve(outDir, "finance-landscape.json");
const landscapePayload = JSON.parse(readFileSync(smokeProps, "utf8"));
landscapePayload.width = 1920;
landscapePayload.height = 1080;
landscapePayload.cuts = landscapePayload.cuts.slice(0, 1);
landscapePayload.cuts[0].out_seconds = 3;
writeFileSync(landscapeProps, JSON.stringify(landscapePayload));
assertResolution(landscapeProps, "1920x1080");

const stills = [
  ["evidence", 60], ["gap-split", 150], ["gap-stacked", 240], ["gap-delta", 330],
  ["gap-reveal", 438], ["flow-horizontal", 510], ["flow-sankey", 600], ["timeline", 690], ["scenarios", 780],
];
for (const [name, frame] of stills) {
  run(["still", entry, "Explainer", resolve(outDir, `${name}.png`), `--props=${smokeProps}`, `--frame=${frame}`]);
}
run(["still", entry, "Explainer", resolve(outDir, "landscape-evidence.png"), `--props=${landscapeProps}`, "--frame=60"]);

const pngSize = (path) => { const data = readFileSync(path); return [data.readUInt32BE(16), data.readUInt32BE(20)]; };
const digest = (path) => createHash("sha256").update(readFileSync(path)).digest("hex");
for (const [name] of stills) {
  const size = pngSize(resolve(outDir, `${name}.png`));
  if (size[0] !== 1080 || size[1] !== 1920) throw new Error(`${name} rendered at ${size.join("x")}`);
}
const landscapeSize = pngSize(resolve(outDir, "landscape-evidence.png"));
if (landscapeSize[0] !== 1920 || landscapeSize[1] !== 1080) throw new Error(`landscape finance rendered at ${landscapeSize.join("x")}`);
const gapHashes = ["gap-split", "gap-stacked", "gap-delta", "gap-reveal"].map((name) => digest(resolve(outDir, `${name}.png`)));
if (new Set(gapHashes).size !== gapHashes.length) throw new Error("ExpectationGap variants are not visually distinct");
if (digest(resolve(outDir, "flow-horizontal.png")) === digest(resolve(outDir, "flow-sankey.png"))) throw new Error("sankey-lite matches horizontal output");
console.log(`Finance smoke passed: ${stills.length} portrait stills plus 1 landscape still`);
