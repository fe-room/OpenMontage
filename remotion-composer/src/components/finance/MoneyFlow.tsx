import { useCurrentFrame } from "remotion";
import { EvidenceIndex } from "./EditorialMarks";
import { FINANCE_COLORS, FINANCE_MONO, FinanceFrame, reveal } from "./FinanceFrame";
import { FinanceTitle } from "./FinanceTitle";
import type { FinanceRenderContext, FlowEdge, FlowNode } from "./types";

export type MoneyFlowProps = FinanceRenderContext & {
  title?: string;
  nodes: FlowNode[];
  edges: FlowEdge[];
  highlightedPath?: string[];
  variant?: "vertical" | "horizontal" | "radial" | "split" | "sankey-lite";
};

type Point = { x: number; y: number };
const MIN_SANKEY_WIDTH = 8;
const MAX_SANKEY_WIDTH = 42;

export const sankeyStrokeWidth = (value: number | undefined, numericValues: number[]): number => {
  if (value === undefined || !Number.isFinite(value) || numericValues.length === 0) return 12;
  const min = Math.min(...numericValues);
  const max = Math.max(...numericValues);
  return min === max ? (MIN_SANKEY_WIDTH + MAX_SANKEY_WIDTH) / 2 : MIN_SANKEY_WIDTH + ((value - min) / (max - min)) * (MAX_SANKEY_WIDTH - MIN_SANKEY_WIDTH);
};

const sankeyPositions = (nodes: FlowNode[], edges: FlowEdge[]): Point[] => {
  const incoming = new Map(nodes.map((node) => [node.id, 0]));
  edges.forEach((edge) => incoming.set(edge.to, (incoming.get(edge.to) ?? 0) + 1));
  const depth = new Map(nodes.map((node) => [node.id, 0]));
  const queue = nodes.filter((node) => (incoming.get(node.id) ?? 0) === 0).map((node) => node.id);
  for (let cursor = 0; cursor < queue.length; cursor += 1) {
    const id = queue[cursor];
    edges.filter((edge) => edge.from === id).forEach((edge) => {
      depth.set(edge.to, Math.max(depth.get(edge.to) ?? 0, (depth.get(id) ?? 0) + 1));
      if (!queue.includes(edge.to)) queue.push(edge.to);
    });
  }
  const maxDepth = Math.max(1, ...depth.values());
  const columns = new Map<number, FlowNode[]>();
  nodes.forEach((node) => {
    const column = depth.get(node.id) ?? 0;
    columns.set(column, [...(columns.get(column) ?? []), node]);
  });
  const byId = new Map<string, Point>();
  columns.forEach((columnNodes, column) => columnNodes.forEach((node, index) => byId.set(node.id, {
    x: 145 + (column * 710) / maxDepth,
    y: 180 + ((index + 1) * 880) / (columnNodes.length + 1),
  })));
  return nodes.map((node) => byId.get(node.id) ?? { x: 145, y: 620 });
};

export const moneyFlowPositions = (nodes: FlowNode[], edges: FlowEdge[], variant: NonNullable<MoneyFlowProps["variant"]>): Point[] => {
  if (variant === "sankey-lite") return sankeyPositions(nodes, edges);
  if (variant === "radial") return nodes.map((_, index) => { const angle = -Math.PI / 2 + (index * Math.PI * 2) / Math.max(nodes.length, 1); return { x: 500 + Math.cos(angle) * 330, y: 620 + Math.sin(angle) * 410 }; });
  if (variant === "vertical") return nodes.map((_, index) => ({ x: 500, y: 150 + (index * 960) / Math.max(nodes.length - 1, 1) }));
  if (variant === "split") return nodes.map((_, index) => ({ x: index === 0 ? 500 : index % 2 ? 250 : 750, y: index === 0 ? 150 : 350 + Math.floor((index - 1) / 2) * 290 }));
  return nodes.map((_, index) => ({ x: 125 + (index * 750) / Math.max(nodes.length - 1, 1), y: 620 }));
};

const isHighlightedEdge = (path: string[], edge: FlowEdge) => path.some((id, index) => id === edge.from && path[index + 1] === edge.to);

