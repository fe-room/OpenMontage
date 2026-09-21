import React from "react";
import { AbsoluteFill } from "remotion";
import { C, FONT_MONO, FONT_SANS, clamp01, easeOutCubic } from "./theme";
import { Kicker, Num, useLocal } from "./Foundation";
import {
  DATES,
  FUNDS,
  INDEX_MAX,
  INITIAL_ASSET,
  PLOT,
  PLOT_HELPER_X,
  PLOT_HELPER_Y,
  RACE,
  SERIES,
  YEAR_TICKS,
} from "./timeline";

// ---------------------------------------------------------------------------
// 折线路径：模块级一次性生成，确定性、不随帧重算。
// 步长 2 在 670px 宽的绘图区里约 0.9px/点，肉眼无损。
// ---------------------------------------------------------------------------
const PATH_STEP = 2;
const PATHS: Record<string, string> = (() => {
  const out: Record<string, string> = {};
  for (const f of FUNDS) {
    const vals = SERIES[f.code];
    const pts: string[] = [];
    for (let i = 0; i < vals.length; i += PATH_STEP) {
      pts.push(`${PLOT_HELPER_X(i).toFixed(1)},${PLOT_HELPER_Y(vals[i]).toFixed(1)}`);
    }
    const last = vals.length - 1;
    pts.push(`${PLOT_HELPER_X(last).toFixed(1)},${PLOT_HELPER_Y(vals[last]).toFixed(1)}`);
    out[f.code] = pts.join(" ");
  }
  return out;
})();

const at = (date: string) => DATES.indexOf(date);
const val = (code: string, date: string) => SERIES[code][at(date)];
const yuan = (n: number) => Math.round(n).toLocaleString("en-US");

// 局部秒 = 绝对秒 − 场景起点
const RS = RACE.startSec - RACE.sceneStartSec;
const RE = RACE.endSec - RACE.sceneStartSec;

const fade = (sec: number, from: number, until: number) => {
  const inn = clamp01((sec - from) / 0.35);
  const out = clamp01((until - sec) / 0.35);
  return Math.min(inn, out);
};

// 竖向防重叠：按当前值排序后强制最小间距，再整体收进绘图区
function decollide(ys: number[], gap: number, min: number, max: number): number[] {
  const out = ys.slice();
  for (let i = 1; i < out.length; i += 1) {
    if (out[i] - out[i - 1] < gap) out[i] = out[i - 1] + gap;
  }
  const overflow = out[out.length - 1] - max;
  if (overflow > 0) for (let i = 0; i < out.length; i += 1) out[i] -= overflow;
  if (out[0] < min) {
    const shift = min - out[0];
    for (let i = 0; i < out.length; i += 1) out[i] += shift;
  }
  return out;
}

// ---------------------------------------------------------------------------
// 注解表：分组方式是设计决定（线性时间下 2023 收官与 2024-02 极值只相隔
// 0.87 秒，无法各自独占一个底部窗口，故 2023 的数字并入极值面板作为对照）。
// 每个数值都从 SERIES / METRICS 现算，不手打。
// ---------------------------------------------------------------------------
type InlineAnn = {
  id: string;
  from: number;
  until: number;
  slot: 0 | 1;
  index: number;
  color: string;
  head: string;
  value: string;
};

type BottomAnn =
  | { id: string; kind: "rank"; from: number; until: number; kicker: string; date: string }
  | { id: string; kind: "climax"; from: number; until: number }
  | { id: string; kind: "peakpair"; from: number; until: number };

const INLINE: InlineAnn[] = [
  {
    id: "peak2021",
    from: 6.0, until: 23.0, slot: 0,
    index: at("2021-02-10"), color: "#31527E",
    head: "沪深300 见顶", value: yuan(val("510300", "2021-02-10")),
  },
  {
    id: "underwater2022",
    from: 15.7, until: 31.0, slot: 1,
    index: at("2022-03-08"), color: "#5A544A",
    head: "首次收于起点以下", value: yuan(val("510300", "2022-03-08")),
  },
  {
    id: "peak2026",
    from: 54.6, until: 56.9, slot: 0,
    index: at("2026-06-30"), color: "#C4791F",
    head: "中证500 见顶", value: yuan(val("510500", "2026-06-30")),
  },
];

