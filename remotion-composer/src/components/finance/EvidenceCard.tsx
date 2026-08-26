import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import {
  DirectionMark,
  FINANCE_COLORS,
  FINANCE_MONO,
  FinanceFrame,
  reveal,
} from "./FinanceFrame";
import type { FinanceLayoutVariant, FinanceRenderContext, FinanceValue, SupportingMetric } from "./types";

export type EvidenceCardProps = FinanceRenderContext & {
  label: string;
  primaryValue: FinanceValue;
  supportingMetrics?: SupportingMetric[];
  interpretation?: string;
  variant?: FinanceLayoutVariant;
};

export const EvidenceCard: React.FC<EvidenceCardProps> = ({
  label,
  primaryValue,
  supportingMetrics = [],
  interpretation,
  variant = "hero-number",
  theme,
  brand,
  ...source
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const valueY = interpolate(reveal(frame, 8, 8 + fps * 0.7), [0, 1], [28, 0]);
  const isDocument = variant === "document";
  const isTable = variant === "table";

  return (
    <FinanceFrame eyebrow={`EVIDENCE / ${variant.toUpperCase()}`} source={source} theme={theme} brand={brand}>
      <div
        style={{
          position: "absolute",
          left: isDocument ? "10%" : "7%",
          right: isDocument ? "7%" : "7%",
          top: isDocument ? "15%" : "18%",
          bottom: "12%",
          display: "grid",
          gridTemplateColumns: variant === "comparison" ? "1.2fr 1fr" : "1fr",
          alignContent: "center",
          gap: 42,
          borderLeft: isDocument ? `8px solid ${FINANCE_COLORS.vermillion}` : undefined,
          paddingLeft: isDocument ? 48 : 0,
        }}
      >
        <div>
          <div
            style={{
              fontFamily: FINANCE_MONO,
              fontSize: 24,
              letterSpacing: "0.08em",
              color: FINANCE_COLORS.vermillion,
              marginBottom: 28,
              opacity: reveal(frame, 0, 12),
            }}
          >
            {label.toUpperCase()}
          </div>
          <div
            style={{
              fontFamily: FINANCE_MONO,
              fontSize: isTable ? 108 : 154,
              lineHeight: 0.92,
              fontWeight: 700,
              letterSpacing: "-0.055em",
              opacity: reveal(frame, 8, 24),
              transform: `translateY(${valueY}px)`,
            }}
          >
            {primaryValue}
          </div>
          {interpretation && (
            <div
              style={{
                marginTop: 34,
                maxWidth: 760,
                fontSize: 33,
                lineHeight: 1.45,
                opacity: reveal(frame, 22, 38),
              }}
            >
              {interpretation}
            </div>
          )}
        </div>
        {supportingMetrics.length > 0 && (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: isTable ? "1fr" : "repeat(2, minmax(0, 1fr))",
              borderTop: `1px solid ${FINANCE_COLORS.line}`,
            }}
          >
            {supportingMetrics.map((metric, index) => (
              <div
                key={`${metric.label}-${index}`}
                style={{
                  padding: "24px 18px 22px 0",
                  borderBottom: `1px solid ${FINANCE_COLORS.line}`,
                  opacity: reveal(frame, 24 + index * 5, 39 + index * 5),
                }}
              >
                <div style={{ color: FINANCE_COLORS.muted, fontSize: 21 }}>{metric.label}</div>
                <div style={{ fontFamily: FINANCE_MONO, fontSize: 36, marginTop: 8 }}>
                  {metric.value} <DirectionMark direction={metric.direction} />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </FinanceFrame>
  );
};
