import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { AnalystNote, EvidenceIndex, UnderlineMark } from "./EditorialMarks";
import { DirectionMark, FINANCE_COLORS, FINANCE_MONO, FinanceFrame, reveal } from "./FinanceFrame";
import { FinanceTitle } from "./FinanceTitle";
import type { FinanceLayoutVariant, FinanceRenderContext, FinanceValue, SupportingMetric } from "./types";

export type EvidenceCardProps = FinanceRenderContext & {
  label: string;
  primaryValue: FinanceValue;
  supportingMetrics?: SupportingMetric[];
  interpretation?: string;
  variant?: FinanceLayoutVariant;
};

export const EvidenceCard: React.FC<EvidenceCardProps> = ({
  label, primaryValue, supportingMetrics = [], interpretation, variant = "hero-number",
  theme, brand, canvasMode = variant === "document" ? "document" : "paper", density = "standard",
  headerTreatment = canvasMode === "full-bleed" ? "none" : "full",
  sourceTreatment = canvasMode === "document" ? "compact" : "full", analystNote, evidenceIndex,
  sourceLabel, sourceDate, period, sampleData,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const valueY = interpolate(reveal(frame, 8, 8 + fps * 0.7), [0, 1], [28, 0]);
  const isDocument = canvasMode === "document";
  const marginNote = canvasMode === "margin-note";
  const isTable = variant === "table";
  const source = { sourceLabel, sourceDate, period, sampleData };
  const note = analystNote || (marginNote ? interpretation : undefined);

  return (
    <FinanceFrame eyebrow={evidenceIndex || "EVIDENCE"} source={source} theme={theme} brand={brand} canvasMode={canvasMode} headerTreatment={headerTreatment} sourceTreatment={sourceTreatment}>
      <div style={{ position: "absolute", left: isDocument ? "13%" : "7%", right: marginNote ? "39%" : isDocument ? "9%" : "7%", top: headerTreatment === "none" ? "9%" : "14%", bottom: "13%", display: "grid", gridTemplateRows: density === "sparse" ? "auto 1fr auto" : "auto auto 1fr auto", alignContent: "start", gap: density === "dense" ? 28 : 42 }}>
        <EvidenceIndex label={evidenceIndex || "EVIDENCE"} />
        <div>
          <FinanceTitle preferredFontSize={isDocument ? 46 : 52} minFontSize={36} maxWidth={marginNote ? 540 : 850}>{label}</FinanceTitle>
          <div style={{ marginTop: 14 }}><UnderlineMark width={Math.min(360, Math.max(160, label.length * 20))} /></div>
        </div>
        <div style={{ alignSelf: "center", padding: density === "dense" ? "20px 0" : "52px 0 40px" }}>
          <div style={{ fontFamily: FINANCE_MONO, fontSize: isTable ? 104 : density === "sparse" ? 176 : 154, lineHeight: 0.9, fontWeight: 700, letterSpacing: "-0.055em", opacity: reveal(frame, 8, 24), translate: `0 ${valueY}px` }}>{primaryValue}</div>
          {interpretation && !marginNote && <div style={{ marginTop: 38, maxWidth: 760, fontSize: 31, lineHeight: 1.5, opacity: reveal(frame, 22, 38) }}>{interpretation}</div>}
        </div>
        {supportingMetrics.length > 0 && (
          <div style={{ display: "grid", gridTemplateColumns: isTable ? "1fr" : `repeat(${Math.min(supportingMetrics.length, 2)}, minmax(0, 1fr))`, gap: "0 34px", borderTop: `2px solid ${FINANCE_COLORS.line}`, alignSelf: "end" }}>
            {supportingMetrics.map((metric, index) => (
              <div key={`${metric.label}-${index}`} style={{ padding: "24px 8px 22px 0", borderBottom: `2px solid ${FINANCE_COLORS.line}`, opacity: reveal(frame, 24 + index * 5, 39 + index * 5) }}>
                <div style={{ color: FINANCE_COLORS.muted, fontSize: 21 }}>{metric.label}</div>
                <div style={{ fontFamily: FINANCE_MONO, fontSize: 36, marginTop: 8 }}>{metric.value} <DirectionMark direction={metric.direction} /></div>
              </div>
            ))}
          </div>
        )}
      </div>
      {note && <div style={{ position: "absolute", right: "8.5%", top: marginNote ? "35%" : "68%", width: marginNote ? "27%" : "44%" }}><AnalystNote compact={marginNote}>{note}</AnalystNote></div>}
    </FinanceFrame>
  );
};