const NodeLabel: React.FC<{ node: FlowNode; point: Point; active: boolean; sankey: boolean; sourceNode: boolean }> = ({ node, point, active, sankey, sourceNode }) => {
  const long = node.label.length > 16;
  const veryLong = node.label.length > 28;
  const width = sankey ? 240 : 230;
  const height = long ? 152 : 118;
  const x = point.x - width / 2;
  const y = point.y - height / 2;
  return (
    <g>
      {(!sankey || sourceNode) && <rect x={x} y={y} width={width} height={height} rx="3" fill={FINANCE_COLORS.surface} stroke={active ? FINANCE_COLORS.vermillion : FINANCE_COLORS.line} strokeWidth={active ? 4 : 2} />}
      {sankey && !sourceNode && <line x1={x} y1={y + height - 6} x2={x + width} y2={y + height - 6} stroke={active ? FINANCE_COLORS.vermillion : FINANCE_COLORS.line} strokeWidth={active ? 4 : 2} />}
      <foreignObject x={x + 10} y={y + 10} width={width - 20} height={height - 20}>
        <div style={{ width: "100%", height: "100%", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", textAlign: "center", overflow: "hidden", color: FINANCE_COLORS.ink }}>
          <div style={{ maxWidth: "100%", fontSize: veryLong ? 18 : long ? 20 : 27, lineHeight: 1.08, fontWeight: 700, overflowWrap: "normal", wordBreak: "keep-all" }}>{node.label}</div>
          {node.value !== undefined && node.value !== null && <div style={{ marginTop: 9, fontSize: 22, lineHeight: 1, fontFamily: FINANCE_MONO, color: active ? FINANCE_COLORS.vermillion : FINANCE_COLORS.muted }}>{node.value}</div>}
        </div>
      </foreignObject>
    </g>
  );
};

export const MoneyFlow: React.FC<MoneyFlowProps> = ({
  title = "资金流向", nodes, edges, highlightedPath = [], variant = "horizontal", theme, brand,
  canvasMode = variant === "sankey-lite" ? "data" : "paper",
  headerTreatment = canvasMode === "full-bleed" ? "none" : canvasMode === "data" ? "compact" : "full",
  sourceTreatment = canvasMode === "full-bleed" ? "inline" : "compact",
  evidenceIndex, sourceLabel, sourceDate, period, sampleData, complianceText,
}) => {
  const frame = useCurrentFrame();
  const positions = moneyFlowPositions(nodes, edges, variant);
  const pointById = Object.fromEntries(nodes.map((node, index) => [node.id, positions[index]]));
  const incoming = new Set(edges.map((edge) => edge.to));
  const numericValues = edges.map((edge) => edge.value).filter((value): value is number => value !== undefined && Number.isFinite(value));
  const sankey = variant === "sankey-lite";
  const source = { sourceLabel, sourceDate, period, sampleData };

  return (
    <FinanceFrame eyebrow="MONEY FLOW" source={source} theme={theme} brand={brand} canvasMode={canvasMode} headerTreatment={headerTreatment} sourceTreatment={sourceTreatment} complianceText={complianceText}>
      <div style={{ position: "absolute", inset: headerTreatment === "none" ? "7% 4.5% 9%" : "11% 4.5% 10%" }}>
        <div style={{ marginLeft: "2.5%" }}><EvidenceIndex label={evidenceIndex || "MONEY FLOW"} /><FinanceTitle preferredFontSize={52} minFontSize={38} maxWidth={900} style={{ marginTop: 16 }}>{title}</FinanceTitle></div>
        <svg viewBox="0 0 1000 1250" style={{ width: "100%", height: "86%", marginTop: 8, overflow: "visible" }}>
          <defs>
            <marker id="finance-arrow" markerUnits="userSpaceOnUse" markerWidth="17" markerHeight="17" refX="15" refY="8.5" orient="auto"><path d="M 0 0 L 17 8.5 L 0 17 z" fill={FINANCE_COLORS.teal} /></marker>
            <marker id="finance-arrow-active" markerUnits="userSpaceOnUse" markerWidth="17" markerHeight="17" refX="15" refY="8.5" orient="auto"><path d="M 0 0 L 17 8.5 L 0 17 z" fill={FINANCE_COLORS.vermillion} /></marker>
          </defs>
          {edges.map((edge, index) => {
            const from = pointById[edge.from];
            const to = pointById[edge.to];
            if (!from || !to) return null;
            const active = isHighlightedEdge(highlightedPath, edge);
            const progress = reveal(frame, 12 + index * 6, 34 + index * 6);
            const width = sankey ? sankeyStrokeWidth(edge.value, numericValues) : active ? 9 : 5;
            const horizontal = Math.abs(to.x - from.x) >= Math.abs(to.y - from.y);
            const startX = horizontal ? from.x + 118 : from.x;
            const startY = horizontal ? from.y : from.y + 68;
            const endX = horizontal ? to.x - 118 : to.x;
            const endY = horizontal ? to.y : to.y - 68;
            const path = sankey ? `M ${startX} ${startY} C ${(startX + endX) / 2} ${startY}, ${(startX + endX) / 2} ${endY}, ${endX} ${endY}` : `M ${startX} ${startY} L ${endX} ${endY}`;
            const label = edge.label ?? (edge.value !== undefined ? String(edge.value) : undefined);
            const labelX = startX + (endX - startX) * 0.58;
            const labelY = startY + (endY - startY) * 0.58 - 18;
            return <g key={`${edge.from}-${edge.to}-${index}`} opacity={progress}><path d={path} fill="none" stroke={active ? FINANCE_COLORS.vermillion : FINANCE_COLORS.teal} strokeWidth={width} strokeOpacity={active ? 0.92 : 0.62} strokeLinecap="round" markerEnd={active ? "url(#finance-arrow-active)" : "url(#finance-arrow)"} />{label && progress > 0.75 && <g><rect x={labelX - 42} y={labelY - 23} width="84" height="36" rx="2" fill={FINANCE_COLORS.paper} fillOpacity="0.94" /><text x={labelX} y={labelY + 3} textAnchor="middle" fontFamily={FINANCE_MONO} fontSize="20" fontWeight="700" fill={active ? FINANCE_COLORS.vermillion : FINANCE_COLORS.muted}>{label}</text></g>}</g>;
          })}
          {nodes.map((node, index) => {
            const point = positions[index];
            const active = highlightedPath.includes(node.id);
            return <g key={node.id} opacity={reveal(frame, index * 5, 16 + index * 5)}><NodeLabel node={node} point={point} active={active} sankey={sankey} sourceNode={!incoming.has(node.id)} /></g>;
          })}
        </svg>
      </div>
    </FinanceFrame>
  );
};
