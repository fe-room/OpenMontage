import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { Annotation, PaperBase, Rule, Slip, SourceLine, useLocal } from "./Foundation";
import { C, FONT_SERIF, clamp01, easeSettle, seeded } from "./theme";
import { OptionCards, type CardState } from "./OptionCards";

// ===========================================================================
// 12–17
// 12 被翻掉的整屏   13 被划掉的算式 + 逐个熄灭
// 14 虚线误会卡     15 不给胜负的水平基准线
// 16 朱红批注卡     17 被划掉的等号 + 四片无价签的纸
// ===========================================================================

// --- sc12 问题立起来，再被一个最短的否定切断 --------------------------------
export const NotANegation: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const askIn = prog(6.9, 0.7);
  const wipe = prog(9.7, 0.5);
  const noIn = prog(9.85, 0.6);
  const labels = ["拍视频", "健身", "出去玩"];
  return (
    <PaperBase tone="base">
      <div style={{ opacity: 1 - wipe }}>
        <SourceLine
          text="特别容易搞错的地方"
          style={{ position: "absolute", left: 130, top: 560, fontSize: 30, letterSpacing: 3, opacity: prog(0.15, 0.6) * 0.9 }}
        />
        <div style={{ position: "absolute", left: 130, top: 700, display: "flex", gap: 26 }}>
          {labels.map((l, i) => {
            const p = prog(3.45 + i * 0.16, 0.5);
            return (
              <div
                key={l}
                style={{
                  width: 244,
                  height: 156,
                  background: C.paper,
                  border: `1px solid rgba(34,32,28,0.16)`,
                  boxShadow: "0 4px 12px rgba(34,32,28,0.09)",
                  transform: `rotate(${-0.7 + i * 0.6}deg) translateY(${(1 - easeSettle(p)) * 40}px)`,
                  opacity: p * 0.92,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontFamily: FONT_SERIF,
                  fontSize: 38,
                  letterSpacing: 3,
                  color: C.inkSoft,
                }}
              >
                {l}
              </div>
            );
          })}
        </div>
        {/* 求和的问题 */}
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 1000,
            textAlign: "center",
            opacity: askIn,
            transform: `translateY(${(1 - easeSettle(askIn)) * 24}px)`,
          }}
        >
          <div style={{ fontFamily: FONT_SERIF, fontSize: 136, letterSpacing: 10, color: C.ink }}>
            B + C + D
          </div>
          <div
            style={{
              marginTop: 18,
              fontFamily: FONT_SERIF,
              fontSize: 76,
              letterSpacing: 8,
              color: C.vermilion,
            }}
          >
            ＝ 机会成本 ？
          </div>
        </div>
      </div>
      {/* 最短的否定 */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: noIn }}>
        <div
          style={{
            fontFamily: FONT_SERIF,
            fontSize: 300,
            letterSpacing: 24,
            color: C.ink,
            transform: `scale(${0.94 + 0.06 * easeSettle(noIn)})`,
          }}
        >
          不是。
        </div>
      </AbsoluteFill>
    </PaperBase>
  );
};

