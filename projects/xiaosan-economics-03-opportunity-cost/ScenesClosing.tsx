import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, interpolate, staticFile } from "remotion";
import { Annotation, PaperBase, Rule, SourceLine, useLocal } from "./Foundation";
import { C, FONT_SANS, FONT_SERIF, clamp01, easeSettle } from "./theme";

// ===========================================================================
// 18–22
// 18 真实排队 + 沙漏式计时条   19 确定性柱形比较
// 20 条款式边界条件            21 被补全的判断句
// 22 结尾追问 + 系列角标 + 原生合规页脚
// ===========================================================================

// --- sc18 免费的那杯咖啡，要你排两个小时 ------------------------------------
const QUEUE_RATE = 0.62;
const QUEUE_FREEZE_SCENE_S = 11.2;

export const FreeCoffeeQueue: React.FC<{ durationInFrames: number }> = () => {
  const { prog, frame } = useLocal(0);
  const frozen = frame >= QUEUE_FREEZE_SCENE_S * 30;
  const fadeToStill = prog(QUEUE_FREEZE_SCENE_S - 0.35, 0.5);
  const label = prog(4.3, 0.6);
  const priceZero = prog(6.7, 0.5);
  const timer = prog(8.23, 0.7);
  const fill = prog(8.23, 3.2);
  const strike = prog(10.84, 0.7);
  const close = prog(13.24, 0.8);
  return (
    <AbsoluteFill style={{ backgroundColor: "#191713" }}>
      <AbsoluteFill style={{ transform: `scale(${1.03 + 0.05 * prog(0, 16.4)})` }}>
        {!frozen ? (
          <OffthreadVideo
            src={staticFile("xiaosan-economics-03-opportunity-cost/video/sc18-queue-v1.mp4")}
            playbackRate={QUEUE_RATE}
            style={{ width: "100%", height: "100%", objectFit: "cover", opacity: 1 - fadeToStill }}
            muted
          />
        ) : null}
        <Img
          src={staticFile("xiaosan-economics-03-opportunity-cost/images/sc18-queue-last.png")}
          style={{
            position: "absolute",
            inset: 0,
            width: "100%",
            height: "100%",
            objectFit: "cover",
            opacity: frozen ? 1 : fadeToStill,
          }}
        />
      </AbsoluteFill>
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(18,16,13,0.72) 0%, rgba(18,16,13,0.16) 34%, rgba(18,16,13,0.20) 62%, rgba(18,16,13,0.80) 100%)",
        }}
      />
      {/* 上：免费的咖啡 */}
      <div style={{ position: "absolute", left: 110, right: 110, top: 372, opacity: label }}>
        <div style={{ fontFamily: FONT_SERIF, fontSize: 60, letterSpacing: 6, color: "#F4F1E8" }}>
          商场送的免费咖啡
        </div>
        <div
          style={{
            marginTop: 26,
            display: "flex",
            alignItems: "baseline",
            gap: 22,
            opacity: priceZero,
          }}
        >
          <div style={{ fontFamily: FONT_SERIF, fontSize: 96, letterSpacing: 4, color: "#F4F1E8" }}>
            ¥0
          </div>
          <div style={{ fontFamily: FONT_SANS, fontSize: 26, letterSpacing: 2, color: "rgba(244,241,232,0.7)" }}>
            价格确实是零
          </div>
        </div>
      </div>
      {/* 中：两小时的计时条 */}
      <div style={{ position: "absolute", left: 110, right: 110, top: 1030, opacity: timer }}>
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            fontFamily: FONT_SANS,
            fontSize: 24,
            letterSpacing: 3,
            color: "rgba(244,241,232,0.78)",
            marginBottom: 16,
          }}
        >
          <span>00:00</span>
          <span>02:00</span>
        </div>
        <div style={{ position: "relative", width: "100%", height: 12, background: "rgba(244,241,232,0.24)" }}>
          <div
            style={{
              width: `${fill * 100}%`,
              height: "100%",
              background: "#F4F1E8",
              opacity: 0.92,
            }}
          />
          <Annotation grow={strike} style={{ left: 0, right: 0, top: 0, height: 0, width: "auto" }} />
        </div>
        <div
          style={{
            marginTop: 24,
            fontFamily: FONT_SERIF,
            fontSize: 42,
            letterSpacing: 3,
            color: "#F4F1E8",
            opacity: strike,
          }}
        >
          那两个小时，不是免费的
        </div>
      </div>
      {/* 结论 */}
      <div
        style={{
          position: "absolute",
          left: 96,
          right: 96,
          top: 660,
          opacity: close,
          transform: `translateY(${(1 - easeSettle(close)) * 20}px)`,
        }}
      >
        <div
          style={{
            fontFamily: FONT_SERIF,
            fontSize: 96,
            letterSpacing: 8,
            color: "#F4F1E8",
            whiteSpace: "nowrap",
            textShadow: "0 4px 18px rgba(0,0,0,0.5)",
          }}
        >
          免费 <span style={{ color: "#D9644F" }}>≠</span> 没有成本
        </div>
      </div>
    </AbsoluteFill>
  );
};

