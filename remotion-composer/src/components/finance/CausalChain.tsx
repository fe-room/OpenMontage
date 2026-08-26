import { useCurrentFrame } from "remotion";
import { FINANCE_COLORS, FINANCE_MONO, FinanceFrame, reveal } from "./FinanceFrame";
import type { CausalEdge, CausalNode, SourceContext } from "./types";

export type CausalChainProps = SourceContext & {
  title?: string;
  nodes: CausalNode[];
  edges: CausalEdge[];
  activeNodeId?: string;
  hypothesis?: boolean;
  variant?: "linear" | "branching";
};

export const CausalChain: React.FC<CausalChainProps> = ({
  title = "How the mechanism may work",
  nodes,
  edges,
  activeNodeId,
  hypothesis = false,
  variant = "linear",
  ...source
}) => {
  const frame = useCurrentFrame();
  const positions = Object.fromEntries(
    nodes.map((node, index) => [
      node.id,
      variant === "branching"
        ? { x: index === 0 ? 500 : index % 2 ? 260 : 740, y: index === 0 ? 170 : 330 + Math.floor((index - 1) / 2) * 250 }
        : { x: 500, y: 150 + (index * 940) / Math.max(nodes.length - 1, 1) },
    ])
  );

  return (
    <FinanceFrame eyebrow={hypothesis ? "MECHANISM / HYPOTHESIS" : "MECHANISM / CAUSAL CHAIN"} source={source}>
      <div style={{ position: "absolute", inset: "12% 6% 11%" }}>
        <h1 style={{ margin: "0 0 18px", fontSize: 48 }}>{title}</h1>
        {hypothesis && (
          <div style={{ color: FINANCE_COLORS.vermillion, fontFamily: FINANCE_MONO, fontSize: 20 }}>
            HYPOTHESIS — CORRELATION ALONE DOES NOT ESTABLISH CAUSALITY
          </div>
        )}
        <svg viewBox="0 0 1000 1250" style={{ width: "100%", height: "86%" }}>
          <defs>
            <marker id="causal-arrow" markerUnits="userSpaceOnUse" markerWidth="20" markerHeight="20" refX="18" refY="10" orient="auto">
              <path d="M 0 0 L 20 10 L 0 20 z" fill={FINANCE_COLORS.muted} />
            </marker>
          </defs>
          {edges.map((edge, index) => {
            const from = positions[edge.from];
            const to = positions[edge.to];
            if (!from || !to) return null;
            const uncertain = edge.relation === "uncertain" || hypothesis;
            const sign = edge.relation === "positive" ? "+" : edge.relation === "negative" ? "−" : "?";
            return (
              <g key={`${edge.from}-${edge.to}-${index}`} opacity={reveal(frame, 12 + index * 6, 28 + index * 6)}>
                <line
                  x1={from.x}
                  y1={from.y + 62}
                  x2={to.x}
                  y2={to.y - 70}
                  stroke={edge.relation === "negative" ? FINANCE_COLORS.vermillion : FINANCE_COLORS.teal}
                  strokeWidth="5"
                  strokeDasharray={uncertain ? "12 10" : undefined}
                  markerEnd="url(#causal-arrow)"
                />
                <text x={(from.x + to.x) / 2 + 18} y={(from.y + to.y) / 2} fontFamily={FINANCE_MONO} fontSize="28" fill={FINANCE_COLORS.vermillion}>
                  {sign} {edge.label ?? ""}
                </text>
              </g>
            );
          })}
          {nodes.map((node, index) => {
            const point = positions[node.id];
            const active = node.id === activeNodeId;
            return (
              <g key={node.id} opacity={reveal(frame, index * 6, 18 + index * 6)}>
                <rect x={point.x - 260} y={point.y - 66} width="520" height="132" rx="3" fill={active ? "#E6DDD0" : FINANCE_COLORS.surface} stroke={active ? FINANCE_COLORS.vermillion : FINANCE_COLORS.line} strokeWidth={active ? 5 : 2} />
                <text x={point.x} y={point.y - 5} textAnchor="middle" fontSize="31" fontWeight="700" fill={FINANCE_COLORS.ink}>{node.label}</text>
                {node.detail && <text x={point.x} y={point.y + 35} textAnchor="middle" fontSize="21" fill={FINANCE_COLORS.muted}>{node.detail}</text>}
              </g>
            );
          })}
        </svg>
      </div>
    </FinanceFrame>
  );
};
