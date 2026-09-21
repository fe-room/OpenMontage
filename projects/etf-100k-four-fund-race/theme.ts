// 一次性视觉语言（atelier）：仪器刻线纸。
// 复用引擎知识（Remotion 原语、SVG 几何、字体栈），不复用任何既有创意组件。
// 依据：art-direction-instrument-plate.md

export const C = {
  base: "#F6F7F4", // 冷调近白基面（刻意避开象牙暖纸）
  panel: "#FFFFFF",
  panelSoft: "#EFEFEA",
  grid: "#E1E6DF",
  gridSoft: "#EDF0EA",
  ink: "#22201C", // 石墨
  inkSoft: "#5A544A",
  inkFaint: "#97907F",
  rule: "#8C948B", // 起跑线 / 结构线
  under: "rgba(140,148,139,0.11)", // 水下带
  invert: "#22201C", // 深墨反白强调（本片不引入第五种彩色）
  invertText: "#F6F7F4",
} as const;

export const FONT_MONO =
  '"SF Mono", "SFMono-Regular", "Menlo", "Consolas", "DejaVu Sans Mono", monospace';
export const FONT_SANS =
  '"PingFang SC", "Hiragino Sans GB", "STHeiti", "Microsoft YaHei", "Noto Sans SC", sans-serif';

export const clamp01 = (x: number) => Math.max(0, Math.min(1, x));

// 慢入慢出的纸面落定感：起手略慢、落定干脆
export const easeSettle = (t: number) => {
  const x = clamp01(t);
  return x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;
};

export const easeOutCubic = (t: number) => 1 - Math.pow(1 - clamp01(t), 3);

export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

// 金额取整展示：三档字号下都要能一眼读准
export const fmtYuan = (n: number) => `${Math.round(n).toLocaleString("en-US")}`;

export const fmtPct = (x: number, digits = 2) =>
  `${x >= 0 ? "+" : "-"}${Math.abs(x * 100).toFixed(digits)}%`;

export const fmtPctAbs = (x: number, digits = 2) =>
  `${Math.abs(x * 100).toFixed(digits)}%`;

// 等宽数字宽度估算（用于排版自检，不做布局回退）
export const monoWidth = (s: string, size: number) => s.length * size * 0.6;
export const cjkWidth = (s: string, size: number) => s.length * size;
