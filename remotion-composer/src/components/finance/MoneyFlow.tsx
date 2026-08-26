import { interpolate, useCurrentFrame } from "remotion";
import { FINANCE_COLORS, FINANCE_MONO, FinanceFrame, reveal } from "./FinanceFrame";
import type { FlowEdge, FlowNode, SourceContext } from "./types";

export type MoneyFlowProps = SourceContext & {
  title?: string;
  nodes: FlowNode[];
  edges: FlowEdge[];
  highlightedPath?: string[];
  variant?: "vertical" | "horizontal" | "radial" | "split" | "sankey-lite";
};

type Point = { x: number; y: number };

const positionsFor = (nodes: FlowNode[], variant: NonNullable<MoneyFlowProps["variant"]>): Point[] => {
  if (variant === "radial") {
    return nodes.map((_, index) => {
      const angle = -Math.PI / 2 + (index * Math.PI * 2) / Math.max(nodes.length, 1);
      return { x: 500 + Math.cos(angle) * 330, y: 620 + Math.sin(angle) * 390 };
    });
  }
  if (variant === "vertical") {
    return nodes.map((_, index) => ({ x: 500, y: 150 + (index * 930) / Math.max(nodes.length - 1, 1) }));
  }
  if (variant === "split") {
    return nodes.map((_, index) => ({
      x: index === 0 ? 500 : index % 2 ? 250 : 750,
      y: index === 0 ? 170 : 340 + Math.floor((index - 1) / 2) * 260,
    }));
  }
  return nodes.map((_, index) => ({ x: 120 + (index * 760) / Math.max(nodes.length - 1, 1), y: 600 }));
};

export const MoneyFlow: React.FC<MoneyFlowProps> = ({
  title = "Where the value moves",
  nodes,
  edges,
  highlightedPath = [],
  variant = "horizontal",
  ...source
}) => {
  const frame = useCurrentFrame();
  const positions = positionsFor(nodes, variant);
  const pointById = Object.fromEntries(nodes.map((node, index) => [node.id, positions[index]]));

  return (
    <FinanceFrame eyebrow={`MONEY FLOW / ${variant.toUpperCase()}`} source={source}>
      <div style={{ position: "absolute", inset: "12% 5.5% 11%" }}>
        <h1 style={{ margin: "0 0 22px 20px", fontSize: 50 }}>{title}</h1>
        <svg viewBox="0 0 1000 1250" style={{ width: "100%", height: "88%" }}>
          <defs>
            <marker id="finance-arrow" markerUnits="userSpaceOnUse" markerWidth="22" markerHeight="22" refX="20" refY="11" orient="auto">
              <path d="M 0 0 L 22 11 L 0 22 z" fill={FINANCE_COLORS.teal} />
            </marker>
          </defs>
          {edges.map((edge, index) => {
            const from = pointById[edge.from];
            const to = pointById[edge.to];
            if (!from || !to) return null;
            const distance = Math.hypot(to.x - from.x, to.y - from.y) || 1;
            const ux = (to.x - from.x) / distance;
            const uy = (to.y - from.y) / distance;
            const start = { x: from.x + ux * 72, y: from.y + uy * 72 };
            const end = { x: to.x - ux * 78, y: to.y - uy * 78 };
            const active = highlightedPath.includes(edge.from) && highlightedPath.includes(edge.to);
            const progress = reveal(frame, 12 + index * 6, 34 + index * 6);
            const x2 = interpolate(progress, [0, 1], [start.x, end.x]);
            const y2 = interpolate(progress, [0, 1], [start.y, end.y]);
            const strokeWidth = variant === "sankey-lite" ? Math.max(5, Math.min(28, edge.value ?? 8)) : active ? 10 : 5;
            return (
              <g key={`${edge.from}-${edge.to}-${index}`}>
                <line
                  x1={start.x}
                  y1={start.y}
                  x2={x2}
                  y2={y2}
                  stroke={active ? FINANCE_COLORS.vermillion : FINANCE_COLORS.teal}
                  strokeWidth={strokeWidth}
                  strokeOpacity={active ? 0.9 : 0.48}
                  markerEnd="url(#finance-arrow)"
                />
                {edge.label && progress > 0.75 && (
                  <text
                    x={(from.x + to.x) / 2}
                    y={(from.y + to.y) / 2 - 18}
                    textAnchor="middle"
                    fontFamily={FINANCE_MONO}
                    fontSize="22"
                    fill={FINANCE_COLORS.muted}
                  >
                    {edge.label}
                  </text>
                )}
              </g>
            );
          })}
          {nodes.map((node, index) => {
            const point = positions[index];
            const opacity = reveal(frame, index * 5, 16 + index * 5);
            return (
              <g key={node.id} opacity={opacity}>
                <rect
                  x={point.x - 115}
                  y={point.y - 60}
                  width="230"
                  height="120"
                  rx="4"
                  fill={FINANCE_COLORS.surface}
                  stroke={highlightedPath.includes(node.id) ? FINANCE_COLORS.vermillion : FINANCE_COLORS.line}
                  strokeWidth={highlightedPath.includes(node.id) ? 5 : 2}
                />
                <text x={point.x} y={point.y - 5} textAnchor="middle" fontSize="28" fontWeight="700" fill={FINANCE_COLORS.ink}>
                  {node.label}
                </text>
                {node.value && (
                  <text x={point.x} y={point.y + 34} textAnchor="middle" fontSize="23" fontFamily={FINANCE_MONO} fill={FINANCE_COLORS.muted}>
                    {node.value}
                  </text>
                )}
              </g>
            );
          })}
        </svg>
      </div>
    </FinanceFrame>
  );
};
