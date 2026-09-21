import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { C, FONT_SANS, FONT_SERIF, seeded } from "./theme";

// ---------------------------------------------------------------------------
// 纸张基座。纹理固定 seed 一次性生成，不随帧变化。
// 这是引擎知识（如何做静态颗粒），不是可复用的创意组件。
// ---------------------------------------------------------------------------

// 纸纤维：稀疏短划线，坐标固定
const FIBERS = (() => {
  const r = seeded(20260921);
  return Array.from({ length: 190 }, () => ({
    x: r() * 1080,
    y: r() * 1920,
    len: 6 + r() * 26,
    rot: -25 + r() * 50,
    o: 0.05 + r() * 0.1,
  }));
})();

// 细颗粒：低频明暗
const GRAIN = (() => {
  const r = seeded(7717);
  return Array.from({ length: 5200 }, () => ({
    x: r() * 1080,
    y: r() * 1920,
    s: 0.8 + r() * 1.9,
    o: 0.012 + r() * 0.045,
    dark: r() > 0.45,
  }));
})();

export const PaperBase: React.FC<{
  children?: React.ReactNode;
  tone?: "base" | "deep";
  vignette?: boolean;
}> = ({ children, tone = "base", vignette = true }) => {
  return (
    <AbsoluteFill
      style={{
        backgroundColor: tone === "base" ? C.paper : C.paperDeep,
        fontFamily: FONT_SERIF,
        color: C.ink,
        overflow: "hidden",
      }}
    >
      <AbsoluteFill>
        {GRAIN.map((g, i) => (
          <div
            key={`g${i}`}
            style={{
              position: "absolute",
              left: g.x,
              top: g.y,
              width: g.s,
              height: g.s,
              borderRadius: g.s,
              background: g.dark ? "#3A352C" : "#FFFFFF",
              opacity: g.o,
            }}
          />
        ))}
      </AbsoluteFill>
      <AbsoluteFill>
        {FIBERS.map((f, i) => (
          <div
            key={`f${i}`}
            style={{
              position: "absolute",
              left: f.x,
              top: f.y,
              width: f.len,
              height: 1,
              background: "#4A4438",
              opacity: f.o,
              transform: `rotate(${f.rot}deg)`,
            }}
          />
        ))}
      </AbsoluteFill>
      {vignette ? (
        <AbsoluteFill
          style={{
            background:
              "radial-gradient(120% 90% at 50% 42%, rgba(0,0,0,0) 52%, rgba(52,46,36,0.16) 100%)",
          }}
        />
      ) : null}
      {children}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// 纸片：1px 暗边 + 克制投影 + 轻微旋转，形成真实厚度
// ---------------------------------------------------------------------------
export const Slip: React.FC<{
  children?: React.ReactNode;
  style?: React.CSSProperties;
  rotate?: number;
  lift?: number;
  dim?: number;
  selected?: boolean;
}> = ({ children, style, rotate = 0, lift = 0, dim = 0, selected = false }) => (
  <div
    style={{
      position: "absolute",
      background: C.paper,
      border: `1px solid ${C.ink}22`,
      boxShadow: selected
        ? `0 ${8 + lift}px ${20 + lift * 2}px ${C.shadow}`
        : `0 ${3 + lift}px ${10 + lift}px rgba(34,32,28,${0.09 + lift * 0.012})`,
      transform: `rotate(${rotate}deg) translateY(${-lift}px)`,
      opacity: 1 - dim * 0.62,
      filter: dim > 0.5 ? "saturate(0.5)" : "none",
      ...style,
    }}
  >
        {children}
  </div>
);

// 印刷细线：规则的、被排出来的线，而不是描边卡片
export const Rule: React.FC<{
  width: number | string;
  color?: string;
  thickness?: number;
  grow?: number; // 0..1 从左展开
  style?: React.CSSProperties;
}> = ({ width, color = C.ink, thickness = 2, grow = 1, style }) => (
  <div
    style={{
      width,
      height: thickness,
      background: color,
      transform: `scaleX(${grow})`,
      transformOrigin: "left center",
      ...style,
    }}
  />
);

// 朱红批注：全片稀缺资源，出现次数应当可数
export const Annotation: React.FC<{
  children?: React.ReactNode;
  grow?: number;
  style?: React.CSSProperties;
}> = ({ children, grow = 1, style }) => (
  <div
    style={{
      position: "absolute",
      borderTop: `3px solid ${C.vermilion}`,
      transform: `scaleX(${grow})`,
      transformOrigin: "left top",
      ...style,
    }}
  >
    {children}
  </div>
);

// 来源小字：只在承载事实的场景出现，且保持可读
export const SourceLine: React.FC<{
  text: string;
  style?: React.CSSProperties;
  opacity?: number;
}> = ({ text, style, opacity = 1 }) => (
  <div
    style={{
      position: "absolute",
      fontFamily: FONT_SANS,
      fontSize: 19,
      lineHeight: 1.5,
      letterSpacing: 0.2,
      color: C.inkFaint,
      opacity,
      ...style,
    }}
  >
    {text}
  </div>
);

// 系列角标：系列感交给画面，而不是口播
export const SeriesChip: React.FC<{ opacity?: number; bottom?: number }> = ({
  opacity = 1,
  bottom = 300,
}) => (
  <div
    style={{
      position: "absolute",
      left: 96,
      bottom,
      fontFamily: FONT_SANS,
      fontSize: 22,
      letterSpacing: 3,
      color: C.inkSoft,
      opacity,
    }}
  >
    小散经济学 03
  </div>
);

// ---------------------------------------------------------------------------
// 常驻系列标题（页眉）。
// 几何对齐第 02 期：文字墨迹 y 226–251，下方 2px 细线在 y=293、x 110→969，
// 线色 rgb(70,83,79)。系列一致性优先于本期美术自由。
// 实拍场景用浅色变体，否则深色文字在暗画面上不可读。
// ---------------------------------------------------------------------------
export const HEADER_RULE_TOP = 293;
export const HEADER_RULE_LEFT = 110;
export const HEADER_RULE_RIGHT = 969;

export const SeriesHeader: React.FC<{
  tone?: "ink" | "light";
  opacity?: number;
}> = ({ tone = "ink", opacity = 1 }) => {
  const isLight = tone === "light";
  return (
    <div style={{ position: "absolute", inset: 0, opacity, pointerEvents: "none" }}>
      {/* 实拍场景：页眉下方垫一层压暗底衬。
          否则背景偏亮的区段会把浅色细线吞掉，看起来像"断了一截"。 */}
      {isLight ? (
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 0,
            height: 400,
            background:
              "linear-gradient(180deg, rgba(12,10,8,0.68) 0%, rgba(12,10,8,0.46) 52%, rgba(12,10,8,0.14) 82%, rgba(12,10,8,0) 100%)",
          }}
        />
      ) : null}
      <div
        style={{
          position: "absolute",
          left: HEADER_RULE_LEFT,
          top: 223,
          fontFamily: FONT_SANS,
          fontSize: 27,
          lineHeight: 1.25,
          letterSpacing: 2.4,
          color: isLight ? "rgba(246,243,234,0.95)" : C.ink,
          textShadow: isLight ? "0 2px 10px rgba(0,0,0,0.6)" : "none",
          whiteSpace: "nowrap",
        }}
      >
        小散经济学 03
        <span style={{ opacity: 0.55, margin: "0 7px" }}>·</span>
        机会成本
      </div>
      <div
        style={{
          position: "absolute",
          left: HEADER_RULE_LEFT,
          top: HEADER_RULE_TOP,
          width: HEADER_RULE_RIGHT - HEADER_RULE_LEFT,
          height: 2,
          background: isLight ? "rgba(243,246,240,0.96)" : "rgb(70,83,79)",
          boxShadow: isLight ? "0 1px 5px rgba(0,0,0,0.55)" : "none",
        }}
      />
    </div>
  );
};

// 帧内本地进度（0..1）：场景内部动效一律用它，不用全局 frame
export const useLocal = (durationInFrames: number) => {
  const frame = useCurrentFrame();
  return {
    frame,
    t: Math.max(0, Math.min(1, frame / Math.max(1, durationInFrames))),
    at: (seconds: number) => frame - seconds * 30,
    prog: (startS: number, durS: number) =>
      Math.max(0, Math.min(1, (frame - startS * 30) / Math.max(1, durS * 30))),
  };
};
