import React from "react";
import { C, FONT_MONO, FONT_SANS, clamp01, easeOutCubic, easeSettle } from "./theme";
import { InvertTag, Kicker, Plate, Rule, land, useLocal } from "./Foundation";
import {
  DATES,
  DRAWDOWN,
  FUNDS,
  INDEX_MAX,
  MECHANISM,
  METRICS,
  UNDERWATER,
} from "./timeline";

// ---------------------------------------------------------------------------
// sc07 规则不同，路径不同 —— 全片唯一的机制镜头
// 两栏规则对照 + 明确的限定文字，不使用单条确定箭头。
// ---------------------------------------------------------------------------
const RuleColumn: React.FC<{
  x: number;
  title: string;
  rule: string;
  codes: string[];
  names: string[];
  bars: { label: string; w: number }[];
  progress: number;
}> = ({ x, title, rule, codes, names, bars, progress }) => {
  const color = FUNDS.find((f) => f.code === codes[0])!.color;
  return (
    <div style={{ position: "absolute", inset: 0, opacity: progress, transform: `translateY(${(1 - progress) * 14}px)` }}>
      <div style={{ position: "absolute", left: x, top: 340, width: 400, height: 2, background: color }} />
      <div style={{ position: "absolute", left: x, top: 366, fontFamily: FONT_SANS, fontSize: 40, fontWeight: 500, color: C.ink, whiteSpace: "nowrap" }}>
        {title}
      </div>
      <div style={{ position: "absolute", left: x, top: 424, fontFamily: FONT_SANS, fontSize: 26, color: C.inkSoft, whiteSpace: "nowrap" }}>
        {names.join("　·　")}
      </div>
      <div style={{ position: "absolute", left: x, top: 462, fontFamily: FONT_MONO, fontSize: 22, color: C.inkFaint }}>
        {codes.join("　")}
      </div>
      <div style={{ position: "absolute", left: x, top: 512, fontFamily: FONT_SANS, fontSize: 28, color: color, whiteSpace: "nowrap" }}>
        {rule}
      </div>
      {bars.map((b, i) => {
        const top = 580 + i * 92;
        const w = 360 * b.w;
        return (
          <div key={b.label} style={{ position: "absolute", inset: 0 }}>
            <div style={{ position: "absolute", left: x, top, width: w, height: 52, background: color, opacity: 0.45 + 0.55 * b.w }} />
            <div style={{ position: "absolute", left: x + 16, top: top + 12, fontFamily: FONT_SANS, fontSize: 23, color: C.ink, whiteSpace: "nowrap" }}>
              {b.label}
            </div>
          </div>
        );
      })}
    </div>
  );
};

export const Mechanism: React.FC = () => {
  const { sec } = useLocal(168);
  const head = land(sec, 0, 0.1, 0.5);
  const left = easeSettle((sec - 0.45) / 0.55);
  const right = easeSettle((sec - 1.0) / 0.55);
  const cav = land(sec, 1.7, 0.1, 0.5);

  return (
    <Plate>
      <Kicker style={{ left: 96, top: 156, opacity: head }} size={25} color={C.inkSoft}>
        机制
      </Kicker>
      <div
        style={{
          position: "absolute", left: 96, top: 200, width: 888, fontFamily: FONT_SANS,
          fontSize: 44, fontWeight: 500, color: C.ink, lineHeight: 1.3, opacity: head,
        }}
      >
        {MECHANISM.head}
      </div>

      <RuleColumn
        x={96}
        title={MECHANISM.left.title}
        rule={MECHANISM.left.rule}
        codes={MECHANISM.left.codes}
        names={MECHANISM.left.names}
        bars={MECHANISM.left.bars}
        progress={left}
      />
      <RuleColumn
        x={584}
        title={MECHANISM.right.title}
        rule={MECHANISM.right.rule}
        codes={MECHANISM.right.codes}
        names={MECHANISM.right.names}
        bars={MECHANISM.right.bars}
        progress={right}
      />

      <Rule width={888} color={C.grid} thickness={2} style={{ position: "absolute", left: 96, top: 900 }} />
      <div style={{ position: "absolute", left: 96, top: 926, width: 888, fontFamily: FONT_SANS, fontSize: 28, color: C.inkSoft, lineHeight: 1.5, opacity: cav }}>
        {MECHANISM.caveat}
      </div>

      <div style={{ position: "absolute", left: 96, top: 1120, opacity: cav }}>
        <InvertTag style={{ left: 0, top: 0, padding: "8px 16px 10px", fontSize: 23 }}>
          规则不同 → 成分股不同 → 路径不同
        </InvertTag>
      </div>
      <div style={{ position: "absolute", left: 96, top: 1192, width: 888, fontFamily: FONT_SANS, fontSize: 21, lineHeight: 1.5, color: C.inkFaint, opacity: cav }}>
        沪深300 与中证500 按调整市值加权；中证红利低波动指数按股息率加权；
        中证红利低波动100指数按股息率 / 波动率加权、季度调样
      </div>
    </Plate>
  );
};

