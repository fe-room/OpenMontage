import React from "react";
import { C, FONT_MONO, FONT_SANS, easeSettle } from "./theme";
import { InvertTag, Kicker, Panel, Plate, Rule, land, useLocal } from "./Foundation";
import { CAST, FUNDS, INITIAL_ASSET, OPENING, RULES } from "./timeline";

const yuan = (n: number) => Math.round(n).toLocaleString("en-US");

// ---------------------------------------------------------------------------
// sc01 开场提问 —— 4.6 秒内建立"同一天、同一笔钱、同一终点"的可比前提
// 首帧即完整在场（不做淡入）：平台取第 0 帧做内容质量判定。
// ---------------------------------------------------------------------------
export const Opening: React.FC = () => {
  const { sec } = useLocal(138);

  // 第 0 帧必须已经带着这支片子的前提：标题、两行铺垫与主句都在场。
  // 因此基础不透明度不为 0，动效只做"轻微上移 + 升到 1.0"。
  const l1 = 1;
  const l2 = 0.78 + 0.22 * easeSettle(sec / 0.5);
  const hero = 0.62 + 0.38 * easeSettle(sec / 0.7);
  const ruleGrow = 0.72 + 0.28 * easeSettle(sec / 0.45);

  const line = (text: string, top: number, op: number, size: number) => (
    <div
      style={{
        position: "absolute",
        left: 96,
        top,
        fontFamily: FONT_SANS,
        fontSize: size,
        lineHeight: 1.3,
        color: C.ink,
        whiteSpace: "nowrap",
        opacity: op,
        transform: `translateY(${(1 - op) * 14}px)`,
      }}
    >
      {text}
    </div>
  );

  return (
    <Plate>
      <Rule width={888} color={C.ink} thickness={3} grow={ruleGrow} style={{ position: "absolute", left: 96, top: 372 }} />
      <Kicker style={{ left: 96, top: 408, opacity: 1 }} size={26} color={C.inkSoft}>
        {OPENING.overline}
      </Kicker>

      {line(OPENING.lines[0], 528, l1, 58)}
      {line(OPENING.lines[1], 616, l2, 58)}

      <div style={{ position: "absolute", left: 96, top: 768, width: 888, height: 2, background: C.grid }} />

      <div
        style={{
          position: "absolute",
          left: 96,
          top: 848,
          fontFamily: FONT_SANS,
          fontSize: 104,
          lineHeight: 1.2,
          fontWeight: 500,
          color: C.ink,
          whiteSpace: "nowrap",
          opacity: hero,
          transform: `translateY(${(1 - hero) * 16}px)`,
        }}
      >
        {OPENING.hero}
      </div>

      <Kicker style={{ left: 96, top: 1032, opacity: 0.55 + 0.45 * easeSettle((sec - 0.9) / 0.6) }} size={24}>
        四只都是场内 ETF　·　同一天买入　·　之后什么都不做
      </Kicker>
    </Plate>
  );
};

