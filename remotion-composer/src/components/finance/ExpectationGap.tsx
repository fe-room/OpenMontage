import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { AnalystNote, BracketMark, EvidenceIndex } from "./EditorialMarks";
import { FINANCE_COLORS, FINANCE_MONO, FinanceFrame, reveal } from "./FinanceFrame";
import { FinanceTitle } from "./FinanceTitle";
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

const displayValue = (value: FinanceValue, unit?: string) => {
  const text = String(value);
  return unit && !text.trim().endsWith(unit) ? `${text}${unit}` : text;
};

const MetricValue: React.FC<{ label: string; value: FinanceValue; unit?: string; accent: string; subdued?: boolean }> = ({ label, value, unit, accent, subdued = false }) => (
  <div style={{ padding: "22px 0 26px", opacity: subdued ? 0.38 : 1 }}>
    <div style={{ display: "flex", alignItems: "center", gap: 12, fontSize: 22, color: FINANCE_COLORS.muted }}><span style={{ width: 28, height: 4, background: accent }} />{label}</div>
    <div style={{ fontFamily: FINANCE_MONO, fontSize: subdued ? 60 : 82, lineHeight: 1, color: FINANCE_COLORS.ink, fontWeight: 700, marginTop: 18 }}>{displayValue(value, unit)}</div>
  </div>
);