// ---------------------------------------------------------------------------
// sc08 最大回撤 —— 零基线横向柱，绝不截断横轴放大差异
// ---------------------------------------------------------------------------
export const Drawdown: React.FC = () => {
  const { sec } = useLocal(156);
  const head = land(sec, 0, 0.1, 0.5);
  const AXIS_LEFT = 96;
  const AXIS_RIGHT = 860;
  // MAX 是横轴的满刻度上界，不是数据上界：只用来给柱端标签留出净空，
  // 四根柱同比缩放，长度比例不受影响。0.46 保证最长的柱子（39.48%）
  // 与其标签一起落在安全区右边界 984 之内。
  const MAX = 0.46;
  const LABEL_W = 200;

  return (
    <Plate>
      <Kicker style={{ left: 96, top: 150, opacity: head }} size={25} color={C.inkSoft}>
        过程 · 一
      </Kicker>
      <div style={{ position: "absolute", left: 96, top: 194, fontFamily: FONT_SANS, fontSize: 48, fontWeight: 500, color: C.ink, whiteSpace: "nowrap", opacity: head }}>
        {DRAWDOWN.head}
      </div>
      <Kicker style={{ left: 96, top: 262, opacity: head }} size={22}>
        {DRAWDOWN.axis_note}
      </Kicker>

      {/* 零基线 */}
      <div style={{ position: "absolute", left: AXIS_LEFT - 2, top: 330, width: 2, height: 790, background: C.ink, opacity: head }} />
      <Kicker style={{ left: AXIS_LEFT - 2, top: 1126, opacity: head }} size={20}>
        0
      </Kicker>

      {DRAWDOWN.rows.map((r, i) => {
        const p = easeOutCubic(clamp01((sec - 0.45 - i * 0.34) / 0.6));
        const top = 372 + i * 190;
        const f = FUNDS.find((x) => x.code === r.code)!;
        const w = ((AXIS_RIGHT - AXIS_LEFT) * r.ratio) / MAX * p;
        return (
          <div key={r.code} style={{ position: "absolute", inset: 0 }}>
            <div style={{ position: "absolute", left: AXIS_LEFT + 14, top: top - 2, width: 14, height: 14, background: f.color }} />
            <div style={{ position: "absolute", left: AXIS_LEFT + 40, top: top - 12, fontFamily: FONT_SANS, fontSize: 32, color: C.ink, whiteSpace: "nowrap" }}>
              {r.name}
              <span style={{ fontFamily: FONT_MONO, fontSize: 21, color: C.inkFaint, marginLeft: 12 }}>{r.code}</span>
            </div>
            <div style={{ position: "absolute", left: AXIS_LEFT, top: top + 44, width: w, height: 58, background: f.color }} />
            {/* 数值一律锚在柱端外侧、左对齐。
                曾经的写法是「柱子够长就把数字放进柱内、右对齐、近白色」，
                但 textAlign:right 配合固定 width 会把文字推到 left + width，
                也就是柱端之外 168px —— 落在浅色底板上，近白字几乎看不见。
                现在不分支：标签永远在柱外，颜色统一用墨色，
                免得最浅的身份色（中证500 #C4791F 对底板只有 3.1:1）成为新的可读性短板。 */}
            <div
              style={{
                position: "absolute",
                left: AXIS_LEFT + w + 16,
                top: top + 52,
                width: LABEL_W,
                textAlign: "left",
                fontFamily: FONT_MONO,
                fontSize: 40,
                fontWeight: 500,
                color: C.ink,
                opacity: 0.4 + 0.6 * p,
                whiteSpace: "nowrap",
              }}
            >
              −{r.drawdown}
            </div>
            <div style={{ position: "absolute", left: AXIS_LEFT, top: top + 118, fontFamily: FONT_SANS, fontSize: 22, color: C.inkFaint, whiteSpace: "nowrap", opacity: p }}>
              {r.span_range}　·　跨 {r.span_days} 天
            </div>
          </div>
        );
      })}
    </Plate>
  );
};