// --- sc13 算式被划掉，卡片逐个熄灭 ------------------------------------------
const PULSE = seeded(991);
export const ExtinguishSum: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const equation = prog(0.3, 0.7);
  const tag = prog(5.7, 0.7);
  const mine = prog(8.07, 0.7);
  const kill = prog(11.74, 0.9);
  const remain = prog(14.33, 0.9);
  const last = prog(17.13, 0.7);
  const states: CardState[] = [
    { enter: 1, dim: 0.9 },
    { enter: 1, dim: 0.9, extinguish: kill },
    { enter: 1, dim: 0.9, extinguish: kill },
    { enter: 1, dim: 0.9, extinguish: kill },
  ];
  return (
    <PaperBase tone="base">
      {/* 印刷出来的算式 */}
      <div style={{ position: "absolute", left: 130, right: 130, top: 340, opacity: equation }}>
        <div
          style={{
            fontFamily: FONT_SERIF,
            fontSize: 62,
            letterSpacing: 5,
            color: C.inkSoft,
            display: "flex",
            alignItems: "center",
            gap: 16,
            whiteSpace: "nowrap",
          }}
        >
          <span>B</span>
          <span style={{ color: C.inkFaint }}>+</span>
          <span>C</span>
          <span style={{ color: C.inkFaint }}>+</span>
          <span>D</span>
          <span style={{ color: C.inkFaint }}>＝</span>
          <span>机会成本</span>
        </div>
        <Annotation grow={kill} style={{ left: -10, right: -10, top: "54%", height: 0, width: "auto" }} />
      </div>
      <div
        style={{
          position: "absolute",
          left: 130,
          top: 505,
          fontFamily: FONT_SERIF,
          fontSize: 32,
          letterSpacing: 3,
          color: C.vermilion,
          opacity: clamp01((kill - 0.5) * 2),
        }}
      >
        不能相加 —— 同一段时间只可能完成其中一件
      </div>
      <div
        style={{
          position: "absolute",
          left: 130,
          right: 130,
          top: 630,
          fontFamily: FONT_SERIF,
          fontSize: 48,
          lineHeight: 1.5,
          letterSpacing: 4,
          color: C.ink,
          opacity: tag,
          transform: `translateY(${(1 - tag) * 14}px)`,
        }}
      >
        关注的是：你放弃掉的最佳替代方案
      </div>
      <div
        style={{
          position: "absolute",
          left: 130,
          right: 130,
          top: 760,
          fontFamily: FONT_SERIF,
          fontSize: 38,
          letterSpacing: 3,
          color: C.inkSoft,
          opacity: mine,
        }}
      >
        选 A 真正付出的机会成本
      </div>
      <OptionCards states={states} />
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 1245,
          textAlign: "center",
          opacity: last * remain,
        }}
      >
        <div
          style={{
            fontFamily: FONT_SERIF,
            fontSize: 52,
            letterSpacing: 6,
            color: C.ink,
            transform: `translateY(${(1 - easeSettle(remain)) * 18}px)`,
          }}
        >
          只剩下最有价值的那个
        </div>
      </div>
    </PaperBase>
  );
};

// --- sc14 虚线误会卡 --------------------------------------------------------
export const MisreadCard: React.FC<{ durationInFrames: number }> = () => {
  const { prog, frame } = useLocal(0);
  const card = prog(0.3, 0.7);
  const stress = prog(6.36, 0.6);
  const wipe = prog(9.92, 0.45);
  const noIn = prog(10.05, 0.6);
  // 待纠正的轻微不安定：低频、固定相位，不是随机抖动
  const wob = stress > 0 && stress < 1 ? Math.sin(frame * 0.55) * 1.4 * stress : 0;
  return (
    <PaperBase tone="base">
      <div style={{ opacity: 1 - wipe }}>
        <SourceLine
          text="另一个误会"
          style={{ position: "absolute", left: 130, top: 580, fontSize: 30, letterSpacing: 3, opacity: prog(0.15, 0.6) * 0.85 }}
        />
        <div
          style={{
            position: "absolute",
            left: 150,
            top: 720,
            right: 150,
            padding: "64px 44px",
            border: `3px dashed rgba(182,58,43,${0.35 + 0.45 * stress})`,
            transform: `rotate(${wob}deg) translateY(${(1 - easeSettle(card)) * 30}px)`,
            opacity: card,
          }}
        >
          <div
            style={{
              fontFamily: FONT_SERIF,
              fontSize: 82,
              lineHeight: 1.5,
              letterSpacing: 4,
              color: C.ink,
              textAlign: "center",
            }}
          >
            休息 4 小时
            <br />＝ 亏 500 ？
          </div>
        </div>
      </div>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: noIn }}>
        <div
          style={{
            fontFamily: FONT_SERIF,
            fontSize: 250,
            letterSpacing: 20,
            color: C.ink,
            transform: `scale(${0.94 + 0.06 * easeSettle(noIn)})`,
          }}
        >
          也不是。
        </div>
      </AbsoluteFill>
    </PaperBase>
  );
};