// --- sc19 确定性柱形：A 3% / B 5% -------------------------------------------
export const ThreeVsFive: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const premise = prog(1.31, 0.7);
  const growA = prog(5.26, 0.8);
  const growB = prog(6.57, 0.8);
  const bracket = prog(8.07, 0.7);
  const BASE = 1230;
  const H = 460;
  const barW = 210;
  const bar = (p: number, x: number, pct: number, label: string, color: string, active: boolean) => (
    <div style={{ position: "absolute", left: x, top: BASE - H, width: barW, height: H }}>
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          width: barW,
          height: H * pct * easeSettle(p),
          background: color,
          opacity: active ? 0.94 : 0.5,
        }}
      />
      <div
        style={{
          position: "absolute",
          bottom: H * pct * easeSettle(p) + 22,
          width: barW,
          textAlign: "center",
          fontFamily: FONT_SERIF,
          fontSize: 74,
          letterSpacing: 2,
          color: C.ink,
          opacity: p,
        }}
      >
        {label}
      </div>
    </div>
  );
  return (
    <PaperBase tone="base">
      <SourceLine
        text="前提：风险、流动性与其他限制相当"
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 470,
          textAlign: "center",
          fontSize: 30,
          letterSpacing: 3,
          color: C.inkSoft,
          opacity: premise,
        }}
      />
      <div style={{ position: "absolute", left: 0, right: 0, top: 1252 }}>
        <div style={{ height: 3, background: C.ink, opacity: 0.45, marginLeft: 130, marginRight: 130 }} />
        <div style={{ display: "flex", justifyContent: "space-around", marginTop: 22 }}>
          <div style={{ fontFamily: FONT_SANS, fontSize: 26, letterSpacing: 4, color: C.inkSoft }}>A 选择</div>
          <div style={{ fontFamily: FONT_SANS, fontSize: 26, letterSpacing: 4, color: C.inkSoft }}>B 本来可以</div>
        </div>
      </div>
      {bar(growA, 210, 1, "+3%", C.teal, true)}
      {bar(growB, 620, 1, "+5%", C.inkFaint, false)}
      {/* 两个柱之间的追问 */}
      <div
        style={{
          position: "absolute",
          left: 210,
          top: BASE - H - 180,
          width: 620,
          opacity: bracket,
        }}
      >
        <div style={{ position: "relative", height: 60 }}>
          <div style={{ position: "absolute", left: 0, top: 30, width: 210, height: 2, background: C.ink, opacity: 0.4 }} />
          <div style={{ position: "absolute", left: 410, top: 30, width: 210, height: 2, background: C.ink, opacity: 0.4 }} />
          <div style={{ position: "absolute", left: 310, top: 0, fontFamily: FONT_SERIF, fontSize: 44, letterSpacing: 3, color: C.ink, whiteSpace: "nowrap" }}>
            放弃了什么？
          </div>
        </div>
      </div>
    </PaperBase>
  );
};

// --- sc20 条款式边界条件 ----------------------------------------------------
const TERMS = ["风险不同", "流动性不同", "确定性不同"];
export const BoundaryTerms: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const ans = prog(0.95, 0.6);
  const plain = prog(3.01, 0.6);
  const terms = prog(6.02, 0.7);
  const verdict = prog(8.64, 0.8);
  return (
    <PaperBase tone="base">
      <div style={{ position: "absolute", left: 130, right: 130, top: 470, opacity: ans }}>
        <div style={{ fontFamily: FONT_SERIF, fontSize: 46, letterSpacing: 4, color: C.inkSoft }}>
          你为了选 A，放弃的是
        </div>
        <div style={{ marginTop: 30, fontFamily: FONT_SERIF, fontSize: 120, letterSpacing: 6, color: C.ink }}>
          B 的 +5%
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          left: 130,
          top: 800,
          fontFamily: FONT_SERIF,
          fontSize: 38,
          letterSpacing: 3,
          color: C.inkFaint,
          opacity: plain,
        }}
      >
        但现实里的投资选择，不会这么简单
      </div>
      <Rule width="100%" color={C.ink} thickness={1} grow={terms} style={{ position: "absolute", left: 130, right: 130, top: 900, width: "auto", opacity: 0.3 }} />
      <div style={{ position: "absolute", left: 130, right: 130, top: 945, opacity: terms }}>
        {TERMS.map((t, i) => (
          <div
            key={t}
            style={{
              fontFamily: FONT_SERIF,
              fontSize: 44,
              letterSpacing: 6,
              color: C.ink,
              marginBottom: 22,
              opacity: clamp01((terms - i * 0.18) * 2),
            }}
          >
            {t}
          </div>
        ))}
      </div>
      <div
        style={{
          position: "absolute",
          left: 130,
          right: 130,
          top: 1195,
          opacity: verdict,
          transform: `translateY(${(1 - easeSettle(verdict)) * 18}px)`,
        }}
      >
        <div
          style={{
            fontFamily: FONT_SERIF,
            fontSize: 46,
            lineHeight: 1.4,
            letterSpacing: 3,
            color: C.ink,
            whiteSpace: "nowrap",
          }}
        >
          不能只拿最终收益率机械比较
        </div>
      </div>
      <SourceLine
        text="Fiveable, 1.1 Scarcity, choice, and opportunity cost"
        style={{ position: "absolute", left: 130, top: 1272, fontSize: 18, opacity: prog(9.4, 0.6) * 0.85 }}
      />
    </PaperBase>
  );
};

