import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { FINANCE_COLORS, FINANCE_MONO, FinanceFrame, reveal } from "./FinanceFrame";
import type { FinanceRenderContext, FinanceValue } from "./types";

export type ExpectationGapProps = FinanceRenderContext & {
  metric: string;
  expectedValue: FinanceValue;
  actualValue: FinanceValue;
  delta: FinanceValue;
  unit?: string;
  interpretation?: string;
  variant?: "split" | "stacked" | "delta" | "reveal";
};

const Value: React.FC<{ label: string; value: FinanceValue; unit?: string; accent: string; opacity?: number }> = ({ label, value, unit, accent, opacity = 1 }) => (
  <div style={{ borderTop: `5px solid ${accent}`, padding: "28px 26px", background: FINANCE_COLORS.surface, opacity }}>
    <div style={{ fontFamily: FINANCE_MONO, fontSize: 22, color: FINANCE_COLORS.muted }}>{label}</div>
    <div style={{ fontFamily: FINANCE_MONO, fontSize: 76, color: FINANCE_COLORS.ink, fontWeight: 700, marginTop: 18 }}>
      {value}<span style={{ fontSize: 30, marginLeft: unit ? 10 : 0 }}>{unit}</span>
    </div>
  </div>
);

export const ExpectationGap: React.FC<ExpectationGapProps> = ({
  metric, expectedValue, actualValue, delta, unit, interpretation, variant = "split", theme, brand, ...source
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const entry = reveal(frame, 8, 30);
  const expectationReveal = reveal(frame, Math.round(durationInFrames * 0.32), Math.round(durationInFrames * 0.5));
  const deltaReveal = reveal(frame, Math.round(durationInFrames * 0.58), Math.round(durationInFrames * 0.76));
  const deltaHero = <div style={{ fontFamily: FINANCE_MONO, color: FINANCE_COLORS.vermillion, fontSize: 54, fontWeight: 700 }}>Δ {delta}</div>;

  return (
    <FinanceFrame eyebrow={`EXPECTATION GAP / ${variant.toUpperCase()}`} source={source} theme={theme} brand={brand}>
      <div style={{ position: "absolute", inset: "15% 7% 12%", display: "flex", flexDirection: "column" }}>
        <h1 style={{ margin: 0, fontSize: 54, lineHeight: 1.18, maxWidth: 850 }}>{metric}</h1>
        {variant === "split" && <div style={{ marginTop: 58, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, transform: `translateY(${interpolate(entry, [0, 1], [28, 0])}px)` }}><Value label="EXPECTED" value={expectedValue} unit={unit} accent={FINANCE_COLORS.ochre} /><Value label="ACTUAL" value={actualValue} unit={unit} accent={FINANCE_COLORS.teal} /></div>}
        {variant === "stacked" && <div style={{ marginTop: 46, display: "grid", gridTemplateRows: "1fr auto 1fr", gap: 16 }}><Value label="EXPECTED" value={expectedValue} unit={unit} accent={FINANCE_COLORS.ochre} /><div style={{ textAlign: "center", color: FINANCE_COLORS.vermillion, fontFamily: FINANCE_MONO, fontSize: 38 }}>↓ COMPARE ↓</div><Value label="ACTUAL" value={actualValue} unit={unit} accent={FINANCE_COLORS.teal} /></div>}
        {variant === "delta" && <div style={{ marginTop: 58, position: "relative", minHeight: 540, background: FINANCE_COLORS.surface, padding: "48px 44px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", fontFamily: FINANCE_MONO }}><span style={{ color: FINANCE_COLORS.muted, fontSize: 22 }}>EXPECTED</span><strong style={{ fontSize: 62 }}>{expectedValue}{unit}</strong></div>
          <div style={{ height: 6, background: FINANCE_COLORS.ochre, marginTop: 18 }} />
          <div style={{ position: "absolute", right: 44, top: 142, height: 205, width: 115, borderRight: `5px solid ${FINANCE_COLORS.vermillion}`, borderTop: `5px solid ${FINANCE_COLORS.vermillion}`, borderBottom: `5px solid ${FINANCE_COLORS.vermillion}` }} />
          <div style={{ position: "absolute", right: 185, top: 210 }}>{deltaHero}</div>
          <div style={{ marginTop: 235, display: "flex", justifyContent: "space-between", alignItems: "baseline", fontFamily: FINANCE_MONO }}><span style={{ color: FINANCE_COLORS.muted, fontSize: 22 }}>ACTUAL</span><strong style={{ fontSize: 62 }}>{actualValue}{unit}</strong></div>
          <div style={{ height: 6, background: FINANCE_COLORS.teal, marginTop: 18, width: "82%" }} />
        </div>}
        {variant === "reveal" && <div style={{ marginTop: 48, display: "grid", gap: 18 }}>
          <Value label="ACTUAL — FIRST IMPRESSION" value={actualValue} unit={unit} accent={FINANCE_COLORS.teal} />
          <div style={{ transform: `translateY(${interpolate(expectationReveal, [0, 1], [24, 0])}px)` }}><Value label="EXPECTATION — REVEALED" value={expectedValue} unit={unit} accent={FINANCE_COLORS.ochre} opacity={expectationReveal} /></div>
          <div style={{ opacity: deltaReveal, transform: `scale(${interpolate(deltaReveal, [0, 1], [0.9, 1])})`, transformOrigin: "left center", display: "flex", alignItems: "baseline", gap: 24 }}>{deltaHero}<span style={{ color: FINANCE_COLORS.muted, fontSize: 26 }}>the gap changes the reading</span></div>
        </div>}
        {variant !== "reveal" && <div style={{ marginTop: 30, display: "flex", alignItems: "baseline", gap: 22 }}>{variant !== "delta" && deltaHero}{interpretation && <span style={{ fontSize: 27, lineHeight: 1.4, color: FINANCE_COLORS.muted }}>{interpretation}</span>}</div>}
        {variant === "reveal" && interpretation && <div style={{ marginTop: 20, fontSize: 27, lineHeight: 1.4, color: FINANCE_COLORS.muted, opacity: deltaReveal }}>{interpretation}</div>}
      </div>
    </FinanceFrame>
  );
};