// ---------------------------------------------------------------------------
// sc02 四只身份牌 —— 让观众在曲线出现前认识四条线的身份
// ---------------------------------------------------------------------------
export const Cast: React.FC = () => {
  const { sec } = useLocal(144);
  const head = land(sec, 0, 0.1, 0.5);

  return (
    <Plate>
      <Kicker style={{ left: 96, top: 190, opacity: head }} size={26} color={C.inkSoft}>
        同为 {yuan(INITIAL_ASSET)} 起点
      </Kicker>
      <div
        style={{
          position: "absolute", left: 96, top: 236, fontFamily: FONT_SANS,
          fontSize: 46, fontWeight: 500, color: C.ink, whiteSpace: "nowrap", opacity: head,
        }}
      >
        四只 ETF，各买 10 万
      </div>

      {FUNDS.map((f, i) => {
        const p = land(sec, 0.45 + i * 0.32, 0.12, 0.5);
        const top = 400 + i * 186;
        return (
          <Panel
            key={f.code}
            style={{
              left: 96,
              top,
              width: 888,
              height: 152,
              opacity: p,
              transform: `translateY(${(1 - p) * 18}px)`,
            }}
          >
            <div style={{ position: "absolute", left: 0, top: 0, width: 8, height: 152, background: f.color }} />
            <div style={{ position: "absolute", left: 36, top: 34, fontFamily: FONT_SANS, fontSize: 42, color: C.ink }}>
              {f.name}
            </div>
            <div style={{ position: "absolute", left: 36, top: 96, fontFamily: FONT_MONO, fontSize: 26, color: C.inkFaint }}>
              {f.code}
            </div>
            <div
              style={{
                position: "absolute", right: 32, top: 46, fontFamily: FONT_SANS,
                fontSize: 26, color: f.color, textAlign: "right",
              }}
            >
              {f.category}
            </div>
            <div style={{ position: "absolute", right: 32, top: 96, fontFamily: FONT_MONO, fontSize: 28, color: C.inkSoft, textAlign: "right" }}>
              ¥{yuan(INITIAL_ASSET)}
            </div>
          </Panel>
        );
      })}

      <Kicker style={{ left: 96, top: 1200, opacity: land(sec, 1.9, 0.1, 0.5) }} size={24}>
        {CAST.foot}
      </Kicker>
    </Plate>
  );
};

// ---------------------------------------------------------------------------
// sc03 规则公布 —— 口径前置：把"分红按再投资处理"说在曲线之前
// ---------------------------------------------------------------------------
export const Rules: React.FC = () => {
  const { sec } = useLocal(114);
  const head = land(sec, 0, 0.1, 0.5);
  const startP = easeSettle((sec - 2.35) / 0.55);

  return (
    <Plate>
      <Rule width={888} color={C.grid} thickness={2} style={{ position: "absolute", left: 96, top: 330 }} />
      <div
        style={{
          position: "absolute", left: 96, top: 240, fontFamily: FONT_SANS,
          fontSize: 44, fontWeight: 500, color: C.ink, whiteSpace: "nowrap", opacity: head,
        }}
      >
        {RULES.head}
      </div>

      {RULES.rows.map((r, i) => {
        const p = land(sec, 0.42 + i * 0.26, 0.1, 0.46);
        const top = 400 + i * 112;
        return (
          <div key={r.k} style={{ position: "absolute", inset: 0, opacity: p, transform: `translateY(${(1 - p) * 12}px)` }}>
            <div style={{ position: "absolute", left: 96, top: top + 8, width: 6, height: 34, background: C.rule }} />
            <div
              style={{
                position: "absolute", left: 126, top: top + 6, fontFamily: FONT_SANS,
                fontSize: 27, color: C.inkFaint, whiteSpace: "nowrap",
              }}
            >
              {r.k}
            </div>
            <div
              style={{
                position: "absolute", left: 330, top: top, fontFamily: FONT_SANS,
                fontSize: 38, color: C.ink, whiteSpace: "nowrap",
              }}
            >
              {r.v}
            </div>
          </div>
        );
      })}

      <div
        style={{
          position: "absolute", left: 96, top: 872, width: 888, fontFamily: FONT_SANS,
          fontSize: 23, lineHeight: 1.5, color: C.inkFaint,
          opacity: land(sec, 1.5, 0.1, 0.5),
        }}
      >
        这是把分红按再投资处理后的总回报口径，不等于账户里收到的现金分红会自动复投
      </div>

      <div style={{ position: "absolute", left: 96, top: 1010, opacity: startP, transform: `translateY(${(1 - startP) * 10}px)` }}>
        <InvertTag style={{ left: 0, top: 0, padding: "12px 30px 16px", fontSize: 68, fontWeight: 500, letterSpacing: 4 }}>
          START
        </InvertTag>
      </div>
      <Kicker style={{ left: 400, top: 1058, opacity: startP }} size={24} color={C.inkSoft}>
        四条线从同一个原点出发
      </Kicker>
    </Plate>
  );
};