// --- sc15 水平基准线：两端都不给胜负 ----------------------------------------
export const NoVerdictBalance: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const line = prog(0.25, 0.8);
  const above = prog(0.6, 0.7);
  const left = prog(1.5, 0.7);
  const right = prog(2.0, 0.7);
  const below = prog(2.74, 0.7);
  const below2 = prog(4.23, 0.7);
  const tilt = prog(5.92, 1.4);
  const balance = prog(12.65, 0.9);
  const L = 130;
  const R = 950;
  const Y = 1010;
  return (
    <PaperBase tone="base">
      <div
        style={{
          position: "absolute",
          left: L,
          top: Y,
          width: R - L,
          height: 3,
          background: C.teal,
          transform: `scaleX(${line})`,
          transformOrigin: "center",
          opacity: 0.72,
        }}
      />
      {/* 线上方：这条线只回答什么 */}
      <SourceLine
        text="机会成本只回答：你放弃了什么"
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: Y - 130,
          textAlign: "center",
          fontSize: 32,
          letterSpacing: 4,
          color: C.inkSoft,
          opacity: above,
        }}
      />
      {/* 左端纸片 */}
      <Slip
        rotate={-0.8}
        style={{
          left: L - 60,
          top: Y - 330,
          width: 320,
          height: 300,
          opacity: left * (1 - 0.06 * tilt),
          padding: "36px 26px",
        }}
      >
        <div style={{ fontFamily: FONT_SERIF, fontSize: 38, lineHeight: 1.5, letterSpacing: 2, color: C.ink }}>
          休息 4 小时的
          <br />
          恢复
        </div>
      </Slip>
      {/* 右端纸片 */}
      <Slip
        rotate={0.7}
        style={{
          left: R - 260,
          top: Y - 330,
          width: 320,
          height: 300,
          opacity: right * (1 - 0.06 * tilt),
          padding: "36px 26px",
        }}
      >
        <div style={{ fontFamily: FONT_SERIF, fontSize: 38, lineHeight: 1.5, letterSpacing: 2, color: C.ink }}>
          兼职净价值
          <br />
          约 500 元
        </div>
      </Slip>
      {/* 线下方：这条线不回答什么 */}
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: Y + 96,
          textAlign: "center",
          opacity: below,
        }}
      >
        <div style={{ fontFamily: FONT_SERIF, fontSize: 44, letterSpacing: 4, color: C.inkSoft }}>
          它并没有替你决定
        </div>
        <div
          style={{
            marginTop: 14,
            fontFamily: FONT_SERIF,
            fontSize: 54,
            letterSpacing: 4,
            color: C.ink,
            opacity: below2,
          }}
        >
          这个选择到底对不对
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: Y + 300,
          textAlign: "center",
          fontFamily: FONT_SERIF,
          fontSize: 46,
          letterSpacing: 6,
          color: C.ink,
          opacity: balance,
        }}
      >
        哪一边更重，只有你自己知道
      </div>
    </PaperBase>
  );
};

// --- sc16 朱红批注：有机会成本，不等于不应该做 -------------------------------
export const CostIsNotError: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const hero = prog(0.84, 0.8);
  const items = ["睡觉", "陪家人", "学习", "工作"];
  return (
    <PaperBase tone="base">
      <div style={{ position: "absolute", left: 110, right: 110, top: 520 }}>
        {/* 朱红批注：全片最重要的一句，也只在这里以批注形式出现 */}
        <div style={{ opacity: hero, transform: `translateY(${(1 - easeSettle(hero)) * 22}px)` }}>
          <Rule width="100%" color={C.vermilion} thickness={4} grow={hero} style={{ opacity: 0.85 }} />
          <div
            style={{
              marginTop: 40,
              fontFamily: FONT_SERIF,
              fontSize: 96,
              lineHeight: 1.45,
              letterSpacing: 5,
              color: C.ink,
            }}
          >
            有机会成本
            <span style={{ color: C.vermilion }}> ≠ </span>
            不应该做
          </div>
        </div>
      </div>
      {/* 排比四行：同一句式，同一语调 */}
      <div style={{ position: "absolute", left: 130, right: 130, top: 900, opacity: 1 - prog(9.26, 0.8) }}>
        {items.map((it, i) => {
          const p = prog(3.46 + i * 1.28, 0.5);
          return (
            <div
              key={it}
              style={{
                display: "flex",
                alignItems: "baseline",
                gap: 24,
                marginBottom: 26,
                opacity: p,
                transform: `translateX(${(1 - easeSettle(p)) * -16}px)`,
              }}
            >
              <div style={{ fontFamily: FONT_SERIF, fontSize: 50, letterSpacing: 4, color: C.ink }}>
                {it}
              </div>
              <div style={{ fontFamily: FONT_SERIF, fontSize: 30, letterSpacing: 3, color: C.inkFaint }}>
                · 有机会成本
              </div>
            </div>
          );
        })}
      </div>
      <div
        style={{
          position: "absolute",
          left: 130,
          right: 130,
          top: 1030,
          textAlign: "center",
          fontFamily: FONT_SERIF,
          fontSize: 52,
          letterSpacing: 5,
          color: C.ink,
          opacity: prog(9.26, 0.8),
        }}
      >
        只要在做选择，就一定有东西被放弃
      </div>
    </PaperBase>
  );
};