// ---------------------------------------------------------------------------
// sc09 最长一段没回到前高 —— 时间条（与上一场图形不同，回答的是"等了多久"）
// ---------------------------------------------------------------------------
const STRIP_LEFT = 150;
const STRIP_RIGHT = 984;

export const Underwater: React.FC = () => {
  const { sec } = useLocal(114);
  const head = land(sec, 0, 0.1, 0.5);
  const hero = land(sec, 2.0, 0.1, 0.5);

  const t0 = new Date(`${DATES[0]}T00:00:00Z`).getTime();
  const t1 = new Date(`${DATES[DATES.length - 1]}T00:00:00Z`).getTime();
  const xOf = (d: string) =>
    STRIP_LEFT + ((STRIP_RIGHT - STRIP_LEFT) * (new Date(`${d}T00:00:00Z`).getTime() - t0)) / (t1 - t0);

  const maxDays = Math.max(...UNDERWATER.rows.map((r) => r.days));

  return (
    <Plate>
      <Kicker style={{ left: 96, top: 150, opacity: head }} size={25} color={C.inkSoft}>
        过程 · 二
      </Kicker>
      <div style={{ position: "absolute", left: 96, top: 194, fontFamily: FONT_SANS, fontSize: 48, fontWeight: 500, color: C.ink, whiteSpace: "nowrap", opacity: head }}>
        {UNDERWATER.head}
      </div>

      {UNDERWATER.rows.map((r, i) => {
        const p = easeOutCubic(clamp01((sec - 0.5 - i * 0.3) / 0.7));
        const top = 330 + i * 196;
        const f = FUNDS.find((x) => x.code === r.code)!;
        const xa = xOf(r.range[0]);
        const xb = xOf(r.range[1]);
        const w = (xb - xa) * p;
        return (
          <div key={r.code} style={{ position: "absolute", inset: 0, opacity: clamp01(p * 1.6) }}>
            <div style={{ position: "absolute", left: 96, top: top - 4, width: 14, height: 14, background: f.color }} />
            <div style={{ position: "absolute", left: 122, top: top - 14, fontFamily: FONT_SANS, fontSize: 32, color: C.ink, whiteSpace: "nowrap" }}>
              {r.name}
            </div>
            <div
              style={{
                position: "absolute", left: STRIP_LEFT, top: top + 26, width: STRIP_RIGHT - STRIP_LEFT,
                height: 34, background: C.gridSoft,
              }}
            />
            <div style={{ position: "absolute", left: xa, top: top + 26, width: w, height: 34, background: f.color, opacity: 0.85 }} />
            {r.still_open ? (
              <div style={{ position: "absolute", left: Math.min(xb + 8, STRIP_RIGHT - 4), top: top + 26, width: 6, height: 34, background: C.invert }} />
            ) : null}
            <div style={{ position: "absolute", left: STRIP_LEFT, top: top + 68, fontFamily: FONT_SANS, fontSize: 21, color: C.inkFaint, whiteSpace: "nowrap", opacity: p }}>
              {r.range[0]} → {r.range[1]}
              {r.still_open ? "（到区间终点仍未回去）" : ""}
            </div>
            <div
              style={{
                position: "absolute", left: STRIP_RIGHT - 210, top: top - 10, width: 210, textAlign: "right",
                fontFamily: FONT_MONO, fontSize: 40, fontWeight: 500, color: f.color,
              }}
            >
              {r.days}
              <span style={{ fontFamily: FONT_SANS, fontSize: 22, color: C.inkSoft, marginLeft: 8 }}>个交易日</span>
            </div>
          </div>
        );
      })}

      <div style={{ position: "absolute", left: 96, top: 1180, opacity: hero }}>
        <InvertTag style={{ left: 0, top: 0, padding: "10px 18px 12px", fontSize: 30 }}>
          {UNDERWATER.hero}
        </InvertTag>
      </div>
      <div
        style={{
          position: "absolute", left: 96, top: 1272, width: 888, fontFamily: FONT_SANS,
          fontSize: 21, lineHeight: 1.5, color: C.inkFaint, opacity: hero,
        }}
      >
        时间条覆盖 {UNDERWATER.range_note}　·　深色区段 = 当日账户资产低于此前历史最高值
      </div>
    </Plate>
  );
};
