// 小散经济学 03 — 一次性视觉语言（atelier）
// 触感研究纸 + 印刷规则 + 朱红批注。
// 复用引擎知识（remotion 原语），不复用任何既有创意组件。

export const C = {
  paper: "#F4F1E8", // 中性象牙白基纸
  paperDeep: "#E9E4D6", // 纸片暗面 / 压痕
  ink: "#22201C", // 石墨文字
  inkSoft: "#5A544A", // 次一级文字
  inkFaint: "#97907F", // 说明 / 来源
  vermilion: "#B63A2B", // 朱红批注（稀缺资源）
  teal: "#2E5B5A", // 深青结构线
  shadow: "rgba(34,32,28,0.14)",
} as const;

export const FONT_SERIF =
  '"Songti SC", "STSong", "Noto Serif SC", "SimSun", serif';
export const FONT_SANS =
  '"PingFang SC", "Hiragino Sans GB", "STHeiti", "Microsoft YaHei", sans-serif';

export const FPS = 30;

// ---- 确定性伪随机：固定 seed，绝不逐帧随机（否则压缩后闪烁/爬动）----
export function seeded(seed: number) {
  let s = seed >>> 0;
  return () => {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 4294967296;
  };
}

export function clamp01(x: number) {
  return Math.max(0, Math.min(1, x));
}

// 慢入慢出的纸感缓动：起手略慢、落定干脆
export const easeSettle = (t: number) =>
  clamp01(t) < 0.5
    ? 2 * clamp01(t) * clamp01(t)
    : 1 - Math.pow(-2 * clamp01(t) + 2, 2) / 2;