export const ExpectationGap: React.FC<ExpectationGapProps> = ({
  metric, expectedValue, actualValue, delta, unit, interpretation, variant = "split", theme, brand,
  canvasMode = "paper", density = variant === "delta" ? "sparse" : "standard",
  headerTreatment = canvasMode === "full-bleed" ? "none" : canvasMode === "data" ? "compact" : "full",
  sourceTreatment = canvasMode === "margin-note" ? "inline" : canvasMode === "data" ? "compact" : "full",
  analystNote, evidenceIndex, sourceLabel, sourceDate, period, sampleData,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const entry = reveal(frame, 8, 28);
  const expectationReveal = reveal(frame, Math.round(durationInFrames * 0.31), Math.round(durationInFrames * 0.47));
  const deltaReveal = reveal(frame, Math.round(durationInFrames * 0.58), Math.round(durationInFrames * 0.74));
  const marginNote = canvasMode === "margin-note";
  const source = { sourceLabel, sourceDate, period, sampleData };
  const note = analystNote || interpretation;
  const contentRight = marginNote ? "39%" : "7%";
  const deltaText = String(delta);

  return (
    <FinanceFrame eyebrow="EXPECTATION GAP" source={source} theme={theme} brand={brand} canvasMode={canvasMode} headerTreatment={headerTreatment} sourceTreatment={sourceTreatment}>
      <div style={{ position: "absolute", left: "7%", right: contentRight, top: headerTreatment === "none" ? "8%" : "13.5%", bottom: "13%", display: "flex", flexDirection: "column" }}>
        <EvidenceIndex label={evidenceIndex || "EXPECTATION GAP"} />
        <FinanceTitle preferredFontSize={56} minFontSize={39} maxWidth={marginNote ? 560 : 900} style={{ marginTop: 18 }}>{metric}</FinanceTitle>

        {variant === "split" && <div style={{ marginTop: density === "dense" ? 42 : 74, display: "grid", gridTemplateColumns: "1fr 1px 1fr", gap: 34, alignItems: "stretch", translate: `0 ${interpolate(entry, [0, 1], [26, 0])}px` }}><MetricValue label="市场预期" value={expectedValue} unit={unit} accent={FINANCE_COLORS.ochre} /><div style={{ background: FINANCE_COLORS.line }} /><MetricValue label="实际结果" value={actualValue} unit={unit} accent={FINANCE_COLORS.teal} /></div>}

        {variant === "stacked" && <div style={{ marginTop: 48, maxWidth: 720 }}><MetricValue label="市场预期" value={expectedValue} unit={unit} accent={FINANCE_COLORS.ochre} /><div style={{ display: "flex", alignItems: "center", gap: 18, color: FINANCE_COLORS.vermillion, fontSize: 22 }}><span style={{ fontFamily: FINANCE_MONO, fontSize: 34 }}>↓</span><span>再看实际</span><span style={{ height: 2, flex: 1, background: FINANCE_COLORS.line }} /></div><MetricValue label="实际结果" value={actualValue} unit={unit} accent={FINANCE_COLORS.teal} /></div>}

        {variant === "delta" && <div style={{ marginTop: density === "sparse" ? 84 : 56, display: "grid", gridTemplateColumns: "1fr 150px", gap: 32, maxWidth: 860 }}><div><div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}><span style={{ fontSize: 23, color: FINANCE_COLORS.muted }}>市场预期</span><strong style={{ fontFamily: FINANCE_MONO, fontSize: 58 }}>{displayValue(expectedValue, unit)}</strong></div><div style={{ height: 5, background: FINANCE_COLORS.ochre, marginTop: 16 }} /><div style={{ padding: "64px 0 54px", textAlign: "center", fontFamily: FINANCE_MONO, color: FINANCE_COLORS.vermillion, fontSize: 92, lineHeight: 1, fontWeight: 700, letterSpacing: "-0.06em" }}>{deltaText}</div><div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}><span style={{ fontSize: 23, color: FINANCE_COLORS.muted }}>实际结果</span><strong style={{ fontFamily: FINANCE_MONO, fontSize: 58 }}>{displayValue(actualValue, unit)}</strong></div><div style={{ height: 5, background: FINANCE_COLORS.teal, marginTop: 16, width: "82%" }} /></div><div style={{ display: "flex", alignItems: "center" }}><BracketMark height={330} width={130} /></div></div>}

        {variant === "reveal" && <div style={{ marginTop: 58, position: "relative", minHeight: 690 }}><div style={{ opacity: interpolate(deltaReveal, [0, 1], [1, 0]), translate: `0 ${interpolate(entry, [0, 1], [26, 0])}px` }}><MetricValue label="实际结果" value={actualValue} unit={unit} accent={FINANCE_COLORS.teal} subdued={deltaReveal > 0.65} /><div style={{ fontSize: 29, marginTop: 8 }}>看起来很强。</div></div><div style={{ marginTop: 40, opacity: expectationReveal * interpolate(deltaReveal, [0, 1], [1, 0]), translate: `0 ${interpolate(expectationReveal, [0, 1], [22, 0])}px` }}><div style={{ fontSize: 25, color: FINANCE_COLORS.muted }}>但市场原本期待</div><div style={{ fontFamily: FINANCE_MONO, fontSize: 74, fontWeight: 700, marginTop: 12 }}>{displayValue(expectedValue, unit)}</div></div><div style={{ position: "absolute", left: 0, top: 205, opacity: deltaReveal, translate: `0 ${interpolate(deltaReveal, [0, 1], [34, 0])}px` }}><div style={{ fontFamily: FINANCE_MONO, fontSize: 118, lineHeight: 1, fontWeight: 700, letterSpacing: "-0.07em", color: FINANCE_COLORS.vermillion }}>{deltaText}</div><div style={{ marginTop: 28, fontSize: 30, lineHeight: 1.5 }}>问题不是差。<br />而是没有好到超过预期。</div></div></div>}

        {variant !== "reveal" && variant !== "delta" && <div style={{ marginTop: "auto", paddingTop: 42, borderTop: `2px solid ${FINANCE_COLORS.line}`, display: "grid", gridTemplateColumns: "auto 1fr", gap: 30, alignItems: "start" }}><div style={{ fontFamily: FINANCE_MONO, color: FINANCE_COLORS.vermillion, fontSize: 58, fontWeight: 700 }}>{deltaText}</div>{note && !marginNote && <div style={{ fontSize: 27, lineHeight: 1.5 }}>{note}</div>}</div>}
        {variant === "delta" && note && !marginNote && <div style={{ marginTop: "auto" }}><AnalystNote>{note}</AnalystNote></div>}
      </div>
      {marginNote && note && <div style={{ position: "absolute", right: "8.5%", top: "34%", width: "27%" }}><AnalystNote compact>{note}</AnalystNote></div>}
    </FinanceFrame>
  );
};
