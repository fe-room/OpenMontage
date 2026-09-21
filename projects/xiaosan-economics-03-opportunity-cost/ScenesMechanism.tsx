import React from "react";
import {
  AbsoluteFill,
  OffthreadVideo,
  interpolate,
  staticFile,
} from "remotion";
import { Annotation, PaperBase, Rule, SourceLine, useLocal } from "./Foundation";
import { C, FONT_SANS, FONT_SERIF, clamp01, easeSettle } from "./theme";
import { OptionCards, type CardState } from "./OptionCards";

// ===========================================================================
// 06–11
// 06 几乎空白的纸面，一行约束   07 四张纸卡落纸
// 08 沙漏时间柱 + 互斥约束      09 逐字打出的追问
// 10 一张卡被点亮并命名         11 定义卡整屏静止
// ===========================================================================

// --- sc06 只有一行，其余都是空白 -------------------------------------------
export const FourHoursTitle: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const rule = prog(0.2, 0.7);
  const small = prog(0.7, 0.5);
  const hero = prog(1.15, 0.85);
  return (
    <PaperBase tone="base">
      <div style={{ position: "absolute", left: 130, right: 130, top: 560 }}>
        <Rule width={240} color={C.ink} thickness={3} grow={rule} style={{ opacity: 0.5 }} />
        <div
          style={{
            marginTop: 42,
            fontFamily: FONT_SERIF,
            fontSize: 46,
            letterSpacing: 8,
            color: C.inkSoft,
            opacity: small,
          }}
        >
          周六下午
        </div>
        <div
          style={{
            marginTop: 12,
            fontFamily: FONT_SERIF,
            fontSize: 196,
            letterSpacing: 12,
            color: C.ink,
            opacity: hero,
            transform: `translateY(${interpolate(easeSettle(hero), [0, 1], [26, 0])}px)`,
          }}
        >
          4 小时
        </div>
      </div>
    </PaperBase>
  );
};

// --- sc07 四张纸卡落纸，然后被一条朱红横线约束 ------------------------------
export const OptionCardsIn: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const at = [0.2, 0.75, 1.44, 2.81];
  const states: CardState[] = at.map((a) => ({ enter: prog(a, 0.55) }));
  const slash = prog(3.79, 0.8);
  return (
    <PaperBase tone="base">
      <div
        style={{
          position: "absolute",
          left: 130,
          top: 620,
          fontFamily: FONT_SERIF,
          fontSize: 40,
          letterSpacing: 6,
          color: C.inkFaint,
          opacity: prog(0.05, 0.5),
        }}
      >
        这 4 个小时，你能同时做几件事？
      </div>
      <OptionCards states={states} />
      {/* 互斥约束：朱红横线一次划过四张卡 */}
      <Annotation
        grow={slash}
        style={{ left: 90, right: 90, top: 1236, height: 0, width: "auto" }}
      />
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 1258,
          textAlign: "center",
          fontFamily: FONT_SERIF,
          fontSize: 42,
          letterSpacing: 4,
          color: C.vermilion,
          opacity: clamp01((slash - 0.55) * 2.2),
        }}
      >
        只能真正使用一次
      </div>
    </PaperBase>
  );
};

// --- sc08 沙漏时间柱 + 互斥后的选择 -----------------------------------------
export const MutualExclusion: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  // 首尾按住上一场的姿态，避免切场跳变
  const states: CardState[] = [
    { enter: 1, lift: 30 * prog(0.78, 0.6), selected: true },
    { enter: 1, dim: 0.85 * prog(0.78, 0.6) },
    { enter: 1, dim: 0.85 * prog(0.78, 0.6) },
    { enter: 1, dim: 0.85 * prog(0.78, 0.6) },
  ];
  const stamp = prog(3.72, 0.5);
  return (
    <PaperBase tone="base">
      {/* 时间柱：真实沙漏素材被收进一条纸边竖栏 */}
      <div
        style={{
          position: "absolute",
          left: 110,
          top: 348,
          width: 236,
          height: 556,
          border: `1px solid rgba(34,32,28,0.22)`,
          boxShadow: "0 8px 22px rgba(34,32,28,0.14)",
          overflow: "hidden",
          transform: "rotate(-0.6deg)",
          opacity: prog(0.15, 0.8),
        }}
      >
        <OffthreadVideo
          src={staticFile("xiaosan-economics-03-opportunity-cost/video/sc08-hourglass-v1.mp4")}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
          muted
        />
      </div>
      <SourceLine
        text={"砂 只 往 下 落"}
        style={{ position: "absolute", left: 110, top: 936, fontSize: 23, letterSpacing: 8, opacity: prog(0.9, 0.7) }}
      />
      <div
        style={{
          position: "absolute",
          left: 400,
          right: 130,
          top: 560,
          fontFamily: FONT_SERIF,
          fontSize: 52,
          lineHeight: 1.5,
          letterSpacing: 5,
          color: C.inkSoft,
          opacity: prog(0.1, 0.7),
        }}
      >
        你选了其中一个
      </div>
      <OptionCards states={states} />
      {/* 0 元标记：落在左下，像盖章 */}
      <div
        style={{
          position: "absolute",
          left: 130,
          top: 1180,
          padding: "18px 24px",
          border: `2px solid ${C.vermilion}`,
          color: C.vermilion,
          fontFamily: FONT_SERIF,
          fontSize: 44,
          letterSpacing: 3,
          transform: `rotate(-1.4deg) scale(${0.86 + 0.14 * easeSettle(stamp)})`,
          opacity: stamp * 0.94,
        }}
      >
        银行卡支出 0 元
      </div>
    </PaperBase>
  );
};