const BOTTOM: BottomAnn[] = [
  { id: "close2021", kind: "rank", from: 14.1, until: 23.0, kicker: "2021 收官 · 排名发生变化", date: "2021-12-31" },
  { id: "close2022", kind: "rank", from: 23.15, until: 30.9, kicker: "2022 收官 · 两只宽基已在水下", date: "2022-12-30" },
  { id: "climax2024", kind: "climax", from: 31.6, until: 37.9 },
  { id: "close2024", kind: "rank", from: 41.2, until: 47.6, kicker: "2024 收官", date: "2024-12-31" },
  { id: "peakpair2025", kind: "peakpair", from: 49.0, until: 55.2 },
];

// ---------------------------------------------------------------------------
const Chip: React.FC<{ x: number; y: number; color: string; name: string; value: number }> = ({
  x, y, color, name, value,
}) => (
  <g>
    <rect x={x} y={y - 34} width={148} height={66} fill="rgba(246,247,244,0.94)" stroke={`${color}66`} strokeWidth={1} />
    <rect x={x} y={y - 34} width={4} height={66} fill={color} />
    <text x={x + 14} y={y - 8} fontFamily={FONT_SANS} fontSize={21} fill={C.inkSoft}>
      {name}
    </text>
    <text x={x + 14} y={y + 24} fontFamily={FONT_MONO} fontSize={28} fontWeight={500} fill={color}>
      {yuan(value)}
    </text>
  </g>
);

