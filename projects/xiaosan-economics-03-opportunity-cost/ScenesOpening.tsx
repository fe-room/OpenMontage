import React from "react";
import { AbsoluteFill, OffthreadVideo, interpolate, staticFile } from "remotion";
import { Annotation, PaperBase, Rule, SourceLine, useLocal } from "./Foundation";
import { C, FONT_SERIF, clamp01, easeSettle } from "./theme";

// ===========================================================================
// 01–05
// 每场的首要视觉主体都不同：实拍 / 巨字 / 印刷账簿 / 被划掉的词 / 分叉问句
// ===========================================================================

// --- sc01 真实躺卧：第一帧就要有文字和主题 -------------------------------
export const RealLieIn: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const push = 1.03 + 0.05 * prog(0, 2.7);
  // 第二行在第 0 帧就已可见（保证首帧内容量），随朗读升到满不透明
  const line2 = 0.62 + 0.38 * prog(1.45, 0.4);
  return (
    <AbsoluteFill style={{ backgroundColor: "#16130F" }}>
      <AbsoluteFill style={{ transform: `scale(${push})` }}>
        <OffthreadVideo
          src={staticFile("xiaosan-economics-03-opportunity-cost/video/sc01-lie-in-v1.mp4")}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
          muted
        />
      </AbsoluteFill>
      {/* 上暗下暗：给页眉与纸面板让出对比度，同时不压死画面中部 */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(18,16,13,0.34) 0%, rgba(18,16,13,0.06) 32%, rgba(18,16,13,0.10) 62%, rgba(18,16,13,0.52) 100%)",
        }}
      />
      <AbsoluteFill style={{ border: `2px solid rgba(244,241,232,0.34)`, margin: 44 }} />
      {/* 主标题纸面板：第 0 帧起完整可见 */}
      <div
        style={{
          position: "absolute",
          left: 96,
          right: 96,
          top: 344,
          padding: "42px 46px 46px",
          background: "rgba(246,243,235,0.97)",
          border: "1px solid rgba(34,32,28,0.20)",
          boxShadow: "0 18px 44px rgba(0,0,0,0.42)",
          transform: "rotate(-0.5deg)",
        }}
      >
        <Rule width={132} color={C.ink} thickness={3} style={{ opacity: 0.5, marginBottom: 28 }} />
        <div
          style={{
            fontFamily: FONT_SERIF,
            fontSize: 54,
            lineHeight: 1.46,
            letterSpacing: 2,
            color: C.ink,
            whiteSpace: "nowrap",
          }}
        >
          周末躺一天，一分钱没花
        </div>
        <div
          style={{
            marginTop: 10,
            fontFamily: FONT_SERIF,
            fontSize: 54,
            lineHeight: 1.46,
            letterSpacing: 2,
            color: C.ink,
            opacity: line2,
            whiteSpace: "nowrap",
          }}
        >
          这一天的成本，是 0
          <span style={{ color: C.vermilion, marginLeft: 6 }}>？</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// --- sc02 巨字：把冲突压成两屏 ---------------------------------------------
export const CostZeroHero: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const zeroOut = prog(0.32, 0.34);
  const hero = prog(0.42, 0.72);
  const settle = easeSettle(hero);
  return (
    <PaperBase tone="base">
      {/* 第一屏：0 元 */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", opacity: 1 - zeroOut }}>
        <div
          style={{
            fontFamily: FONT_SERIF,
            fontSize: 250,
            letterSpacing: 10,
            color: C.ink,
            transform: `scale(${1 - 0.16 * zeroOut})`,
          }}
        >
          0<span style={{ fontSize: 120, letterSpacing: 0, marginLeft: 20 }}>元</span>
        </div>
      </AbsoluteFill>
      {/* 第二屏：成本 = 0 ？ */}
      <AbsoluteFill
        style={{
          alignItems: "center",
          justifyContent: "center",
          opacity: hero,
          transform: `scale(${0.9 + 0.1 * settle})`,
        }}
      >
        <div
          style={{
            fontFamily: FONT_SERIF,
            fontSize: 168,
            lineHeight: 1.12,
            letterSpacing: 6,
            color: C.ink,
            textAlign: "center",
          }}
        >
          成本 = 0
          <span style={{ color: C.vermilion, marginLeft: 14 }}>？</span>
        </div>
        <Rule width={520} color={C.ink} thickness={3} grow={clamp01((hero - 0.5) * 2)} style={{ marginTop: 34, opacity: 0.5 }} />
      </AbsoluteFill>
    </PaperBase>
  );
};

// --- sc03 印刷账簿：四行 0 元一笔笔落下 -------------------------------------
const LEDGER = [
  { label: "买东西", at: 3.74 },
  { label: "打车", at: 4.53 },
  { label: "出去吃饭", at: 5.12 },
  { label: "银行卡", at: 6.11 },
];