// --- sc09 逐字打出的追问 ----------------------------------------------------
const TYPED = "你最可能去做的那件事是什么？";
export const AskTheOneThing: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const shown = Math.floor(clamp01(prog(3.08, 2.0)) * TYPED.length);
  const cursor = prog(3.0, 2.2) < 1;
  return (
    <PaperBase tone="base">
      <div
        style={{
          position: "absolute",
          left: 130,
          right: 130,
          top: 760,
        }}
      >
        <Rule width={180} color={C.teal} thickness={3} grow={prog(0.2, 0.8)} style={{ opacity: 0.5 }} />
        <div
          style={{
            marginTop: 48,
            fontFamily: FONT_SERIF,
            fontSize: 96,
            lineHeight: 1.55,
            letterSpacing: 4,
            color: C.ink,
            minHeight: 300,
          }}
        >
          {TYPED.slice(0, shown)}
          <span style={{ opacity: cursor ? 1 : 0, color: C.vermilion }}>|</span>
        </div>
      </div>
      <SourceLine
        text="不是「花了多少钱」，而是「本来还能做什么」"
        style={{ position: "absolute", left: 130, top: 1180, fontSize: 27, letterSpacing: 2, opacity: prog(2.4, 0.8) * 0.85 }}
      />
    </PaperBase>
  );
};

// --- sc10 把被放弃的那一张点亮并命名 ----------------------------------------
export const NameTheOpportunityCost: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const highlight = prog(0.52, 0.7);
  const tag = prog(3.42, 0.6);
  const value = prog(5.24, 0.6);
  const word = prog(8.0, 1.0);
  const states: CardState[] = [
    { enter: 1, dim: 0.9, lift: 26 },
    { enter: 1, dim: 0.9 },
    { enter: 1, lift: 78 * easeSettle(highlight), selected: true, tag: "最佳被放弃方案", tagProgress: tag, value: "净价值约 500 元", valueProgress: value },
    { enter: 1, dim: 0.9 },
  ];
  const recede = prog(7.4, 0.9);
  return (
    <PaperBase tone="base">
      <div style={{ opacity: 1 - recede }}>
        <OptionCards states={states} />
      </div>
      {/* 命名：整屏只剩一个词 */}
      <AbsoluteFill
        style={{
          alignItems: "center",
          justifyContent: "center",
          opacity: recede,
          transform: `scale(${0.92 + 0.08 * easeSettle(word)})`,
        }}
      >
        <div
          style={{
            fontFamily: FONT_SERIF,
            fontSize: 186,
            letterSpacing: 16,
            color: C.ink,
          }}
        >
          机会成本
        </div>
      </AbsoluteFill>
    </PaperBase>
  );
};

// --- sc11 定义卡：全片唯一一次让画面完全静止 --------------------------------
export const DefinitionCard: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const neq = prog(0.78, 0.6);
  const eq = prog(4.95, 0.7);
  const src = prog(5.9, 0.7);
  return (
    <PaperBase tone="base">
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", padding: "0 110px" }}>
        <div
          style={{
            fontFamily: FONT_SERIF,
            fontSize: 92,
            letterSpacing: 10,
            color: C.ink,
            opacity: 0.35 + 0.65 * prog(0, 0.7),
          }}
        >
          机会成本
        </div>
        <div style={{ marginTop: 96, width: "100%" }}>
          <div
            style={{
              display: "flex",
              alignItems: "baseline",
              gap: 26,
              opacity: neq,
              transform: `translateY(${(1 - neq) * 14}px)`,
            }}
          >
            <div style={{ fontFamily: FONT_SERIF, fontSize: 54, width: 62, color: C.vermilion }}>≠</div>
            <div style={{ fontFamily: FONT_SERIF, fontSize: 52, letterSpacing: 3, color: C.inkSoft }}>
              你花出去的钱
            </div>
          </div>
          <Rule width="100%" color={C.ink} thickness={1} grow={neq} style={{ margin: "48px 0", opacity: 0.22 }} />
          <div
            style={{
              display: "flex",
              alignItems: "baseline",
              gap: 26,
              opacity: eq,
              transform: `translateY(${(1 - eq) * 14}px)`,
            }}
          >
            <div style={{ fontFamily: FONT_SERIF, fontSize: 54, width: 62, color: C.teal }}>=</div>
            <div
              style={{
                fontFamily: FONT_SERIF,
                fontSize: 56,
                lineHeight: 1.5,
                letterSpacing: 3,
                color: C.ink,
              }}
            >
              为了当前选择，而放弃的
              <br />
              最佳替代方案的价值
            </div>
          </div>
        </div>
        <SourceLine
          text="Federal Reserve Bank of St. Louis, 2020-01 ｜ N. G. Mankiw, Principles of Microeconomics, Ch.1"
          style={{ position: "absolute", left: 110, right: 110, bottom: 430, fontSize: 20, opacity: src * 0.9 }}
        />
      </AbsoluteFill>
    </PaperBase>
  );
};