const RankPanel: React.FC<{ kicker: string; date: string; opacity: number }> = ({
  kicker, date, opacity,
}) => {
  const rows = [...FUNDS]
    .map((f) => ({ f, v: val(f.code, date) }))
    .sort((a, b) => b.v - a.v);
  return (
    <div style={{ position: "absolute", inset: 0, opacity }}>
      <Kicker style={{ left: 96, top: 1104 }} size={25} color={C.ink}>
        {kicker}
      </Kicker>
      {rows.map((r, i) => {
        const y = 1156 + i * 46;
        const under = r.v < INITIAL_ASSET;
        return (
          <div key={r.f.code}>
            <div
              style={{
                position: "absolute", left: 112, top: y + 4,
                fontFamily: FONT_MONO, fontSize: 20, color: C.inkFaint,
              }}
            >
              {i + 1}
            </div>
            <div style={{ position: "absolute", left: 142, top: y + 6, width: 14, height: 14, background: r.f.color }} />
            <div
              style={{
                position: "absolute", left: 168, top: y,
                fontFamily: FONT_SANS, fontSize: 26, color: C.ink,
              }}
            >
              {r.f.name}
              <span style={{ fontFamily: FONT_MONO, fontSize: 19, color: C.inkFaint, marginLeft: 10 }}>
                {r.f.code}
              </span>
            </div>
            <div
              style={{
                position: "absolute", left: 620, top: y - 3, width: 200,
                textAlign: "right", fontFamily: FONT_MONO, fontSize: 30, fontWeight: 500, color: r.f.color,
              }}
            >
              {yuan(r.v)}
            </div>
            {under ? (
              <div
                style={{
                  position: "absolute", left: 838, top: y + 1, padding: "3px 10px",
                  background: C.invert, color: C.invertText, fontFamily: FONT_SANS, fontSize: 20,
                }}
              >
                水下
              </div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
};

const ClimaxPanel: React.FC<{ opacity: number }> = ({ opacity }) => {
  const v300 = val("510300", "2024-02-02");
  const v100 = val("515100", "2024-02-02");
  const v500 = val("510500", "2024-02-05");
  const v50 = val("512890", "2024-02-05");
  const gap = v100 - v300;
  return (
    <div style={{ position: "absolute", inset: 0, opacity }}>
      <Kicker style={{ left: 96, top: 1088 }} size={24} color={C.ink}>
        2024 年 2 月 · 区间最低点
      </Kicker>
      {[
        { name: "沪深300", code: "510300", v: v300, tag: "区间最低", date: "2024-02-02" },
        { name: "中证500", code: "510500", v: v500, tag: "下一个交易日", date: "2024-02-05" },
      ].map((r, i) => {
        const y = 1130 + i * 52;
        const f = FUNDS.find((x) => x.code === r.code)!;
        return (
          <div key={r.code} style={{ position: "absolute", inset: 0 }}>
            <div style={{ position: "absolute", left: 96, top: y + 12, width: 14, height: 14, background: f.color }} />
            <div style={{ position: "absolute", left: 122, top: y + 4, fontFamily: FONT_SANS, fontSize: 28, color: C.ink }}>
              {r.name}
            </div>
            <div
              style={{
                position: "absolute", left: 300, top: y, fontFamily: FONT_MONO,
                fontSize: 38, fontWeight: 500, color: f.color,
              }}
            >
              {yuan(r.v)}
            </div>
            <div style={{ position: "absolute", left: 556, top: y + 10, fontFamily: FONT_SANS, fontSize: 21, color: C.inkFaint, whiteSpace: "nowrap" }}>
              {r.tag}　{r.date}
            </div>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 96, top: 1240, fontFamily: FONT_SANS, fontSize: 23, color: C.inkSoft }}>
        2023 收官：沪深300 {yuan(val("510300", "2023-12-29"))}　红利低波100 {yuan(val("515100", "2023-12-29"))}
      </div>
      <div style={{ position: "absolute", left: 96, top: 1278, fontFamily: FONT_SANS, fontSize: 23, color: C.inkSoft, whiteSpace: "nowrap" }}>
        同一天的另一边：沪深300 {yuan(v300)}　／　红利低波100 {yuan(v100)}
      </div>
      <div style={{ position: "absolute", left: 96, top: 1306, background: C.invert, color: C.invertText, padding: "8px 18px 10px" }}>
        <span style={{ fontFamily: FONT_SANS, fontSize: 26 }}>同一天相差　</span>
        <span style={{ fontFamily: FONT_MONO, fontSize: 42, fontWeight: 500 }}>{yuan(gap)}</span>
      </div>
    </div>
  );
};

const PeakPairPanel: React.FC<{ opacity: number }> = ({ opacity }) => {
  const d = "2025-11-12";
  return (
    <div style={{ position: "absolute", inset: 0, opacity }}>
      <Kicker style={{ left: 96, top: 1104 }} size={25} color={C.ink}>
        2025-11-12 · 两只红利低波在同一天见顶
      </Kicker>
      {[
        { code: "512890", name: "红利低波50" },
        { code: "515100", name: "红利低波100" },
      ].map((r, i) => {
        const f = FUNDS.find((x) => x.code === r.code)!;
        const y = 1160 + i * 56;
        return (
          <div key={r.code} style={{ position: "absolute", inset: 0 }}>
            <div style={{ position: "absolute", left: 96, top: y + 12, width: 14, height: 14, background: f.color }} />
            <div style={{ position: "absolute", left: 122, top: y + 4, fontFamily: FONT_SANS, fontSize: 28, color: C.ink }}>
              {r.name}
            </div>
            <div
              style={{
                position: "absolute", left: 340, top: y, fontFamily: FONT_MONO,
                fontSize: 38, fontWeight: 500, color: f.color,
              }}
            >
              {yuan(val(r.code, d))}
            </div>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 96, top: 1284, fontFamily: FONT_SANS, fontSize: 23, color: C.inkSoft }}>
        同一天沪深300 是 {yuan(val("510300", d))}　·　中证500 是 {yuan(val("510500", d))}
      </div>
      <div style={{ position: "absolute", left: 96, top: 1324, fontFamily: FONT_SANS, fontSize: 21, color: C.inkFaint }}>
        两只都在同一天创下各自的区间最高账户资产（账户资产口径）
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
export const RaceStage: React.FC<{ durationInFrames: number }> = ({ durationInFrames }) => {
  const { sec } = useLocal(durationInFrames);

  const reveal = clamp01((sec - RS) / (RE - RS));
  const idx = Math.round(reveal * INDEX_MAX);
  const boundary = PLOT_HELPER_X(idx);
  const drawn = easeOutCubic(clamp01((sec - RS) / 0.6));

  // 四条跟随数值签：按当前值排序后竖向防重叠
  const chips = [...FUNDS]
    .map((f) => ({ f, v: SERIES[f.code][idx], y: PLOT_HELPER_Y(SERIES[f.code][idx]) }))
    .sort((a, b) => a.y - b.y);
  const ys = decollide(chips.map((c) => c.y), 76, PLOT.y0 + 36, PLOT.y1 - 20);

  const bottom = BOTTOM.find((b) => sec >= b.from && sec <= b.until);
  const bottomOpacity = bottom ? fade(sec, bottom.from, bottom.until) : 0;

  return (
    <AbsoluteFill style={{ backgroundColor: C.base }}>
      <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{ position: "absolute", inset: 0 }}>
        <defs>
          <clipPath id="race-reveal" clipPathUnits="userSpaceOnUse">
            <rect x={PLOT.x0} y={PLOT.y0} width={Math.max(0, boundary - PLOT.x0)} height={PLOT.y1 - PLOT.y0} />
          </clipPath>
        </defs>

        {/* 绘图区 */}
        <rect x={PLOT.x0} y={PLOT.y0} width={PLOT.x1 - PLOT.x0} height={PLOT.y1 - PLOT.y0} fill="#FFFFFF" />
        {/* 水下带：¥100,000 以下 */}
        <rect
          x={PLOT.x0}
          y={PLOT_HELPER_Y(PLOT.baseline)}
          width={PLOT.x1 - PLOT.x0}
          height={PLOT.y1 - PLOT_HELPER_Y(PLOT.baseline)}
          fill={C.under}
          opacity={drawn}
        />
        {/* 横向刻度 */}
        {[80000, 100000, 120000, 140000, 160000, 180000, 200000].map((gv) => (
          <g key={gv} opacity={drawn}>
            <line x1={PLOT.x0} y1={PLOT_HELPER_Y(gv)} x2={PLOT.x1} y2={PLOT_HELPER_Y(gv)} stroke={C.grid} strokeWidth={1} />
            {gv % 40000 === 0 ? (
              <text
                x={PLOT.x0 - 10}
                y={PLOT_HELPER_Y(gv) + 7}
                textAnchor="end"
                fontFamily={FONT_MONO}
                fontSize={20}
                fill={C.inkFaint}
              >
                {gv / 1000}k
              </text>
            ) : null}
          </g>
        ))}
        {/* 年份刻度：随揭示进度点亮 */}
        {YEAR_TICKS.map((t) => {
          const lit = clamp01((sec - (t.tSec - RACE.sceneStartSec)) / 0.35);
          return (
            <g key={t.label} opacity={drawn}>
              <line x1={t.x} y1={PLOT.y0} x2={t.x} y2={PLOT.y1} stroke={lit > 0.5 ? C.grid : C.gridSoft} strokeWidth={1} />
              <text
                x={t.x}
                y={PLOT.y1 + 30}
                textAnchor="middle"
                fontFamily={FONT_MONO}
                fontSize={22}
                fill={lit > 0.5 ? C.ink : C.grid}
              >
                {t.label}
              </text>
            </g>
          );
        })}
        {/* 起跑线 */}
        <line
          x1={PLOT.x0}
          y1={PLOT_HELPER_Y(PLOT.baseline)}
          x2={PLOT.x0 + (PLOT.x1 - PLOT.x0) * drawn}
          y2={PLOT_HELPER_Y(PLOT.baseline)}
          stroke={C.rule}
          strokeWidth={2}
          strokeDasharray="7 5"
        />
        <text
          x={PLOT.x1}
          y={PLOT_HELPER_Y(PLOT.baseline) - 10}
          textAnchor="end"
          fontFamily={FONT_SANS}
          fontSize={21}
          fill={C.rule}
          opacity={drawn}
        >
          起点 ¥100,000
        </text>
        <text
          x={PLOT.x1 - 10}
          y={PLOT_HELPER_Y(PLOT.baseline) + 28}
          textAnchor="end"
          fontFamily={FONT_SANS}
          fontSize={20}
          fill={C.rule}
          opacity={drawn * 0.9}
        >
          水下
        </text>

        {/* 四条曲线 */}
        <g clipPath="url(#race-reveal)">
          {FUNDS.map((f) => (
            <polyline key={f.code} points={PATHS[f.code]} fill="none" stroke={f.color} strokeWidth={4} strokeLinejoin="round" strokeLinecap="round" />
          ))}
        </g>

        {/* 仍在绘图区内的内联注解：竖虚线 + 锚点 */}
        {INLINE.filter((a) => sec >= a.from && sec <= a.until).map((a) => (
          <g key={a.id} opacity={fade(sec, a.from, a.until)}>
            <line
              x1={PLOT_HELPER_X(a.index)}
              y1={PLOT.y0}
              x2={PLOT_HELPER_X(a.index)}
              y2={PLOT.y1}
              stroke={a.color}
              strokeWidth={1.4}
              strokeDasharray="3 4"
              opacity={0.5}
            />
            <circle
              cx={PLOT_HELPER_X(a.index)}
              cy={PLOT_HELPER_Y(
                a.id === "peak2021"
                  ? val("510300", "2021-02-10")
                  : a.id === "underwater2022"
                    ? val("510300", "2022-03-08")
                    : val("510500", "2026-06-30"),
              )}
              r={5}
              fill={a.color}
            />
          </g>
        ))}

        {/* 跟随数值签 */}
        <g>
          {chips.map((c, i) => (
            <Chip key={c.f.code} x={boundary + 10} y={ys[i]} color={c.f.color} name={c.f.name} value={c.v} />
          ))}
        </g>
      </svg>

      {/* 顶部读数 */}
      <Kicker style={{ left: 96, top: 94 }} size={21}>
        {`${DATES[0].replace(/-/g, ".")} → ${DATES[DATES.length - 1].replace(/-/g, ".")}`}
      </Kicker>
      <Num style={{ left: 96, top: 128, opacity: bottom ? 0.42 : 1 }} size={46} color={C.ink}>
        {DATES[idx]}
      </Num>
      <Kicker style={{ right: 96, top: 142 }} size={22} color={C.inkSoft}>
        账户资产（元）
      </Kicker>

      {/* 内联注解文字（两个插槽，避免互相压字） */}
      {INLINE.filter((a) => sec >= a.from && sec <= a.until).map((a) => {
        const x = PLOT_HELPER_X(a.index);
        const label = `${a.head}　${a.value}`;
        const w = a.head.length * 26 + 14 + a.value.length * 15.6;
        const flip = x + 20 + w > 984;
        const tx = flip ? x - 16 : x + 16;
        const ty = a.slot === 0 ? 204 : 246;
        return (
          <div key={`lab-${a.id}`} style={{ position: "absolute", inset: 0, opacity: fade(sec, a.from, a.until) }}>
            <div style={{ position: "absolute", left: x, top: ty - 2, width: 3, height: 30, background: a.color }} />
            <div
              style={{
                position: "absolute", left: flip ? undefined : tx, right: flip ? 1080 - tx : undefined, top: ty,
                fontFamily: FONT_SANS, fontSize: 26, color: a.color, whiteSpace: "nowrap",
              }}
            >
              {a.head}
              <span style={{ fontFamily: FONT_MONO, fontSize: 26, marginLeft: 12 }}>{a.value}</span>
            </div>
          </div>
        );
      })}

      {/* 底部注解：任一时点只显示一个 */}
      {bottom?.kind === "rank" ? (
        <RankPanel kicker={bottom.kicker} date={bottom.date} opacity={bottomOpacity} />
      ) : null}
      {bottom?.kind === "climax" ? <ClimaxPanel opacity={bottomOpacity} /> : null}
      {bottom?.kind === "peakpair" ? <PeakPairPanel opacity={bottomOpacity} /> : null}
    </AbsoluteFill>
  );
};
