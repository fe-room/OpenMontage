import { useCurrentFrame } from "remotion";
import { FINANCE_COLORS, FINANCE_MONO, FinanceFrame, reveal } from "./FinanceFrame";
import type { FinanceRenderContext, ResearchTimelineEvent } from "./types";

export type ResearchTimelineProps = FinanceRenderContext & {
  title?: string;
  events: ResearchTimelineEvent[];
  highlightedIndex?: number;
  variant?: "horizontal" | "vertical";
};

export const ResearchTimeline: React.FC<ResearchTimelineProps> = ({
  title = "Research timeline",
  events,
  highlightedIndex,
  variant = "vertical",
  theme,
  brand,
  ...source
}) => {
  const frame = useCurrentFrame();
  const horizontal = variant === "horizontal";
  return (
    <FinanceFrame eyebrow={`DOCUMENT / TIMELINE / ${variant.toUpperCase()}`} source={source} theme={theme} brand={brand}>
      <div style={{ position: "absolute", inset: "13% 7% 12%" }}>
        <h1 style={{ margin: 0, fontSize: 52 }}>{title}</h1>
        <div
          style={{
            marginTop: 55,
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
                  padding: horizontal ? "32px 12px" : "0 0 34px 38px",
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
