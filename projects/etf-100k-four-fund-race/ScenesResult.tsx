import React from "react";
import { C, FONT_MONO, FONT_SANS, easeSettle } from "./theme";
import { InvertTag, Kicker, Panel, Plate, Rule, land, useLocal } from "./Foundation";
import { FUNDS, RESULT, TURN } from "./timeline";

// ---------------------------------------------------------------------------
// sc05 冻结最终结果 —— 先让观众记住结果，再拆过程
// ---------------------------------------------------------------------------
export const Result: React.FC = () => {
  const { sec } = useLocal(192);
  const head = land(sec, 0, 0.1, 0.5);

  return (
    <Plate>
      <Kicker style={{ left: 96, top: 150, opacity: head }} size={26} color={C.inkSoft}>
        {RESULT.head}
      </Kicker>
      <div
        style={{
          position: "absolute", left: 96, top: 196, fontFamily: FONT_SANS,
          fontSize: 46, fontWeight: 500, color: C.ink, whiteSpace: "nowrap", opacity: head,
        }}
      >
        四只 ETF 的账户资产
      </div>

      {/* 表头 */}
      <div style={{ position: "absolute", left: 96, top: 320, width: 888, height: 2, background: C.ink, opacity: head }} />
      {RESULT.columns.map((cLabel, i) => (
        <div
          key={cLabel}
          style={{
            position: "absolute",
            left: [400, 600, 790][i],
            top: 336,
            width: [180, 150, 170][i],
            textAlign: "right",
            fontFamily: FONT_SANS, fontSize: 23, color: C.inkFaint,
            opacity: head,
          }}
        >
          {cLabel}
        </div>
      ))}

      {RESULT.rows.map((r, i) => {
        const p = land(sec, 0.5 + i * 0.36, 0.12, 0.5);
        const top = 400 + i * 152;
        const f = FUNDS.find((x) => x.code === r.code)!;
        return (
          <Panel
            key={r.code}
            style={{
              left: 96, top, width: 888, height: 136, opacity: p,
              fill: i % 2 === 0 ? C.panel : C.panelSoft,
              transform: `translateY(${(1 - p) * 14}px)`,
              
            }}
          >
            <div style={{ position: "absolute", left: 0, top: 0, width: 8, height: 136, background: f.color }} />
            <div style={{ position: "absolute", left: 34, top: 26, fontFamily: FONT_SANS, fontSize: 38, color: C.ink }}>
              {r.name}
            </div>
            <div style={{ position: "absolute", left: 34, top: 84, fontFamily: FONT_MONO, fontSize: 22, color: C.inkFaint }}>
              {r.code}
            </div>
            <div style={{ position: "absolute", left: 284, top: 32, width: 200, textAlign: "right", fontFamily: FONT_MONO, fontSize: 42, fontWeight: 500, color: f.color, whiteSpace: "nowrap" }}>
              {r.final_asset}
            </div>
            <div style={{ position: "absolute", left: 504, top: 62, width: 150, textAlign: "right", fontFamily: FONT_MONO, fontSize: 32, color: C.ink, whiteSpace: "nowrap" }}>
              {r.cumulative}
            </div>
            <div style={{ position: "absolute", left: 694, top: 62, width: 170, textAlign: "right", fontFamily: FONT_MONO, fontSize: 32, color: C.ink, whiteSpace: "nowrap" }}>
              {r.annualized}
            </div>
          </Panel>
        );
      })}

      <div
        style={{
          position: "absolute", left: 96, top: 1060, opacity: land(sec, 2.3, 0.1, 0.5),
        }}
      >
        <InvertTag style={{ left: 0, top: 0, padding: "10px 20px 12px", fontSize: 26 }}>
          {RESULT.foot}
        </InvertTag>
      </div>
      <Kicker style={{ left: 96, top: 1160, opacity: land(sec, 2.7, 0.1, 0.5) }} size={22}>
        累计收益 = 最终资产 ÷ 100,000 − 1　·　年化按 365.2425 天/年复利折算
      </Kicker>
    </Plate>
  );
};


// ---------------------------------------------------------------------------
// sc06 转折 —— 把注意力从"结果"切到"过程"
// ---------------------------------------------------------------------------
export const Turn: React.FC = () => {
  const { sec } = useLocal(96);
  const hero = easeSettle(sec / 0.5);
  const sub = easeSettle((sec - 0.55) / 0.5);
  const foot = easeSettle((sec - 1.1) / 0.5);

  return (
    <Plate>
      <Rule width={888} color={C.ink} thickness={3} grow={easeSettle(sec / 0.4)} style={{ position: "absolute", left: 96, top: 620 }} />
      <div
        style={{
          position: "absolute", left: 96, top: 690, fontFamily: FONT_SANS,
          fontSize: 96, fontWeight: 500, color: C.ink, whiteSpace: "nowrap", lineHeight: 1.2,
          opacity: hero, transform: `translateY(${(1 - hero) * 16}px)`,
        }}
      >
        {TURN.hero}
      </div>
      <div
        style={{
          position: "absolute", left: 96, top: 900, width: 888, fontFamily: FONT_SANS,
          fontSize: 32, lineHeight: 1.45, color: C.inkSoft,
          opacity: sub, transform: `translateY(${(1 - sub) * 12}px)`,
        }}
      >
        {TURN.sub}
      </div>
      <div
        style={{
          position: "absolute", left: 96, top: 982, width: 888, fontFamily: FONT_SANS,
          fontSize: 29, lineHeight: 1.45, color: C.inkFaint, opacity: foot,
        }}
      >
        {TURN.foot}
      </div>
    </Plate>
  );
};
