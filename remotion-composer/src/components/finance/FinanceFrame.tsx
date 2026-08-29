import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import type { ThemeConfig } from "../../theme";
import type {
  FinanceBrand,
  FinanceCanvasMode,
  FinanceHeaderTreatment,
  FinanceSourceTreatment,
} from "./types";

export const FINANCE_SAFE_AREA = {
  top: "6.5%",
  right: "7%",
  bottom: "8.5%",
  left: "7%",
};

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
  treatment?: FinanceSourceTreatment;
  dark?: boolean;
  complianceText?: string;
};

export const SourceStrip: React.FC<SourceStripProps> = ({
  sourceLabel,
  sourceDate,
  period,
  sampleData = false,
  treatment = "full",
  dark = false,
  complianceText,
}) => {
  const frame = useCurrentFrame();
  const opacity = reveal(frame, 10, 24);
  const hasSource = Boolean(sourceLabel || sourceDate || period || sampleData);
  if (!hasSource) return null;
  const compact = treatment === "compact";
  const inline = treatment === "inline";

  return (
    <div
      style={{
        position: "absolute",
        left: inline ? "57%" : "7%",
        right: "7%",
        bottom: complianceText ? "7.2%" : compact ? "3.8%" : "4.6%",
        borderTop: inline ? undefined : `2px solid ${dark ? "rgba(242,239,231,0.28)" : FINANCE_COLORS.line}`,
        paddingTop: inline ? 0 : compact ? 10 : 14,
        display: "grid",
        gridTemplateColumns: compact ? "1fr auto" : inline ? "1fr" : "112px 1fr auto",
        alignItems: "start",
        gap: compact ? 18 : 22,
        color: dark ? "rgba(242,239,231,0.7)" : FINANCE_COLORS.muted,
        fontSize: compact ? 18 : 19,
        opacity,
      }}
    >
      {!compact && <span style={{ fontFamily: FINANCE_MONO, letterSpacing: "0.09em", color: dark ? FINANCE_COLORS.ochre : FINANCE_COLORS.teal }}>SOURCE</span>}
      <div style={{ minWidth: 0 }}>
        {sourceLabel && <div style={{ fontSize: compact ? 18 : 22, lineHeight: 1.25, color: dark ? "#F2EFE7" : FINANCE_COLORS.ink }}>{sourceLabel}</div>}
        {(period || sourceDate) && (
          <div style={{ marginTop: sourceLabel ? 5 : 0, fontFamily: FINANCE_MONO, fontSize: compact ? 16 : 17, letterSpacing: "0.045em" }}>
            {[period, sourceDate].filter(Boolean).join("  ·  ")}
          </div>
        )}
      </div>
      {sampleData && (
        <span style={{ color: FINANCE_COLORS.vermillion, fontFamily: FINANCE_MONO, fontWeight: 700, letterSpacing: "0.06em", whiteSpace: "nowrap" }}>SAMPLE DATA</span>
      )}
      {complianceText && (
        <div style={{ position: "fixed", left: "7%", right: "7%", bottom: "3.1%", borderTop: `1px solid ${dark ? "rgba(242,239,231,0.2)" : FINANCE_COLORS.line}`, paddingTop: 10, textAlign: "center", fontSize: 18, lineHeight: 1.35, color: dark ? "rgba(242,239,231,0.72)" : FINANCE_COLORS.muted }}>
          {complianceText}
        </div>
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
  canvasMode?: FinanceCanvasMode;
  headerTreatment?: FinanceHeaderTreatment;
  sourceTreatment?: FinanceSourceTreatment;
  complianceText?: string;
}> = ({ eyebrow, children, source, theme, brand, canvasMode = "paper", headerTreatment = "full", sourceTreatment = "full", complianceText }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const grainOpacity = 0.018 + Math.sin(frame / 19) * 0.003;
  const scale = Math.min(width / 1080, height / 1920);
  const headerRight = [brand?.series, brand?.issue].filter(Boolean).join(" / ") || eyebrow || "";
  const dark = canvasMode === "dark-ink";
  const fullBleed = canvasMode === "full-bleed";
  const compactHeader = headerTreatment === "compact";
  const cssTokens = {
    "--finance-paper": dark ? "#171715" : theme?.backgroundColor,
    "--finance-ink": dark ? "#F2EFE7" : theme?.textColor,
    "--finance-muted": dark ? "#BEB8AB" : theme?.mutedTextColor,
    "--finance-accent": theme?.accentColor,
    "--finance-primary": theme?.primaryColor,
    "--finance-highlight": theme?.chartColors?.[2],
    "--finance-surface": dark ? "#242421" : theme?.surfaceColor,
    "--finance-line": dark ? "#4D4B45" : "#CEC8BA",
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
      {!fullBleed && <AbsoluteFill style={{ opacity: grainOpacity, backgroundImage: `repeating-linear-gradient(0deg, ${FINANCE_COLORS.ink} 0, ${FINANCE_COLORS.ink} 1px, transparent 1px, transparent 4px)`, backgroundSize: `${Math.max(3, 4 * scale)}px ${Math.max(3, 4 * scale)}px` }} />}
      {canvasMode === "document" && (
        <div style={{ position: "absolute", left: "8.5%", right: "4.5%", top: "9.5%", bottom: "7.5%", background: FINANCE_COLORS.surface, boxShadow: "0 8px 26px rgba(23,23,21,0.08)", borderLeft: `2px solid ${FINANCE_COLORS.line}` }}>
          <div style={{ position: "absolute", right: 24, top: 30, fontFamily: FINANCE_MONO, fontSize: 16, color: FINANCE_COLORS.muted }}>PAGE / 01</div>
        </div>
      )}
      {canvasMode === "data" && (
        <AbsoluteFill style={{ opacity: dark ? 0.11 : 0.055, backgroundImage: `linear-gradient(${FINANCE_COLORS.teal} 1px, transparent 1px), linear-gradient(90deg, ${FINANCE_COLORS.teal} 1px, transparent 1px)`, backgroundSize: "72px 72px", maskImage: "linear-gradient(to bottom, transparent 8%, black 34%, black 82%, transparent 96%)" }} />
      )}
      {canvasMode === "margin-note" && (
        <div style={{ position: "absolute", top: "10%", bottom: "10%", right: "7%", width: "31%", borderLeft: `2px solid ${FINANCE_COLORS.vermillion}`, background: dark ? "rgba(242,239,231,0.035)" : "rgba(180,71,54,0.035)" }} />
      )}
      {headerTreatment !== "none" && (
        <div style={{ position: "absolute", left: "7%", top: compactHeader ? "3.5%" : "4.6%", width: "86%", display: "flex", justifyContent: "space-between", alignItems: "center", fontFamily: FINANCE_MONO, fontSize: compactHeader ? 16 : 18, letterSpacing: compactHeader ? "0.055em" : "0.08em", color: FINANCE_COLORS.muted, opacity: reveal(frame, 0, 12) }}>
          <span>{compactHeader ? [brand?.label || "FINANCE DOSSIER", brand?.issue].filter(Boolean).join(" / ") : brand?.label || "FINANCE DOSSIER"}</span>
          {!compactHeader && <span>{headerRight}</span>}
          {compactHeader && eyebrow && <span style={{ color: FINANCE_COLORS.vermillion }}>{eyebrow.split(" /")[0]}</span>}
        </div>
      )}
      {children}
      {source && <SourceStrip {...source} treatment={sourceTreatment} dark={dark} complianceText={complianceText} />}
    </AbsoluteFill>
  );
};
