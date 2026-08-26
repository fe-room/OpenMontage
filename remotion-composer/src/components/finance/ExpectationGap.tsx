import { interpolate, useCurrentFrame } from "remotion";
import { FINANCE_COLORS, FINANCE_MONO, FinanceFrame, reveal } from "./FinanceFrame";
import type { SourceContext } from "./types";

export type ExpectationGapProps = SourceContext & {
  metric: string;
  expectedValue: string;
  actualValue: string;
  delta: string;
  unit?: string;
  interpretation?: string;
  variant?: "split" | "stacked" | "delta" | "reveal";
};

export const ExpectationGap: React.FC<ExpectationGapProps> = ({
  metric,
  expectedValue,
  actualValue,
  delta,
  unit,
  interpretation,
  variant = "split",
  ...source
}) => {
  const frame = useCurrentFrame();
  const progress = reveal(frame, 8, 30);
  const vertical = variant === "stacked" || variant === "reveal";
  return (
    <FinanceFrame eyebrow={`EXPECTATION GAP / ${variant.toUpperCase()}`} source={source}>
      <div style={{ position: "absolute", inset: "15% 7% 12%", display: "flex", flexDirection: "column" }}>
        <h1 style={{ margin: 0, fontSize: 54, lineHeight: 1.18, maxWidth: 820 }}>{metric}</h1>
        <div
          style={{
            marginTop: 58,
            display: "grid",
            gridTemplateColumns: vertical ? "1fr" : "1fr 1fr",
            gap: vertical ? 26 : 20,
          }}
        >
          {[
            ["EXPECTED", expectedValue, FINANCE_COLORS.muted],
            ["ACTUAL", actualValue, FINANCE_COLORS.ink],
          ].map(([label, value, color], index) => (
            <div
              key={label}
              style={{
                borderTop: `5px solid ${index === 0 ? FINANCE_COLORS.ochre : FINANCE_COLORS.teal}`,
                padding: "30px 26px",
                background: FINANCE_COLORS.surface,
                transform: `translateY(${interpolate(progress, [0, 1], [28 + index * 16, 0])}px)`,
                opacity: reveal(frame, 10 + index * 8, 28 + index * 8),
              }}
            >
              <div style={{ fontFamily: FINANCE_MONO, fontSize: 22, color: FINANCE_COLORS.muted }}>{label}</div>
              <div style={{ fontFamily: FINANCE_MONO, fontSize: 76, color, fontWeight: 700, marginTop: 22 }}>
                {value}<span style={{ fontSize: 30, marginLeft: 10 }}>{unit}</span>
              </div>
            </div>
          ))}
        </div>
        <div style={{ marginTop: 34, display: "flex", alignItems: "baseline", gap: 22 }}>
          <span style={{ fontFamily: FINANCE_MONO, color: FINANCE_COLORS.vermillion, fontSize: 45, fontWeight: 700, whiteSpace: "nowrap", flexShrink: 0 }}>
            Δ {delta}
          </span>
          {interpretation && <span style={{ fontSize: 27, lineHeight: 1.4, color: FINANCE_COLORS.muted }}>{interpretation}</span>}
        </div>
      </div>
    </FinanceFrame>
  );
};
