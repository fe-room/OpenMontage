import React from "react";
import { C, FONT_SANS, FONT_SERIF, easeSettle, clamp01 } from "./theme";

// ---------------------------------------------------------------------------
// 四张选项纸卡 —— 本片的「论证装置」，不是装饰。
// 它只出现在论证确实需要它的几拍（建立集合 / 互斥约束 / 高亮最佳替代 / 熄灭相加）。
// 它不是可复用场景模板：每场对它的用法（落纸、抬起、变暗、熄灭）都不同。
// ---------------------------------------------------------------------------

export const CARD_W = 196;
export const CARD_H = 240;
export const CARD_GAP = 22;
const TOTAL = CARD_W * 4 + CARD_GAP * 3;
export const CARD_X = [0, 1, 2, 3].map((i) => (1080 - TOTAL) / 2 + i * (CARD_W + CARD_GAP));

export type CardState = {
  /** 0 = 未出现，1 = 完全落定 */
  enter?: number;
  /** 抬起高度 px */
  lift?: number;
  /** 变暗 0..1 */
  dim?: number;
  /** 熄灭（失去对比度并下沉）0..1 */
  extinguish?: number;
  /** 被选中：抬厚 + 完全点亮 */
  selected?: boolean;
  /** 卡面浮出的标签 */
  tag?: string;
  /** 标签下的数值行 */
  value?: string;
  tagProgress?: number;
  valueProgress?: number;
};

const Card: React.FC<{ index: number; label: string; state: CardState }> = ({
  index,
  label,
  state,
}) => {
  const {
    enter = 1,
    lift = 0,
    dim = 0,
    extinguish = 0,
    selected = false,
    tag,
    value,
    tagProgress = 0,
    valueProgress = 0,
  } = state;
  const e = easeSettle(enter);
  const drop = (1 - e) * 140;
  const rot = [-0.9, 0.6, -0.5, 0.85][index];
  const sink = extinguish * 46;
  const opacity = clamp01(enter) * (1 - dim * 0.6) * (1 - extinguish * 0.72);
  return (
    <div
      style={{
        position: "absolute",
        left: CARD_X[index],
        top: 990 + drop + sink,
        width: CARD_W,
        height: CARD_H,
        background: C.paper,
        border: `1px solid rgba(34,32,28,${selected ? 0.30 : 0.16})`,
        boxShadow: selected
          ? `0 ${12 + lift}px ${26 + lift * 2}px rgba(34,32,28,0.22)`
          : `0 ${3 + lift}px ${11 + lift}px rgba(34,32,28,${0.08 + lift * 0.01})`,
        transform: `rotate(${rot}deg) translateY(${-lift}px)`,
        opacity,
        filter: dim > 0.4 || extinguish > 0.4 ? "saturate(0.45)" : "none",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 22,
          left: 0,
          right: 0,
          textAlign: "center",
          fontFamily: FONT_SANS,
          fontSize: 26,
          letterSpacing: 4,
          color: C.inkFaint,
          opacity: 0.9,
        }}
      >
        {"ABCD"[index]}
      </div>
      <div
        style={{
          position: "absolute",
          top: 84,
          left: 10,
          right: 10,
          textAlign: "center",
          fontFamily: FONT_SERIF,
          fontSize: 32,
          lineHeight: 1.3,
          letterSpacing: 1,
          color: C.ink,
          whiteSpace: "nowrap",
        }}
      >
        {label}
      </div>
      {tag ? (
        <div
          style={{
            position: "absolute",
            left: -10,
            right: -10,
            top: -70,
            textAlign: "center",
            fontFamily: FONT_SERIF,
            fontSize: 30,
            letterSpacing: 3,
            color: C.ink,
            opacity: tagProgress,
            transform: `translateY(${(1 - tagProgress) * 14}px)`,
            whiteSpace: "nowrap",
          }}
        >
          {tag}
        </div>
      ) : null}
      {value ? (
        <div
          style={{
            position: "absolute",
            left: -34,
            right: -34,
            top: CARD_H + 26,
            textAlign: "center",
            fontFamily: FONT_SERIF,
            fontSize: 30,
            letterSpacing: 2,
            color: C.inkSoft,
            opacity: valueProgress,
            transform: `translateY(${(1 - valueProgress) * 12}px)`,
            whiteSpace: "nowrap",
          }}
        >
          {value}
        </div>
      ) : null}
    </div>
  );
};

export const OPTION_LABELS = ["在家休息", "拍一期视频", "接一个兼职", "去健身"];

export const OptionCards: React.FC<{ states: CardState[] }> = ({ states }) => (
  <>
    {OPTION_LABELS.map((label, i) => (
      <Card key={label} index={i} label={label} state={states[i] ?? {}} />
    ))}
  </>
);
