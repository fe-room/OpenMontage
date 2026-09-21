import React from "react";
import { C, FONT_SANS, easeSettle } from "./theme";
import { InvertTag, IdentityMark, Kicker, Rule, land, useLocal, Plate } from "./Foundation";
import { CLOSING, FUNDS } from "./timeline";

// ---------------------------------------------------------------------------
// sc10 结尾与合规 —— 三组归类 + 可复用判断动作 + 边界条件 + 原生合规页脚
// ---------------------------------------------------------------------------
export const Closing: React.FC = () => {
  const { sec } = useLocal(144);
  const head = land(sec, 0, 0.1, 0.5);
  const hero = easeSettle((sec - 1.5) / 0.6);
  const sub = easeSettle((sec - 2.0) / 0.6);
  const method = easeSettle((sec - 2.5) / 0.6);
  const tailP = clamp(sec, 3.0, 0.6);

  const group = (idx: number) => CLOSING.groups[idx];

  return (
    <Plate>
      <Kicker style={{ left: 96, top: 128, opacity: head }} size={26} color={C.inkSoft}>
        {CLOSING.head}
      </Kicker>
      <Rule width={888} color={C.ink} thickness={3} grow={easeSettle(sec / 0.4)} style={{ position: "absolute", left: 96, top: 178 }} />

      {/* 三组归类 */}
      {[
        { top: 240, lines: 1 },
        { top: 372, lines: 1 },
        { top: 504, lines: 2 },
      ].map((slot, gi) => {
        const g = group(gi);
        const p = land(sec, 0.35 + gi * 0.28, 0.1, 0.5);
        return (
          <div key={g.label} style={{ position: "absolute", inset: 0, opacity: p, transform: `translateY(${(1 - p) * 12}px)` }}>
            <div
              style={{
                position: "absolute", left: 96, top: slot.top + 4, fontFamily: FONT_SANS,
                fontSize: 26, color: C.inkFaint, whiteSpace: "nowrap",
              }}
            >
              {g.label}
            </div>
            {g.codes.map((code, ci) => {
              const f = FUNDS.find((x) => x.code === code)!;
              return (
                <IdentityMark
                  key={code}
                  color={f.color}
                  label={f.name}
                  code={f.code}
                  style={{ left: 384, top: slot.top + ci * 84 }}
                  labelSize={34}
                  codeSize={20}
                />
              );
            })}
          </div>
        );
      })}

      <Rule width={888} color={C.grid} thickness={2} style={{ position: "absolute", left: 96, top: 720 }} />

      <div
        style={{
          position: "absolute", left: 96, top: 764, fontFamily: FONT_SANS, fontSize: 74,
          fontWeight: 500, color: C.ink, whiteSpace: "nowrap", opacity: hero,
          transform: `translateY(${(1 - hero) * 14}px)`,
        }}
      >
        {CLOSING.hero}
      </div>
      <div
        style={{
          position: "absolute", left: 96, top: 880, fontFamily: FONT_SANS, fontSize: 34,
          color: C.inkSoft, whiteSpace: "nowrap", opacity: sub,
        }}
      >
        {CLOSING.sub}
      </div>

      <div style={{ position: "absolute", left: 96, top: 968, opacity: method }}>
        <InvertTag style={{ left: 0, top: 0, padding: "8px 16px 10px", fontSize: 22 }}>
          可以带走的一个动作
        </InvertTag>
      </div>
      <div
        style={{
          position: "absolute", left: 96, top: 1032, width: 888, fontFamily: FONT_SANS,
          fontSize: 28, lineHeight: 1.5, color: C.ink, opacity: method,
        }}
      >
        {CLOSING.method}
      </div>

      {/* 边界条件与合规页脚：必须落在竖屏安全区（距底 520px）之内 */}
      <Rule width={888} color={C.grid} thickness={2} style={{ position: "absolute", left: 96, top: 1226 }} />
      <div
        style={{
          position: "absolute", left: 96, top: 1242, width: 888, fontFamily: FONT_SANS,
          fontSize: 20, lineHeight: 1.5, color: C.inkFaint, opacity: tailP,
        }}
      >
        {CLOSING.scope_note}
      </div>
      <div
        style={{
          position: "absolute", left: 96, top: 1326, width: 888, fontFamily: FONT_SANS,
          fontSize: 22, lineHeight: 1.4, color: C.inkSoft, opacity: tailP,
        }}
      >
        {CLOSING.disclaimer}
      </div>
    </Plate>
  );
};

function clamp(x: number, start: number, dur: number) {
  return Math.max(0, Math.min(1, (x - start) / dur));
}
