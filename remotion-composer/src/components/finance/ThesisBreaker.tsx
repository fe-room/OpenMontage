import { useCurrentFrame } from "remotion";
import { FINANCE_COLORS, FINANCE_MONO, FinanceFrame, reveal } from "./FinanceFrame";
import type { SourceContext, ThesisBreakerCondition } from "./types";

export type ThesisBreakerProps = SourceContext & {
  thesis: string;
  conditions: Array<string | ThesisBreakerCondition>;
};

export const ThesisBreaker: React.FC<ThesisBreakerProps> = ({ thesis, conditions, ...source }) => {
  const frame = useCurrentFrame();
  const normalized = conditions.slice(0, 4).map((condition) =>
    typeof condition === "string" ? { title: condition } : condition
  );
  return (
    <FinanceFrame eyebrow="DECISION / THESIS BREAKER" source={source}>
      <div style={{ position: "absolute", inset: "14% 7% 12%" }}>
        <div style={{ fontFamily: FINANCE_MONO, fontSize: 21, color: FINANCE_COLORS.vermillion }}>WHAT WOULD CHANGE THE THESIS?</div>
        <h1 style={{ fontSize: 45, lineHeight: 1.28, margin: "24px 0 45px", maxWidth: 900 }}>{thesis}</h1>
        <div style={{ display: "grid", gridTemplateColumns: normalized.length > 2 ? "1fr 1fr" : "1fr", gap: 18 }}>
          {normalized.map((condition, index) => (
            <div
              key={`${condition.title}-${index}`}
              style={{
                minHeight: 230,
                padding: 28,
                background: FINANCE_COLORS.surface,
                borderLeft: `7px solid ${FINANCE_COLORS.vermillion}`,
                opacity: reveal(frame, 7 + index * 7, 24 + index * 7),
              }}
            >
              <div style={{ fontFamily: FINANCE_MONO, color: FINANCE_COLORS.muted, fontSize: 20 }}>0{index + 1}</div>
              <div style={{ fontSize: 29, lineHeight: 1.3, fontWeight: 700, marginTop: 12 }}>{condition.title}</div>
              {condition.description && <div style={{ fontSize: 21, lineHeight: 1.4, color: FINANCE_COLORS.muted, marginTop: 10 }}>{condition.description}</div>}
              {condition.evidenceToWatch && <div style={{ fontFamily: FINANCE_MONO, fontSize: 18, color: FINANCE_COLORS.teal, marginTop: 14 }}>WATCH / {condition.evidenceToWatch}</div>}
            </div>
          ))}
        </div>
      </div>
    </FinanceFrame>
  );
};
