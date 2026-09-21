import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { C, FONT_MONO, FONT_SANS, clamp01, easeSettle } from "./theme";

// ---------------------------------------------------------------------------
// 基面：仪器刻线纸。静态、无逐帧随机（H.264 下逐帧噪点会爬动）。
// ---------------------------------------------------------------------------

// 极轻的纸面起伏：固定 seed 一次性生成，不随帧变化
const MOTTLE = (() => {
  let s = 20260921 >>> 0;
  const r = () => {
    s = (s * 1664525 + 1013904223) >>> 0;
    return s / 4294967296;
  };
  return Array.from({ length: 260 }, () => ({
    x: r() * 1080,
    y: r() * 1400,
    w: 60 + r() * 220,
    h: 40 + r() * 160,
    o: 0.008 + r() * 0.016,
  }));
})();

export const Plate: React.FC<{
  children?: React.ReactNode;
  tone?: "base" | "deep";
}> = ({ children, tone = "base" }) => (
  <AbsoluteFill
    style={{
      backgroundColor: tone === "base" ? C.base : C.panelSoft,
      fontFamily: FONT_SANS,
      color: C.ink,
      overflow: "hidden",
    }}
  >
    <AbsoluteFill>
      {MOTTLE.map((m, i) => (
        <div
          key={`m${i}`}
          style={{
            position: "absolute",
            left: m.x,
            top: m.y,
            width: m.w,
            height: m.h,
            borderRadius: 8,
            background: "#3A352C",
            opacity: m.o,
          }}
        />
      ))}
    </AbsoluteFill>
    {children}
  </AbsoluteFill>
);

// ---------------------------------------------------------------------------
// 纸片与线：本片的层级规则 —— 1px 暗边 + 克制投影，不做圆角按钮
// ---------------------------------------------------------------------------
export const Panel: React.FC<{
  children?: React.ReactNode;
  style?: React.CSSProperties;
  fill?: string;
  border?: string;
}> = ({ children, style, fill = C.panel, border = `${C.ink}1F` }) => (
  <div
    style={{
      position: "absolute",
      background: fill,
      border: `1px solid ${border}`,
      boxSizing: "border-box",
      ...style,
    }}
  >
    {children}
  </div>
);

export const Rule: React.FC<{
  width: number | string;
  color?: string;
  thickness?: number;
  grow?: number;
  style?: React.CSSProperties;
}> = ({ width, color = C.ink, thickness = 2, grow = 1, style }) => (
  <div
    style={{
      width,
      height: thickness,
      background: color,
      transform: `scaleX(${clamp01(grow)})`,
      transformOrigin: "left center",
      ...style,
    }}
  />
);

// 深墨反白强调块：本片唯一允许的强调方式（不引入第五种彩色）
export const InvertTag: React.FC<{
  children: React.ReactNode;
  grow?: number;
  style?: React.CSSProperties;
}> = ({ children, grow = 1, style }) => (
  <div
    style={{
      position: "absolute",
      background: C.invert,
      color: C.invertText,
      fontFamily: FONT_SANS,
      display: "inline-block",
      transform: `scaleX(${clamp01(grow)})`,
      transformOrigin: "left center",
      whiteSpace: "nowrap",
      ...style,
    }}
  >
    {children}
  </div>
);

export const Kicker: React.FC<{
  children: React.ReactNode;
  style?: React.CSSProperties;
  color?: string;
  size?: number;
}> = ({ children, style, color = C.inkFaint, size = 24 }) => (
  <div
    style={{
      position: "absolute",
      fontFamily: FONT_SANS,
      fontSize: size,
      letterSpacing: 2,
      color,
      whiteSpace: "nowrap",
      ...style,
    }}
  >
    {children}
  </div>
);

export const Num: React.FC<{
  children: React.ReactNode;
  size: number;
  color?: string;
  style?: React.CSSProperties;
  weight?: number;
}> = ({ children, size, color = C.ink, style, weight = 500 }) => (
  <div
    style={{
      position: "absolute",
      fontFamily: FONT_MONO,
      fontSize: size,
      fontWeight: weight,
      letterSpacing: -0.5,
      color,
      whiteSpace: "nowrap",
      ...style,
    }}
  >
    {children}
  </div>
);

export const SourceLine: React.FC<{
  text: string;
  style?: React.CSSProperties;
  size?: number;
  color?: string;
}> = ({ text, style, size = 20, color = C.inkFaint }) => (
  <div
    style={{
      position: "absolute",
      fontFamily: FONT_SANS,
      fontSize: size,
      lineHeight: 1.5,
      letterSpacing: 0.2,
      color,
      ...style,
    }}
  >
    {text}
  </div>
);

// 身份色点 + 名称：色彩之外的识别冗余（色觉障碍 / 小屏 / 压缩）
export const IdentityMark: React.FC<{
  color: string;
  label: string;
  code?: string;
  style?: React.CSSProperties;
  labelSize?: number;
  codeSize?: number;
}> = ({ color, label, code, style, labelSize = 26, codeSize = 20 }) => (
  <div style={{ position: "absolute", display: "flex", alignItems: "center", gap: 10, ...style }}>
    <div style={{ width: 16, height: 16, background: color, flex: "0 0 auto" }} />
    <div style={{ whiteSpace: "nowrap" }}>
      <span style={{ fontFamily: FONT_SANS, fontSize: labelSize, color: C.ink }}>{label}</span>
      {code ? (
        <span
          style={{
            fontFamily: FONT_MONO,
            fontSize: codeSize,
            color: C.inkFaint,
            marginLeft: 10,
          }}
        >
          {code}
        </span>
      ) : null}
    </div>
  </div>
);

// 逐行落定：全片统一的入场节奏，不做弹跳。
// 元素出现的第一帧就带 0.4 不透明度 —— 否则每次硬切都会先闪出一帧空画面。
export const land = (t: number, i: number, stagger = 0.14, dur = 0.42) => {
  const x = t - i * stagger;
  if (x <= 0) return 0;
  return 0.5 + 0.5 * easeSettle(x / dur);
};

// 场景局部时间。场景内部动效一律用它，不用全局 frame。
export const useLocal = (durationInFrames: number) => {
  const frame = useCurrentFrame();
  const sec = frame / 30;
  return {
    frame,
    sec,
    total: durationInFrames / 30,
    t: clamp01(frame / Math.max(1, durationInFrames)),
    prog: (startS: number, durS: number) => clamp01((sec - startS) / Math.max(0.001, durS)),
    since: (s: number) => sec - s,
  };
};
