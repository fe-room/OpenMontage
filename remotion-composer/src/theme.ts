export type ThemeConfig = {
  primaryColor: string;
  accentColor: string;
  backgroundColor: string;
  surfaceColor: string;
  textColor: string;
  mutedTextColor: string;
  headingFont: string;
  bodyFont: string;
  monoFont: string;
  chartColors: string[];
  springConfig: { damping: number; stiffness: number; mass: number };
  transitionDuration: number;
  captionHighlightColor: string;
  captionBackgroundColor: string;
};

export const THEMES: Record<string, ThemeConfig> = {
  "clean-professional": {
    primaryColor: "#2563EB", accentColor: "#F59E0B", backgroundColor: "#FFFFFF",
    surfaceColor: "#F9FAFB", textColor: "#1F2937", mutedTextColor: "#6B7280",
    headingFont: "Inter", bodyFont: "Inter", monoFont: "JetBrains Mono",
    chartColors: ["#2563EB", "#F59E0B", "#10B981", "#8B5CF6", "#EC4899", "#06B6D4"],
    springConfig: { damping: 20, stiffness: 120, mass: 1 }, transitionDuration: 0.4,
    captionHighlightColor: "#2563EB", captionBackgroundColor: "rgba(255, 255, 255, 0.85)",
  },
  "flat-motion-graphics": {
    primaryColor: "#7C3AED", accentColor: "#EC4899", backgroundColor: "#0F172A",
    surfaceColor: "#1E293B", textColor: "#F8FAFC", mutedTextColor: "#94A3B8",
    headingFont: "Space Grotesk", bodyFont: "Space Grotesk", monoFont: "Fira Code",
    chartColors: ["#7C3AED", "#EC4899", "#06B6D4", "#F59E0B", "#10B981", "#EF4444"],
    springConfig: { damping: 12, stiffness: 80, mass: 1 }, transitionDuration: 0.3,
    captionHighlightColor: "#22D3EE", captionBackgroundColor: "rgba(15, 23, 42, 0.75)",
  },
  "minimalist-diagram": {
    primaryColor: "#1A1A2E", accentColor: "#E94560", backgroundColor: "#FAFAFA",
    surfaceColor: "#FFFFFF", textColor: "#1A1A2E", mutedTextColor: "#6B7280",
    headingFont: "IBM Plex Sans", bodyFont: "IBM Plex Sans", monoFont: "IBM Plex Mono",
    chartColors: ["#E94560", "#1A1A2E", "#0F3460", "#9CA3AF"],
    springConfig: { damping: 25, stiffness: 150, mass: 1 }, transitionDuration: 0.5,
    captionHighlightColor: "#E94560", captionBackgroundColor: "rgba(250, 250, 250, 0.9)",
  },
  "anime-ghibli": {
    primaryColor: "#2D5016", accentColor: "#FFB347", backgroundColor: "#0A0A1A",
    surfaceColor: "#1A2332", textColor: "#F0E6D3", mutedTextColor: "#A8957E",
    headingFont: "Noto Serif JP", bodyFont: "Noto Sans", monoFont: "Fira Code",
    chartColors: ["#FFB347", "#2D5016", "#FF6B9D", "#A8E6CF", "#6B4C8A", "#E8927C"],
    springConfig: { damping: 18, stiffness: 60, mass: 1 }, transitionDuration: 1,
    captionHighlightColor: "#FFB347", captionBackgroundColor: "rgba(10, 10, 26, 0.8)",
  },
  // Direct Studio/demo fallback. Production renders receive a resolved
  // themeConfig from the active playbook and can override every token.
  "finance-dossier": {
    primaryColor: "#345C5B", accentColor: "#B44736", backgroundColor: "#F2EFE7",
    surfaceColor: "#F8F5ED", textColor: "#171715", mutedTextColor: "#6C6860",
    headingFont: '"Noto Sans SC", "Source Han Sans SC", "PingFang SC", sans-serif',
    bodyFont: '"Noto Sans SC", "Source Han Sans SC", "PingFang SC", sans-serif',
    monoFont: '"IBM Plex Mono", "SFMono-Regular", Consolas, monospace',
    chartColors: ["#345C5B", "#B44736", "#C5A64A", "#171715", "#6C6860"],
    springConfig: { damping: 200, stiffness: 100, mass: 1 }, transitionDuration: 0.3,
    captionHighlightColor: "#B44736", captionBackgroundColor: "rgba(242, 239, 231, 0.92)",
  },
};

export const DEFAULT_THEME = THEMES["flat-motion-graphics"];

export const resolveTheme = (props: Record<string, unknown>): ThemeConfig => {
  // A fully resolved per-project theme is authoritative over named presets.
  if (props.themeConfig && typeof props.themeConfig === "object") {
    return { ...DEFAULT_THEME, ...(props.themeConfig as Partial<ThemeConfig>) };
  }
  const themeName = (props.theme as string) || (props.playbook as string);
  return (themeName && THEMES[themeName]) || DEFAULT_THEME;
};