// --- sc21 判断句被补全 ------------------------------------------------------
export const CompleteTheJudgment: React.FC<{ durationInFrames: number }> = () => {
  const { prog } = useLocal(0);
  const rule = prog(0.09, 0.7);
  const line1 = prog(2.53, 0.6);
  const give = prog(3.65, 0.6);
  const gap = prog(5.2, 0.5);
  const complete = prog(6.66, 0.9);
  return (
    <PaperBase tone="base">
      <div style={{ position: "absolute", left: 130, right: 130, top: 620 }}>
        <Rule width={220} color={C.teal} thickness={3} grow={rule} style={{ opacity: 0.55 }} />
        <div
          style={{
            marginTop: 54,
            fontFamily: FONT_SERIF,
            fontSize: 66,
            lineHeight: 1.55,
            letterSpacing: 4,
            color: C.inkSoft,
            opacity: line1,
          }}
        >
          判断一个选择
        </div>
        <div
          style={{
            marginTop: 18,
            fontFamily: FONT_SERIF,
            fontSize: 66,
            lineHeight: 1.55,
            letterSpacing: 4,
            color: C.inkSoft,
            opacity: give,
          }}
        >
          不能只看它给了你什么
        </div>
        {/* 留白：等下一句补进来 */}
        <div style={{ height: gap * 150 }} />
        <div
          style={{
            opacity: complete,
            transform: `translateX(${(1 - easeSettle(complete)) * 80}px)`,
          }}
        >
          <div
            style={{
              fontFamily: FONT_SERIF,
              fontSize: 34,
              letterSpacing: 5,
              color: C.inkFaint,
              marginBottom: 14,
            }}
          >
            还要看
          </div>
          <div
            style={{
              fontFamily: FONT_SERIF,
              fontSize: 76,
              letterSpacing: 4,
              color: C.ink,
              whiteSpace: "nowrap",
            }}
          >
            为了它，你放弃了什么
          </div>
        </div>
      </div>
    </PaperBase>
  );
};

// --- sc22 结尾：只留一个追问 + 原生合规页脚 ---------------------------------
export const ClosingQuestion: React.FC<{
  durationInFrames: number;
  complianceText: string;
}> = ({ complianceText }) => {
  const { prog } = useLocal(0);
  const ask = prog(3.35, 0.8);
  const answer = prog(5.64, 0.9);
  const footer = prog(6.6, 0.9);
  return (
    <PaperBase tone="base">
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", paddingBottom: 300 }}>
        {/* 灰的那一问 */}
        <div
          style={{
            opacity: ask,
            transform: `translateY(${(1 - easeSettle(ask)) * 20}px)`,
            fontFamily: FONT_SERIF,
            fontSize: 96,
            letterSpacing: 6,
            color: C.inkFaint,
          }}
        >
          我要花多少钱？
        </div>
        {/* 补出来的第二问 */}
        <div
          style={{
            marginTop: 92,
            opacity: answer,
            transform: `translateY(${(1 - easeSettle(answer)) * 24}px)`,
            textAlign: "center",
          }}
        >
          <Rule width={360} color={C.ink} thickness={3} grow={answer} style={{ margin: "0 auto 42px", opacity: 0.45 }} />
          <div
            style={{
              fontFamily: FONT_SERIF,
              fontSize: 116,
              lineHeight: 1.35,
              letterSpacing: 9,
              color: C.ink,
            }}
          >
            为了它，
            <br />
            我放弃了什么？
          </div>
        </div>
      </AbsoluteFill>
      {/* 系列角标 + 原生合规页脚 */}
      <div
        style={{
          position: "absolute",
          left: 96,
          bottom: 660,
          opacity: footer,
          fontFamily: FONT_SANS,
          fontSize: 23,
          letterSpacing: 4,
          color: C.inkSoft,
        }}
      >
        小散经济学 03｜机会成本
      </div>
      <div
        style={{
          position: "absolute",
          left: 96,
          right: 96,
          bottom: 580,
          opacity: footer,
          fontFamily: FONT_SANS,
          fontSize: 22,
          lineHeight: 1.5,
          letterSpacing: 1,
          color: C.inkSoft,
        }}
      >
        {complianceText}
      </div>
    </PaperBase>
  );
};
