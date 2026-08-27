import { useCurrentFrame } from "remotion";
import { FINANCE_COLORS, FINANCE_MONO, FinanceFrame, reveal } from "./FinanceFrame";
import { FinanceTitle } from "./FinanceTitle";
import type { FinanceRenderContext, ResearchTimelineEvent } from "./types";

export type ResearchTimelineProps = FinanceRenderContext & {
  title?: string;
  events: ResearchTimelineEvent[];
  highlightedIndex?: number;
  variant?: "horizontal" | "vertical";
};

export const ResearchTimeline: React.FC<ResearchTimelineProps> = ({
  title = "研究时间线",
  events,
  highlightedIndex,
  variant = "vertical",
  theme,
  brand,
  canvasMode = "document",
  headerTreatment = "compact",
  sourceTreatment = "compact",
  sourceLabel,
  sourceDate,
  period,
  sampleData,
}) => {
  const frame = useCurrentFrame();
  const horizontal = variant === "horizontal";
  return (
    <FinanceFrame eyebrow={`DOCUMENT / TIMELINE / ${variant.toUpperCase()}`} source={{sourceLabel, sourceDate, period, sampleData}} theme={theme} brand={brand} canvasMode={canvasMode} headerTreatment={headerTreatment} sourceTreatment={sourceTreatment}>
      <div style={{ position: "absolute", inset: "12% 8% 11% 12%" }}>
        <FinanceTitle preferredFontSize={52} minFontSize={38} maxWidth={820}>{title}</FinanceTitle>
        <div
          style={{
            marginTop: 72,
            display: "grid",
            gridTemplateColumns: horizontal ? `repeat(${events.length}, minmax(0, 1fr))` : "1fr",
            gap: horizontal ? 18 : 0,
            borderLeft: horizontal ? undefined : `2px solid ${FINANCE_COLORS.line}`,
            borderTop: horizontal ? `2px solid ${FINANCE_COLORS.line}` : undefined,
          }}
        >
          {events.map((event, index) => {
            const active = index === highlightedIndex;
            return (
              <div
                key={`${event.date}-${index}`}
                style={{
                  position: "relative",
                  minHeight: horizontal ? 280 : Math.max(190, 820 / Math.max(events.length, 1)),
                  padding: horizontal ? "32px 12px" : "0 0 42px 42px",
                  opacity: reveal(frame, 5 + index * 7, 20 + index * 7),
                }}
              >
                <div style={{ position: "absolute", left: horizontal ? 8 : -9, top: horizontal ? -9 : 8, width: 16, height: 16, borderRadius: "50%", background: active ? FINANCE_COLORS.vermillion : FINANCE_COLORS.teal }} />
                <div style={{ fontFamily: FINANCE_MONO, color: active ? FINANCE_COLORS.vermillion : FINANCE_COLORS.muted, fontSize: 20 }}>{event.date}</div>
                <div style={{ fontSize: horizontal ? 26 : 31, fontWeight: 700, marginTop: 9 }}>{event.title}</div>
                {event.description && <div style={{ fontSize: 21, lineHeight: 1.4, color: FINANCE_COLORS.muted, marginTop: 7 }}>{event.description}</div>}
                {event.source && <div style={{ fontFamily: FINANCE_MONO, fontSize: 17, marginTop: 8, color: FINANCE_COLORS.teal }}>SRC / {event.source}</div>}
              </div>
            );
          })}
        </div>
      </div>
    </FinanceFrame>
  );
};