// --- sc17 被划掉的等号：成本不必货币化 --------------------------------------
const SHAPES = [
  { w: 236, h: 156, rot: -0.8 }, // 收入
  { w: 304, h: 122, rot: 0.7 },  // 时间
  { w: 196, h: 196, rot: -0.5 }, // 精力
  { w: 340, h: 132, rot: 0.9 },  // 陪伴 / 休息 / 学习机会
];
const NAMES = ["收入", "时间", "精力", "陪伴 · 休息 · 学习机会"];
export const StrikeTheEquals: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const eq = prog(0.3, 0.7);
  const kill = prog(2.4, 0.8);
  const wide = prog(14.83, 0.8);
  let x = 130;
  return (
    <PaperBase tone="base">
      {/* 印刷出来的等号 */}
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 470,
          textAlign: "center",
          fontFamily: FONT_SERIF,
          fontSize: 170,
          letterSpacing: 20,
          color: C.inkSoft,
          opacity: eq * (1 - 0.25 * kill),
        }}
      >
        ═
      </div>
      <Annotation grow={kill} style={{ left: 300, right: 300, top: 560, height: 0, width: "auto" }} />
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 640,
          textAlign: "center",
          fontFamily: FONT_SERIF,
          fontSize: 34,
          letterSpacing: 3,
          color: C.vermilion,
          opacity: clamp01((kill - 0.5) * 2),
        }}
      >
        不是所有东西都必须换算成钱
      </div>
      {/* 四片形状不同的纸，都没有价签 */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: 1920 }}>
        {SHAPES.map((sh, i) => {
          const p = prog(4.8 + i * 2.2, 0.7);
          const row = i < 2 ? 0 : 1;
          const widths = [[200, 250], [165, 290]][row];
          const rowW = widths[0] + 26 + widths[1];
          const x0 = (1080 - rowW) / 2;
          const left = i % 2 === 0 ? x0 : x0 + widths[0] + 26;
          const top = row === 0 ? 900 : 1085;
          return (
            <div
              key={NAMES[i]}
              style={{
                position: "absolute",
                left,
                top,
                width: widths[i % 2],
                height: row === 0 ? 150 : 140,
                background: C.paper,
                border: `1px solid rgba(34,32,28,0.16)`,
                boxShadow: "0 5px 14px rgba(34,32,28,0.10)",
                transform: `rotate(${sh.rot}deg) translateY(${(1 - easeSettle(p)) * 46}px)`,
                opacity: p,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                padding: "0 12px",
                textAlign: "center",
                fontFamily: FONT_SERIF,
                fontSize: 28,
                lineHeight: 1.35,
                letterSpacing: 2,
                color: C.ink,
              }}
            >
              {NAMES[i]}
            </div>
          );
        })}
      </div>
      <div
        style={{
          position: "absolute",
          left: 130,
          right: 130,
          top: 1258,
          textAlign: "center",
          opacity: wide,
        }}
      >
        <div style={{ fontFamily: FONT_SERIF, fontSize: 50, letterSpacing: 5, color: C.ink, whiteSpace: "nowrap" }}>
          比「花了多少钱」宽得多
        </div>
      </div>
    </PaperBase>
  );
};
