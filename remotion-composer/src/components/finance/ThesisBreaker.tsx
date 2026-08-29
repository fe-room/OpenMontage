import { useCurrentFrame } from "remotion";
import { FINANCE_COLORS, FINANCE_MONO, FinanceFrame, reveal } from "./FinanceFrame";
import { FinanceTitle } from "./FinanceTitle";
import type { FinanceRenderContext, ThesisBreakerCondition } from "./types";

export type ThesisBreakerProps = FinanceRenderContext & {
  thesis: string;
  conditions: Array<string | ThesisBreakerCondition>;
};

export const ThesisBreaker: React.FC<ThesisBreakerProps> = ({ thesis, conditions, theme, brand, canvasMode = "margin-note", headerTreatment = "compact", sourceTreatment = "compact", sourceLabel, sourceDate, period, sampleData, complianceText }) => {
  const frame = useCurrentFrame();
  const normalized = conditions.slice(0, 4).map((condition) =>
    typeof condition === "string" ? { title: condition } : condition
  );
  return (
    <FinanceFrame eyebrow="DECISION / THESIS BREAKER" source={{sourceLabel, sourceDate, period, sampleData}} theme={theme} brand={brand} canvasMode={canvasMode} headerTreatment={headerTreatment} sourceTreatment={sourceTreatment} complianceText={complianceText}>
      <div style={{ position: "absolute", left: "7%", right: canvasMode === "margin-note" ? "39%" : "7%", top: "13%", bottom: "12%" }}>
        <div style={{ fontFamily: FINANCE_MONO, fontSize: 19, letterSpacing: "0.08em", color: FINANCE_COLORS.vermillion }}>THESIS BREAKER</div>
        <div style={{ fontSize: 24, marginTop: 10, color: FINANCE_COLORS.muted }}>什么会改变当前判断？</div>
        <FinanceTitle preferredFontSize={45} minFontSize={34} maxWidth={canvasMode === "margin-note" ? 560 : 880} style={{ marginTop: 28 }}>{thesis}</FinanceTitle>
        <div style={{ display: "grid", gridTemplateColumns: "1fr", gap: 0, marginTop: 60, borderTop: `2px solid ${FINANCE_COLORS.line}` }}>
          {normalized.map((condition, index) => (
            <div
              key={`${condition.title}-${index}`}
              style={{
                minHeight: 185,
                padding: "26px 6px",
                display: "grid",
                gridTemplateColumns: "58px 1fr",
                gap: 18,
                borderBottom: `2px solid ${FINANCE_COLORS.line}`,
                opacity: reveal(frame, 7 + index * 7, 24 + index * 7),
              }}
            >
              <div style={{ fontFamily: FINANCE_MONO, color: FINANCE_COLORS.vermillion, fontSize: 22 }}>0{index + 1}</div>
              <div><div style={{ fontSize: 28, lineHeight: 1.3, fontWeight: 700 }}>{condition.title}</div>{condition.description && <div style={{ fontSize: 21, lineHeight: 1.4, color: FINANCE_COLORS.muted, marginTop: 10 }}>{condition.description}</div>}{condition.evidenceToWatch && <div style={{ fontFamily: FINANCE_MONO, fontSize: 18, color: FINANCE_COLORS.teal, marginTop: 14 }}>WATCH / {condition.evidenceToWatch}</div>}</div>
            </div>
          ))}
        </div>
      </div>
    </FinanceFrame>
  );
};
