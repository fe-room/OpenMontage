import { useCurrentFrame } from "remotion";
import { FINANCE_COLORS, FINANCE_MONO, FinanceFrame, reveal } from "./FinanceFrame";
import type { FinanceRenderContext, FlowEdge, FlowNode } from "./types";

export type MoneyFlowProps = FinanceRenderContext & { title?: string; nodes: FlowNode[]; edges: FlowEdge[]; highlightedPath?: string[]; variant?: "vertical" | "horizontal" | "radial" | "split" | "sankey-lite" };
type Point = { x: number; y: number };
const MIN_SANKEY_WIDTH = 6;
const MAX_SANKEY_WIDTH = 34;

export const sankeyStrokeWidth = (value: number | undefined, numericValues: number[]): number => {
  if (value === undefined || !Number.isFinite(value) || numericValues.length === 0) return 10;
  const min = Math.min(...numericValues); const max = Math.max(...numericValues);
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
  nodes.forEach((node) => { const column = depth.get(node.id) ?? 0; columns.set(column, [...(columns.get(column) ?? []), node]); });
  const byId = new Map<string, Point>();
  columns.forEach((columnNodes, column) => columnNodes.forEach((node, index) => byId.set(node.id, { x: 150 + (column * 700) / maxDepth, y: 230 + ((index + 1) * 790) / (columnNodes.length + 1) })));
  return nodes.map((node) => byId.get(node.id) ?? { x: 150, y: 620 });
};

export const moneyFlowPositions = (nodes: FlowNode[], edges: FlowEdge[], variant: NonNullable<MoneyFlowProps["variant"]>): Point[] => {
  if (variant === "sankey-lite") return sankeyPositions(nodes, edges);
  if (variant === "radial") return nodes.map((_, index) => { const angle = -Math.PI / 2 + (index * Math.PI * 2) / Math.max(nodes.length, 1); return { x: 500 + Math.cos(angle) * 330, y: 620 + Math.sin(angle) * 390 }; });
  if (variant === "vertical") return nodes.map((_, index) => ({ x: 500, y: 150 + (index * 930) / Math.max(nodes.length - 1, 1) }));
  if (variant === "split") return nodes.map((_, index) => ({ x: index === 0 ? 500 : index % 2 ? 250 : 750, y: index === 0 ? 170 : 340 + Math.floor((index - 1) / 2) * 260 }));
  return nodes.map((_, index) => ({ x: 120 + (index * 760) / Math.max(nodes.length - 1, 1), y: 600 }));
};
const isHighlightedEdge = (path: string[], edge: FlowEdge) => path.some((id, index) => id === edge.from && path[index + 1] === edge.to);

export const MoneyFlow: React.FC<MoneyFlowProps> = ({ title = "Where the value moves", nodes, edges, highlightedPath = [], variant = "horizontal", theme, brand, ...source }) => {
  const frame = useCurrentFrame(); const positions = moneyFlowPositions(nodes, edges, variant);
  const pointById = Object.fromEntries(nodes.map((node, index) => [node.id, positions[index]]));
  const numericValues = edges.map((edge) => edge.value).filter((value): value is number => value !== undefined && Number.isFinite(value));
  return <FinanceFrame eyebrow={`MONEY FLOW / ${variant.toUpperCase()}`} source={source} theme={theme} brand={brand}>
    <div style={{ position: "absolute", inset: "12% 5.5% 11%" }}><h1 style={{ margin: "0 0 22px 20px", fontSize: 50 }}>{title}</h1><svg viewBox="0 0 1000 1250" style={{ width: "100%", height: "88%" }}>
      <defs><marker id="finance-arrow" markerUnits="userSpaceOnUse" markerWidth="22" markerHeight="22" refX="20" refY="11" orient="auto"><path d="M 0 0 L 22 11 L 0 22 z" fill={FINANCE_COLORS.teal} /></marker><marker id="finance-arrow-active" markerUnits="userSpaceOnUse" markerWidth="22" markerHeight="22" refX="20" refY="11" orient="auto"><path d="M 0 0 L 22 11 L 0 22 z" fill={FINANCE_COLORS.vermillion} /></marker></defs>
      {edges.map((edge, index) => { const from = pointById[edge.from]; const to = pointById[edge.to]; if (!from || !to) return null; const active = isHighlightedEdge(highlightedPath, edge); const progress = reveal(frame, 12 + index * 6, 34 + index * 6); const width = variant === "sankey-lite" ? sankeyStrokeWidth(edge.value, numericValues) : active ? 10 : 5; const startX = from.x + 120; const endX = to.x - 120; const path = variant === "sankey-lite" ? `M ${startX} ${from.y} C ${(startX + endX) / 2} ${from.y}, ${(startX + endX) / 2} ${to.y}, ${endX} ${to.y}` : `M ${from.x} ${from.y} L ${to.x} ${to.y}`; return <g key={`${edge.from}-${edge.to}-${index}`} opacity={progress}><path d={path} fill="none" stroke={active ? FINANCE_COLORS.vermillion : FINANCE_COLORS.teal} strokeWidth={width} strokeOpacity={active ? 0.9 : 0.55} strokeLinecap="round" markerEnd={active ? "url(#finance-arrow-active)" : "url(#finance-arrow)"} />{edge.label && progress > 0.75 && <text x={(from.x + to.x) / 2} y={(from.y + to.y) / 2 - 18} textAnchor="middle" fontFamily={FINANCE_MONO} fontSize="22" fill={FINANCE_COLORS.muted} stroke={FINANCE_COLORS.paper} strokeWidth="8" paintOrder="stroke">{edge.label}</text>}</g>; })}
      {nodes.map((node, index) => { const point = positions[index]; const active = highlightedPath.includes(node.id); return <g key={node.id} opacity={reveal(frame, index * 5, 16 + index * 5)}><rect x={point.x - 115} y={point.y - 60} width="230" height="120" rx="4" fill={FINANCE_COLORS.surface} stroke={active ? FINANCE_COLORS.vermillion : FINANCE_COLORS.line} strokeWidth={active ? 5 : 2} /><text x={point.x} y={point.y - 5} textAnchor="middle" fontSize="28" fontWeight="700" fill={FINANCE_COLORS.ink}>{node.label}</text>{node.value !== undefined && node.value !== null && <text x={point.x} y={point.y + 34} textAnchor="middle" fontSize="23" fontFamily={FINANCE_MONO} fill={FINANCE_COLORS.muted}>{node.value}</text>}</g>; })}
    </svg></div>
  </FinanceFrame>;
};
