import { useCurrentFrame } from "remotion";
import { FINANCE_COLORS, FINANCE_MONO, FinanceFrame, reveal } from "./FinanceFrame";
import { FinanceTitle } from "./FinanceTitle";
import type { FinanceRenderContext, Scenario } from "./types";

export type ScenarioBoardProps = FinanceRenderContext & {
  title?: string;
  scenarios: Scenario[];
  highlightedScenario?: string;
};

export const ScenarioBoard: React.FC<ScenarioBoardProps> = ({
  title = "条件情景，不是预测",
  scenarios,
  highlightedScenario,
  theme,
  brand,
  canvasMode = "paper",
  headerTreatment = "full",
  sourceTreatment = "compact",
  sourceLabel,
  sourceDate,
  period,
  sampleData,
  complianceText,
}) => {
  const frame = useCurrentFrame();
  return (
    <FinanceFrame eyebrow="DECISION / SCENARIO" source={{sourceLabel, sourceDate, period, sampleData}} theme={theme} brand={brand} canvasMode={canvasMode} headerTreatment={headerTreatment} sourceTreatment={sourceTreatment} complianceText={complianceText}>
      <div style={{ position: "absolute", inset: "13% 6% 11%" }}>
        <FinanceTitle preferredFontSize={50} minFontSize={38} maxWidth={880}>{title}</FinanceTitle>
        <div style={{ marginTop: 58, display: "grid", gridTemplateColumns: `repeat(${Math.min(scenarios.length, 3)}, minmax(0, 1fr))`, gap: 22 }}>
          {scenarios.map((scenario, index) => {
            const active = scenario.name === highlightedScenario;
            return (
              <div
                key={`${scenario.name}-${index}`}
                style={{
                  minHeight: 900,
                  padding: "30px 24px",
                  background: active ? FINANCE_COLORS.surface : "transparent",
                  borderTop: `7px solid ${active ? FINANCE_COLORS.vermillion : index === 1 ? FINANCE_COLORS.teal : FINANCE_COLORS.ochre}`,
                  borderBottom: `2px solid ${FINANCE_COLORS.line}`,
                  opacity: reveal(frame, index * 7, 20 + index * 7),
                }}
              >
                <div style={{ fontFamily: FINANCE_MONO, fontSize: 24, color: FINANCE_COLORS.vermillion }}>{scenario.name.toUpperCase()}</div>
                <h2 style={{ fontSize: 31, lineHeight: 1.2, margin: "24px 0 18px" }}>{scenario.title ?? scenario.name}</h2>
                <p style={{ fontSize: 23, lineHeight: 1.45, color: FINANCE_COLORS.muted }}>{scenario.description}</p>
                <div style={{ borderTop: `1px solid ${FINANCE_COLORS.line}`, marginTop: 24, paddingTop: 18 }}>
                  <div style={{ fontFamily: FINANCE_MONO, fontSize: 18, color: FINANCE_COLORS.teal }}>TRIGGER</div>
                  <div style={{ fontSize: 22, lineHeight: 1.4, marginTop: 8 }}>{scenario.trigger}</div>
                </div>
                {scenario.probability !== undefined && (
                  <div style={{ fontFamily: FINANCE_MONO, fontSize: 26, marginTop: 22 }}>P / {scenario.probability}%</div>
                )}
                {scenario.metrics && scenario.metrics.length > 0 && (
                  <div style={{ marginTop: 26 }}>
                    <div style={{ fontFamily: FINANCE_MONO, fontSize: 18, color: FINANCE_COLORS.teal }}>WATCH</div>
                    {scenario.metrics.map((metric) => <div key={metric} style={{ fontSize: 19, marginTop: 8 }}>→ {metric}</div>)}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </FinanceFrame>
  );
};
