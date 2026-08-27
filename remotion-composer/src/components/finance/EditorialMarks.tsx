import { useCurrentFrame } from "remotion";
import { FINANCE_COLORS, FINANCE_MONO, reveal } from "./FinanceFrame";

export const EvidenceIndex: React.FC<{ label?: string }> = ({ label = "EVIDENCE" }) => (
  <div style={{ fontFamily: FINANCE_MONO, fontSize: 18, letterSpacing: "0.1em", color: FINANCE_COLORS.vermillion }}>
    {label}
  </div>
);

export const AnalystNote: React.FC<{ children: React.ReactNode; label?: string; compact?: boolean }> = ({
  children,
  label = "NOTE",
  compact = false,
}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ display: "grid", gridTemplateColumns: "24px 1fr", gap: compact ? 12 : 18, maxWidth: compact ? 360 : 620, opacity: reveal(frame, 20, 36) }}>
      <svg width="24" height={compact ? 70 : 96} viewBox="0 0 24 96" aria-hidden="true">
        <path d="M20 2 H8 V94 H20" fill="none" stroke={FINANCE_COLORS.vermillion} strokeWidth="3" />
      </svg>
      <div>
        <div style={{ fontFamily: FINANCE_MONO, fontSize: 17, letterSpacing: "0.09em", color: FINANCE_COLORS.vermillion }}>{label}</div>
        <div style={{ marginTop: 8, fontSize: compact ? 22 : 27, lineHeight: 1.45, fontWeight: 600 }}>{children}</div>
      </div>
    </div>
  );
};

export const UnderlineMark: React.FC<{ width?: number; delay?: number }> = ({ width = 220, delay = 10 }) => {
  const frame = useCurrentFrame();
  const progress = reveal(frame, delay, delay + 16);
  return (
    <svg width={width} height="18" viewBox={`0 0 ${width} 18`} aria-hidden="true">
      <path d={`M2 9 C ${width * 0.32} 3, ${width * 0.66} 15, ${width - 2} 7`} fill="none" stroke={FINANCE_COLORS.vermillion} strokeWidth="4" strokeLinecap="round" pathLength="1" strokeDasharray="1" strokeDashoffset={1 - progress} />
    </svg>
  );
};

export const BracketMark: React.FC<{ height?: number; width?: number }> = ({ height = 210, width = 118 }) => (
  <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} aria-hidden="true">
    <path d={`M4 4 H${width - 6} V${height - 4} H4`} fill="none" stroke={FINANCE_COLORS.vermillion} strokeWidth="5" />
  </svg>
);