export const ZeroLedger: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const conclusion = prog(7.88, 0.5);
  return (
    <PaperBase tone="base">
      <div style={{ position: "absolute", left: 130, right: 130, top: 356 }}>
        <SourceLine
          text="按我们平时理解「成本」的方式"
          style={{ position: "relative", fontSize: 30, color: C.inkSoft, opacity: prog(0.15, 0.5) }}
        />
        <Rule
          width="100%"
          color={C.ink}
          thickness={2}
          grow={prog(0.5, 0.7)}
          style={{ marginTop: 22, opacity: 0.55 }}
        />
        {/* 账簿主体 */}
        <div style={{ marginTop: 54 }}>
          {LEDGER.map((row, i) => {
            const p = prog(row.at, 0.42);
            const y = 26 * (1 - easeSettle(p));
            return (
              <div
                key={row.label}
                style={{
                  display: "flex",
                  alignItems: "baseline",
                  justifyContent: "space-between",
                  padding: "30px 6px",
                  borderBottom: `1px solid rgba(34,32,28,${0.14 * p})`,
                  opacity: p,
                  transform: `translateY(${y}px)`,
                }}
              >
                <div
                  style={{
                    fontFamily: FONT_SERIF,
                    fontSize: 56,
                    letterSpacing: 3,
                    color: C.inkSoft,
                    fontWeight: 400,
                  }}
                >
                  {row.label}
                </div>
                <div
                  style={{
                    fontFamily: FONT_SERIF,
                    fontSize: 62,
                    letterSpacing: 1,
                    color: C.ink,
                    opacity: 0.92,
                  }}
                >
                  0<span style={{ fontSize: 30, marginLeft: 8 }}>元</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
      {/* 结论：观众的直觉落点 */}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-end" }}>
        <div
          style={{
            marginBottom: 640,
            opacity: conclusion,
            transform: `translateY(${interpolate(conclusion, [0, 1], [22, 0])}px)`,
            textAlign: "center",
          }}
        >
          <Rule width={300} color={C.ink} thickness={3} grow={conclusion} style={{ margin: "0 auto 26px", opacity: 0.45 }} />
          <div
            style={{
              fontFamily: FONT_SERIF,
              fontSize: 132,
              letterSpacing: 8,
              color: C.ink,
            }}
          >
            0 成本
          </div>
        </div>
      </AbsoluteFill>
    </PaperBase>
  );
};

// --- sc04 划掉的词：一次朱红批注完成第一反转 --------------------------------
export const StrikeTheSpend: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const strike = prog(1.37, 0.55);
  const after = prog(2.6, 0.6);
  return (
    <PaperBase tone="base">
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
        <div style={{ position: "relative", padding: "0 40px" }}>
          <div
            style={{
              fontFamily: FONT_SERIF,
              fontSize: 104,
              letterSpacing: 6,
              color: C.inkSoft,
              opacity: 0.5 + 0.5 * (1 - strike),
            }}
          >
            花了多少钱
          </div>
          {/* 朱红横线：跟朗读节奏一起划过 */}
          <Annotation
            grow={strike}
            style={{ left: -14, right: -14, top: "52%", height: 0, width: "auto" }}
          />
        </div>
        {/* 划掉之后，真正被追问的东西才出现 */}
        <div
          style={{
            marginTop: 96,
            opacity: after,
            transform: `translateY(${interpolate(after, [0, 1], [18, 0])}px)`,
            textAlign: "center",
          }}
        >
          <div
            style={{
              fontFamily: FONT_SERIF,
              fontSize: 176,
              letterSpacing: 10,
              color: C.ink,
            }}
          >
            成本
          </div>
          <SourceLine
            text="不只看这个"
            style={{ position: "relative", textAlign: "center", marginTop: 20, fontSize: 32, letterSpacing: 6, opacity: 0.75 }}
          />
        </div>
      </AbsoluteFill>
    </PaperBase>
  );
};

// --- sc05 分叉问句：一个问句 + 四条引线指向四个空纸位 ------------------------
export const QuestionFork: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const q = prog(1.35, 0.7);
  const fork = prog(1.9, 0.9);
  const slots = prog(2.5, 1.0);
  const X = [230, 450, 650, 850];
  return (
    <PaperBase tone="base">
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", paddingBottom: 420 }}>
        <div
          style={{
            opacity: q,
            transform: `translateY(${interpolate(q, [0, 1], [26, 0])}px)`,
            textAlign: "center",
            padding: "0 120px",
          }}
        >
          <div
            style={{
              fontFamily: FONT_SERIF,
              fontSize: 92,
              lineHeight: 1.5,
              letterSpacing: 4,
              color: C.ink,
            }}
          >
            这一天，你本来还能
            <br />
            拿去干什么？
          </div>
        </div>
      </AbsoluteFill>
      {/* 四条深青引线，落到四个尚未填写的空纸位 */}
      <AbsoluteFill>
        {X.map((x, i) => (
          <div
            key={x}
            style={{
              position: "absolute",
              left: x,
              top: 980,
              width: 1,
              height: 168 * easeSettle(clamp01((fork - i * 0.12) / 0.6)),
              background: C.teal,
              opacity: 0.55,
            }}
          />
        ))}
        {X.map((x) => (
          <div
            key={`s${x}`}
            style={{
              position: "absolute",
              left: x - 86,
              top: 1148,
              width: 172,
              height: 186,
              border: `1px dashed rgba(46,91,90,0.6)`,
              background: "rgba(244,241,232,0.5)",
              opacity: slots * 0.9,
            }}
          />
        ))}
      </AbsoluteFill>
    </PaperBase>
  );
};
