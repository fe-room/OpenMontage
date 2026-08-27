import { FINANCE_SANS } from "./FinanceFrame";

export type FinanceTitleProps = {
  children: string;
  maxLines?: number;
  preferredFontSize?: number;
  minFontSize?: number;
  lineHeight?: number;
  maxWidth?: number;
  color?: string;
  style?: React.CSSProperties;
};

const isCjk = (character: string) => /[\u3400-\u9fff\uf900-\ufaff]/.test(character);

const textUnits = (text: string): number =>
  [...text].reduce((total, character) => {
    if (isCjk(character)) return total + 1;
    if (/\s/.test(character)) return total + 0.32;
    if (/[A-Z0-9]/.test(character)) return total + 0.64;
    return total + 0.54;
  }, 0);

const semanticBreaks = (text: string): number[] => {
  const breaks = new Set<number>();
  const patterns = [/\s[|·/]\s/g, /\s(?:vs\.?|VS\.?)\s/g, /[，。；：？！]/g, /\s[—–-]\s/g, /\s+/g];
  patterns.forEach((pattern) => {
    for (const match of text.matchAll(pattern)) {
      breaks.add((match.index ?? 0) + match[0].length);
    }
  });
  return [...breaks].filter((index) => index > 1 && index < text.length - 1);
};

const avoidChineseOrphan = (lines: string[]): string[] => {
  if (lines.length < 2) return lines;
  const result = [...lines];
  const last = result[result.length - 1].trim();
  const previous = result[result.length - 2].trimEnd();
  if ([...last].length === 1 && isCjk(last) && [...previous].length > 2) {
    const previousChars = [...previous];
    result[result.length - 2] = previousChars.slice(0, -1).join("").trimEnd();
    result[result.length - 1] = `${previousChars[previousChars.length - 1]}${last}`;
  }
  return result.map((line) => line.replace(/^[|·/]\s*/, "").replace(/\s*[|·/]$/, "").trim());
};

export const layoutFinanceTitle = (
  text: string,
  maxWidth: number,
  preferredFontSize: number,
  minFontSize: number,
  maxLines: number,
): { fontSize: number; lines: string[] } => {
  const clean = text.replace(/\s+/g, " ").trim();
  if (!clean) return { fontSize: preferredFontSize, lines: [""] };

  // Preserve a single line when a modest (at most 8px) reduction is enough.
  // This follows the finance hierarchy: slight size adjustment before wrapping.
  for (let fontSize = preferredFontSize; fontSize >= Math.max(minFontSize, preferredFontSize - 8); fontSize -= 2) {
    if (textUnits(clean) <= maxWidth / fontSize) return { fontSize, lines: [clean] };
  }

  for (let fontSize = preferredFontSize; fontSize >= minFontSize; fontSize -= 2) {
    const maxUnits = maxWidth / fontSize;
    if (textUnits(clean) <= maxUnits) return { fontSize, lines: [clean] };
    if (maxLines < 2) continue;

    const candidates = semanticBreaks(clean);
    const midpoint = textUnits(clean) / 2;
    const ranked = candidates.sort((a, b) =>
      Math.abs(textUnits(clean.slice(0, a)) - midpoint) - Math.abs(textUnits(clean.slice(0, b)) - midpoint)
    );
    for (const boundary of ranked) {
      const left = clean.slice(0, boundary).trim().replace(/[|·/]$/, "").trim();
      let right = clean.slice(boundary).trim();
      if (/^(?:vs\.?|VS\.?)\b/.test(clean.slice(boundary).trim())) right = clean.slice(boundary).trim();
      const lines = avoidChineseOrphan([left, right]);
      if (lines.every((line) => textUnits(line) <= maxUnits)) return { fontSize, lines };
    }

    const characters = [...clean];
    let best = 1;
    for (let index = 1; index < characters.length; index += 1) {
      if (textUnits(characters.slice(0, index).join("")) <= maxUnits) best = index;
    }
    const lines = avoidChineseOrphan([
      characters.slice(0, best).join("").trim(),
      characters.slice(best).join("").trim(),
    ]);
    if (lines.every((line) => textUnits(line) <= maxUnits)) return { fontSize, lines };
  }

  return { fontSize: minFontSize, lines: avoidChineseOrphan([clean]) };
};

export const FinanceTitle: React.FC<FinanceTitleProps> = ({
  children,
  maxLines = 2,
  preferredFontSize = 54,
  minFontSize = 38,
  lineHeight = 1.12,
  maxWidth = 900,
  color,
  style,
}) => {
  const { fontSize, lines } = layoutFinanceTitle(children, maxWidth, preferredFontSize, minFontSize, maxLines);
  return (
    <h1
      style={{
        margin: 0,
        width: maxWidth,
        maxWidth: "100%",
        fontFamily: FINANCE_SANS,
        fontSize,
        lineHeight,
        fontWeight: 700,
        letterSpacing: fontSize < preferredFontSize ? "-0.025em" : "-0.015em",
        color,
        ...style,
      }}
    >
      {lines.map((line, index) => (
        <span key={`${line}-${index}`} style={{ display: "block", whiteSpace: "nowrap" }}>{line}</span>
      ))}
    </h1>
  );
};
