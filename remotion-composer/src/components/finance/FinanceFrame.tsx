import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import type { ThemeConfig } from "../../theme";
import type { FinanceBrand } from "./types";

export const FINANCE_COLORS = {
  paper: "var(--finance-paper, #F2EFE7)",
  ink: "var(--finance-ink, #171715)",
  muted: "var(--finance-muted, #6C6860)",
  vermillion: "var(--finance-accent, #B44736)",
  teal: "var(--finance-primary, #345C5B)",
  ochre: "var(--finance-highlight, #C5A64A)",
  line: "var(--finance-line, #CEC8BA)",
  surface: "var(--finance-surface, #F8F5ED)",
};

export const FINANCE_SANS =
  'var(--finance-sans, "Noto Sans SC", "Source Han Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif)';
export const FINANCE_MONO =
  'var(--finance-mono, "IBM Plex Mono", "SFMono-Regular", Consolas, monospace)';

export const reveal = (frame: number, start: number, end: number): number =>
  interpolate(frame, [start, end], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

export const DirectionMark: React.FC<{ direction?: "up" | "down" | "flat" }> = ({
  direction,
}) => {
  if (!direction) return null;
  const mark = direction === "up" ? "+ ↑" : direction === "down" ? "− ↓" : "→ FLAT";
  return <span style={{ color: FINANCE_COLORS.teal, fontFamily: FINANCE_MONO }}>{mark}</span>;
};

export type SourceStripProps = {
  sourceLabel?: string;
  sourceDate?: string;
  period?: string;
  sampleData?: boolean;
};

export const SourceStrip: React.FC<SourceStripProps> = ({
  sourceLabel,
  sourceDate,
  period,
  sampleData = false,
}) => {
  const frame = useCurrentFrame();
  const opacity = reveal(frame, 10, 24);
  const parts = [period, sourceLabel, sourceDate].filter(Boolean);
  if (!parts.length && !sampleData) return null;

  return (
    <div
      style={{
        position: "absolute",
        left: "6.5%",
        right: "6.5%",
        bottom: "4.5%",
        borderTop: `1px solid ${FINANCE_COLORS.line}`,
        paddingTop: 16,
        display: "flex",
        justifyContent: "space-between",
        gap: 24,
        color: FINANCE_COLORS.muted,
        fontFamily: FINANCE_MONO,
        fontSize: 19,
        letterSpacing: "0.055em",
        opacity,
      }}
    >
      <span>{parts.join("  /  ")}</span>
      {sampleData && (
        <span style={{ color: FINANCE_COLORS.vermillion, fontWeight: 700 }}>SAMPLE DATA</span>
      )}
    </div>
  );
};

export const FinanceFrame: React.FC<{
  eyebrow?: string;
  children: React.ReactNode;
  source?: SourceStripProps;
  theme?: ThemeConfig;
  brand?: FinanceBrand;
}> = ({ eyebrow, children, source, theme, brand }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const grainOpacity = 0.018 + Math.sin(frame / 19) * 0.003;
  const scale = Math.min(width / 1080, height / 1920);
  const headerRight = [brand?.series, brand?.issue].filter(Boolean).join(" / ") || eyebrow || "";
  const cssTokens = {
    "--finance-paper": theme?.backgroundColor,
    "--finance-ink": theme?.textColor,
    "--finance-muted": theme?.mutedTextColor,
    "--finance-accent": theme?.accentColor,
    "--finance-primary": theme?.primaryColor,
    "--finance-highlight": theme?.chartColors?.[2],
    "--finance-surface": theme?.surfaceColor,
    "--finance-sans": theme?.headingFont || theme?.bodyFont,
    "--finance-mono": theme?.monoFont,
  } as React.CSSProperties;

  return (
    <AbsoluteFill
      style={{
        ...cssTokens,
        background: FINANCE_COLORS.paper,
        color: FINANCE_COLORS.ink,
        fontFamily: FINANCE_SANS,
        overflow: "hidden",
      }}
    >
      <AbsoluteFill
        style={{
          opacity: grainOpacity,
          backgroundImage:
            `repeating-linear-gradient(0deg, ${FINANCE_COLORS.ink} 0, ${FINANCE_COLORS.ink} 1px, transparent 1px, transparent 4px)`,
          backgroundSize: `${Math.max(3, 4 * scale)}px ${Math.max(3, 4 * scale)}px`,
        }}
      />
      <div
        style={{
          position: "absolute",
          left: "6.5%",
          top: "4.5%",
          width: "87%",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontFamily: FINANCE_MONO,
          fontSize: 18,
          letterSpacing: "0.08em",
          color: FINANCE_COLORS.muted,
          opacity: reveal(frame, 0, 12),
        }}
      >
        <span>{brand?.label || "FINANCE DOSSIER"}</span>
        <span>{headerRight}</span>
      </div>
      {children}
      {source && <SourceStrip {...source} />}
    </AbsoluteFill>
  );
};
