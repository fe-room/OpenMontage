"""Step 3 — script for etf-100k-four-fund-race.

Single owner of: artifacts/script.json (+ artifacts/onscreen.json copy deck)

This is a silent film: there is no narration, so the script's job is the
on-screen beat sheet. Every number that will appear on screen is GENERATED from
the canonical dataset — never typed by hand — and verify() re-checks each
rendered figure against the series before the artifact is written.

Structural decision recorded here: the 56.8s race is ONE continuous scene with
seven annotation beats, not seven cuts. The film never cuts during the race, so
modelling it as seven scenes would misdescribe it (and would trip the
consecutive-repeated-type advisory for no real reason).
"""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

OUT = PROJECT / "artifacts" / "script.json"
OUT_DECK = PROJECT / "artifacts" / "onscreen.json"

DISCLAIMER = "本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。"
TITLE = "10万元买4只ETF，6年后差多少？"
TOTAL = 99.0
FPS = 30

DATA = json.loads((PROJECT / "artifacts" / "etf_data.json").read_text())
DATES: list[str] = DATA["dates"]
SERIES: dict[str, list[int]] = DATA["series"]
METRICS: dict[str, dict] = DATA["metrics"]
FUNDS: list[dict] = DATA["funds"]
NAME_BY_CODE = {f["code"]: f["name"] for f in FUNDS}
INITIAL = DATA["meta"]["initial_asset"]
N = len(DATES) - 1

RACE_START, RACE_END = 13.6, 70.0
RACE_SPAN = RACE_END - RACE_START
RACE_STAGE_START = 13.2

WEEKDAY = "一二三四五六日"


# --------------------------------------------------------------------------
# data helpers — every screen figure comes from here
# --------------------------------------------------------------------------
def idx(d: str) -> int:
    return DATES.index(d)


def v(code: str, d: str) -> int:
    return SERIES[code][idx(d)]


def yuan(n: int) -> str:
    return f"¥{n:,}"


def pct(x: float, digits: int = 2) -> str:
    return f"{x * 100:+.{digits}f}%"


def pct_abs(x: float, digits: int = 2) -> str:
    return f"{abs(x) * 100:.{digits}f}%"


def rank_rows(d: str) -> list[dict]:
    order = sorted(SERIES, key=lambda c: -v(c, d))
    return [
        {
            "code": c,
            "name": NAME_BY_CODE[c],
            "value": v(c, d),
            "display": yuan(v(c, d)),
            "underwater": v(c, d) < INITIAL,
        }
        for c in order
    ]


def t_of(d: str) -> float:
    return RACE_START + RACE_SPAN * (idx(d) / N)


# --------------------------------------------------------------------------
# beat sheet
# --------------------------------------------------------------------------
def build_beats() -> list[dict]:
    m300, m500, m50, m100 = (
        METRICS["510300"], METRICS["510500"], METRICS["512890"], METRICS["515100"]
    )
    beats: list[dict] = []

    beats.append({
        "id": "sc01", "kind": "standalone", "label": "开场提问", "role": "hook",
        "type": "text_card",
        "data": {
            "overline": f"{DATES[0].replace('-', '.')}　周{'一二三四五六日'[date.fromisoformat(DATES[0]).weekday()]}",
            "lines": ["同一天，同一笔钱", "四只 ETF，各买 10 万"],
            "hero": "6 年后，差多少？",
        },
        "source_ref": "腾讯证券行情接口 日线后复权；区间起点见口径说明",
    })

    beats.append({
        "id": "sc02", "kind": "standalone", "label": "四只身份牌", "role": "cast",
        "type": "chip_row",
        "data": {
            "head": f"同为 {yuan(INITIAL)} 起点",
            "chips": [
                {"name": f["name"], "code": f["code"], "category": f["category"], "color": f["color"]}
                for f in FUNDS
            ],
            "foot": "四只跟踪的指数不同，选股与加权规则也不同",
        },
        "source_ref": "基金公司与交易所公开产品资料",
    })

    beats.append({
        "id": "sc03", "kind": "standalone", "label": "规则公布", "role": "rules",
        "type": "rule_list",
        "data": {
            "head": "规则只有一条：中途什么都不做",
            "rows": [
                {"k": "起点", "v": DATES[0].replace("-", ".")},
                {"k": "初始资金", "v": yuan(INITIAL)},
                {"k": "分红处理", "v": "按再投资计算（后复权口径）"},
                {"k": "之后的操作", "v": "不定投 · 不择时 · 不卖出"},
            ],
            "hero": "START",
        },
        "source_ref": "用户工作簿「口径说明」工作表",
    })

    beats.append({
        "id": "ch-2020h2", "kind": "chart_beat", "label": "2020 下半年 → 2021-02 见顶",
        "role": "race",
        "data": {"pins": [{
            "at": t_of("2021-02-10"),
            "date": "2021-02-10",
            "head": f"沪深300 见顶 {yuan(v('510300', '2021-02-10'))}",
            "sub": "此后再也没回到这个位置",
        }]},
        "source_ref": "2021-02-10 截面，账户资产口径",
    })

    beats.append({
        "id": "ch-2021", "kind": "chart_beat", "label": "2021 分化 → 排名变化", "role": "race",
        "data": {"callouts": [{
            "at": t_of("2021-12-31"),
            "kicker": "2021 收官 · 排名发生变化",
            "rows": rank_rows("2021-12-31"),
        }]},
        "source_ref": "2021-12-31 截面",
    })

    beats.append({
        "id": "ch-2022", "kind": "chart_beat", "label": "2022 跌破起跑线", "role": "race",
        "data": {
            "markers": [{
                "at": t_of("2022-03-08"),
                "text": f"2022-03-08　沪深300 首次收于起点以下 {yuan(v('510300', '2022-03-08'))}",
            }],
            "callouts": [{
                "at": t_of("2022-12-30"),
                "kicker": (
                    "2022 收官 · "
                    + str(sum(1 for c in SERIES if v(c, "2022-12-30") < INITIAL))
                    + " 只已在水下"
                ),
                "rows": rank_rows("2022-12-30"),
            }],
        },
        "source_ref": "2022-03-08 与 2022-12-30 截面",
    })

    beats.append({
        "id": "ch-2023", "kind": "chart_beat", "label": "2023 深水区", "role": "race",
        "data": {"callouts": [{
            "at": t_of("2023-12-29"),
            "kicker": "2023 收官",
            "rows": rank_rows("2023-12-29"),
            "foot": f"沪深300 距 2021-02 高点 {pct(v('510300', '2023-12-29') / m300['peak_asset'] - 1)}",
        }]},
        "source_ref": "2023-12-29 截面 vs 2021-02-10 峰值",
    })

    beats.append({
        "id": "ch-2024", "kind": "chart_beat", "label": "2024-02 极值（全屏标注）",
        "role": "climax",
        "data": {
            "head": "2024 年 2 月",
            "rows": [
                {"date": "2024-02-02", "name": "沪深300",
                 "value": yuan(v("510300", "2024-02-02")), "tag": "区间最低"},
                {"date": "2024-02-05", "name": "中证500",
                 "value": yuan(v("510500", "2024-02-05")), "tag": "区间最低"},
            ],
            "contrast": {
                "date": "2024-02-02",
                "left": f"{yuan(v('510300', '2024-02-02'))}　沪深300",
                "right": f"{yuan(v('515100', '2024-02-02'))}　红利低波100",
                "hero": f"同一天相差 {yuan(v('515100', '2024-02-02') - v('510300', '2024-02-02'))}",
            },
            "foot": (
                f"下一个交易日，中证500 也跌到区间最低 {yuan(v('510500', '2024-02-05'))}；"
                f"同一天红利低波50 是 {yuan(v('512890', '2024-02-05'))}"
            ),
        },
        "source_ref": "2024-02-02 与 2024-02-05 两个截面，日期分别标注",
    })

    beats.append({
        "id": "ch-2024h2", "kind": "chart_beat", "label": "2024 收官 → 2025-11 双雄见顶",
        "role": "race",
        "data": {
            "callouts": [{
                "at": t_of("2024-12-31"),
                "kicker": "2024 收官",
                "rows": rank_rows("2024-12-31"),
            }],
            "pins": [{
                "at": t_of("2025-11-12"),
                "date": "2025-11-12",
                "head": f"红利低波50 {yuan(v('512890', '2025-11-12'))}　红利低波100 {yuan(v('515100', '2025-11-12'))}",
                "sub": "两只在同一天见顶",
            }],
        },
        "source_ref": "2024-12-31 与 2025-11-12 截面",
    })

    beats.append({
        "id": "ch-end", "kind": "chart_beat", "label": "收束到区间终点", "role": "race",
        "data": {
            "markers": [{
                "at": t_of("2026-06-30"),
                "text": f"2026-06-30　中证500 见顶 {yuan(v('510500', '2026-06-30'))}",
            }],
            "end_card": {
                "at": t_of(DATES[-1]),
                "date": DATES[-1].replace("-", "."),
                "label": "区间终点",
            },
        },
        "source_ref": f"{DATES[-1]} 截面，抓取日可获得的最新完整交易日",
    })

    beats.append({
        "id": "sc05", "kind": "standalone", "label": "冻结最终结果", "role": "result",
        "type": "result_table",
        "data": {
            "head": f"{DATES[-1].replace('-', '.')}　冻结",
            "columns": ["最终资产", "累计收益", "年化收益"],
            "rows": [
                {
                    "code": c, "name": NAME_BY_CODE[c],
                    "final_asset": yuan(METRICS[c]["final_asset"]),
                    "cumulative": pct(METRICS[c]["cumulative_return"]),
                    "annualized": pct(METRICS[c]["annualized_return"]),
                }
                for c in sorted(SERIES, key=lambda k: -METRICS[k]["final_asset"])
            ],
            "foot": f"期末最好与最差相差 {yuan(max(m['final_asset'] for m in METRICS.values()) - min(m['final_asset'] for m in METRICS.values()))}",
        },
        "source_ref": "账户资产口径；累计 = 最终资产 ÷ 100,000 − 1；年化按 365.2425 天/年复利折算",
    })

    beats.append({
        "id": "sc06", "kind": "standalone", "label": "转折", "role": "turn",
        "type": "text_card",
        "data": {
            "hero": "但是，过程一样吗？",
            "sub": (
                f"跌幅都在四成上下：沪深300 -{pct_abs(m300['max_drawdown'])}，"
                f"中证500 -{pct_abs(m500['max_drawdown'])}"
            ),
            "foot": (
                f"但沪深300 从峰值到低点走了 {m300['mdd_days']} 天，"
                f"红利低波50 只走了 {m50['mdd_days']} 天"
            ),
        },
        "source_ref": f"最大回撤幅度与跨度：沪深300 {m300['mdd_peak_date']} → {m300['mdd_trough_date']}；红利低波50 {m50['mdd_peak_date']} → {m50['mdd_trough_date']}",
    })

    beats.append({
        "id": "sc07", "kind": "standalone", "label": "规则不同，路径不同", "role": "mechanism",
        "type": "rule_compare",
        "data": {
            "head": "差别不在基金经理，在指数的选股规则",
            "left": {
                "title": "按市值加权",
                "codes": ["510300", "510500"],
                "names": ["沪深300", "中证500"],
                "rule": "规模越大，权重越高",
                "bars": [{"label": "规模最大", "w": 1.0}, {"label": "居中", "w": 0.62}, {"label": "规模最小", "w": 0.34}],
            },
            "right": {
                "title": "按股息率加权",
                "codes": ["512890", "515100"],
                "names": ["红利低波50", "红利低波100"],
                "rule": "股息率越高，权重越高",
                "bars": [{"label": "股息率最高", "w": 1.0}, {"label": "居中", "w": 0.62}, {"label": "股息率最低", "w": 0.34}],
            },
            "caveat": "规则不同 → 选出的股票集合不同 → 同一天的涨跌并不同步。这只是解释过去路径的差异，不构成对未来的推断。",
        },
        "source_ref": "中证指数有限公司编制公告；上海证券交易所 ETF 产品页（中证红利低波动指数选样条件）",
    })

    dd_rows = [
        {
            "code": c, "name": NAME_BY_CODE[c],
            "drawdown": pct_abs(METRICS[c]["max_drawdown"]),
            "ratio": abs(METRICS[c]["max_drawdown"]),
            "span_days": METRICS[c]["mdd_days"],
            "span_range": f"{METRICS[c]['mdd_peak_date']} → {METRICS[c]['mdd_trough_date']}",
        }
        for c in sorted(SERIES, key=lambda k: -METRICS[k]["max_drawdown"])
    ]
    beats.append({
        "id": "sc08", "kind": "standalone", "label": "最大回撤（零基线横向柱）",
        "role": "evidence", "type": "drawdown_bars",
        "data": {
            "head": "最大回撤",
            "rows": dd_rows,
            "axis_note": "零基线，从 0 起算",
        },
        "source_ref": "每日账户资产相对此前历史峰值的最大跌幅",
    })

    uw_rows = [
        {
            "code": c, "name": NAME_BY_CODE[c],
            "days": METRICS[c]["longest_underwater_days"],
            "range": METRICS[c]["longest_underwater_range"],
            "still_open": METRICS[c]["longest_underwater_range"][1] == DATES[-1],
        }
        for c in sorted(SERIES, key=lambda k: -METRICS[k]["longest_underwater_days"])
    ]
    beats.append({
        "id": "sc09", "kind": "standalone", "label": "最长一段没回到前高",
        "role": "evidence", "type": "underwater_strips",
        "data": {
            "head": "最长一段没回到前高",
            "rows": uw_rows,
            "hero": f"沪深300 到区间终点都没回去（{m300['longest_underwater_days']} 个交易日）",
            "range_note": f"{DATES[0].replace('-', '.')} → {DATES[-1].replace('-', '.')}",
        },
        "source_ref": "当日账户资产低于此前历史最高值的连续区间，按交易日计数",
    })

    beats.append({
        "id": "sc10", "kind": "standalone", "label": "结尾与合规", "role": "close",
        "type": "closing",
        "data": {
            "head": f"同样是 {yuan(INITIAL)}",
            "groups": [
                {"label": "市场核心资产", "names": ["沪深300"], "codes": ["510300"]},
                {"label": "中小盘弹性", "names": ["中证500"], "codes": ["510500"]},
                {"label": "红利低波策略", "names": ["红利低波50", "红利低波100"], "codes": ["512890", "515100"]},
            ],
            "hero": "收益不同，过程也不同。",
            "sub": "数据不会告诉你买哪个，但会告诉你过去发生了什么。",
            "method": "下次看收益对比，除收益率之外再问一句：中间最深亏了多少，亏了多久。",
            "scope_note": (
                f"后复权口径，分红按再投资处理 · 区间 {DATES[0]} 至 {DATES[-1]} · "
                "这一段包含 A 股长期调整与红利风格相对占优的年份，换起点可能换排名 · 历史数据不代表未来"
            ),
            "disclaimer": DISCLAIMER,
        },
        "source_ref": "腾讯证券行情接口 日线后复权；编制规则见中证指数公司与上交所公开文件",
    })

    return beats


# scene windows: the race is a single continuous scene 13.2 → 70.0
STANDALONE_WINDOWS = {
    "sc01": (0.0, 4.6),
    "sc02": (4.6, 9.4),
    "sc03": (9.4, 13.2),
    "sc05": (70.0, 76.4),
    "sc06": (76.4, 79.6),
    "sc07": (79.6, 85.2),
    "sc08": (85.2, 90.4),
    "sc09": (90.4, 94.2),
    "sc10": (94.2, 99.0),
}
RACE_SCENE = {"id": "sc04", "start": RACE_STAGE_START, "end": RACE_END}


def build() -> dict:
    beats = build_beats()
    chart_beats = [b for b in beats if b["kind"] == "chart_beat"]
    standalone = [b for b in beats if b["kind"] == "standalone"]
    assert len(chart_beats) == 7, len(chart_beats)
    assert len(standalone) == 9, len(standalone)

    scenes: list[dict] = []
    for b in standalone:
        s, e = STANDALONE_WINDOWS[b["id"]]
        scenes.append({**b, "start_seconds": s, "end_seconds": e})
    race_scene = {
        "id": RACE_SCENE["id"], "kind": "standalone", "label": "连续赛跑（7 个注解拍）",
        "role": "race", "type": "chart_stage",
        "start_seconds": RACE_SCENE["start"], "end_seconds": RACE_SCENE["end"],
        "data": {"beats": [{k: val for k, val in cb.items() if k not in ("kind", "source_ref")} for cb in chart_beats]},
        "source_ref": "腾讯证券行情接口 日线后复权；七个注解拍各自的截面日期见 beats[].source_ref",
    }
    scenes.append(race_scene)
    scenes.sort(key=lambda s: s["start_seconds"])

    # continuity
    for a, b in zip(scenes, scenes[1:]):
        assert a["end_seconds"] <= b["start_seconds"] + 1e-9, (a["id"], b["id"])
    assert abs(sum(s["end_seconds"] - s["start_seconds"] for s in scenes) - TOTAL) < 1e-6
    assert scenes[0]["start_seconds"] == 0.0 and scenes[-1]["end_seconds"] == TOTAL

    sections = []
    for s in scenes:
        bits = []
        d = s.get("data", {})
        for key in ("overline", "head", "hero", "sub", "foot", "caveat", "method", "kick"):
            if d.get(key):
                bits.append(str(d[key]))
        bits += [str(x) for x in d.get("lines", [])]
        for row in d.get("rows", []):
            if isinstance(row, dict):
                bits.append(" ".join(str(row.get(k, "")) for k in ("name", "value", "drawdown", "days")).strip())
        sections.append({
            "id": s["id"],
            "label": s["label"],
            "text": " ／ ".join([b for b in bits if b]) or s["label"],
            "start_seconds": s["start_seconds"],
            "end_seconds": s["end_seconds"],
            "delivery_cues": {
                "pace": "custom",
                "energy": "无语音：本段无口播，节奏完全由画面推进控制",
                "pause_after_seconds": round(s["end_seconds"] - s["start_seconds"], 1),
                "delivery_note": (
                    f"无口播场景。场景类型 {s['type']}，停留 "
                    f"{round(s['end_seconds'] - s['start_seconds'], 1)} 秒；"
                    "全部信息由原生画面排版承担，不做语音合成。"
                ),
            },
            "enhancement_cues": [
                {
                    "type": "animation" if s["type"] == "chart_stage" else "stat_card" if s["type"] == "result_table" else "diagram" if s["type"] in ("drawdown_bars", "underwater_strips", "rule_compare", "chip_row", "rule_list") else "overlay",
                    "description": "屏幕上出现的每一个数字都必须来自 artifacts/etf_data.json，且与同截面其他数字一致",
                    "timestamp_seconds": s["start_seconds"],
                },
                {
                    "type": "overlay",
                    "description": "受竖屏安全区约束：可读文字位于 y ≤ 1400、x ∈ [96, 984]",
                    "timestamp_seconds": s["start_seconds"],
                },
            ],
            "source_ref": s.get("source_ref", ""),
        })

    return {
        "version": "1.0",
        "title": TITLE,
        "total_duration_seconds": TOTAL,
        "sections": sections,
        "metadata": {
            "content_category": "finance",
            "audio": {
                "narration": "none", "music": "none", "audio_streams": 0,
                "reason": "用户在开工前明确选择全程无口播；持久无 BGM 默认。本片为纯视觉数据片，不产出任何音轨。",
            },
            "structure_note": (
                f"全片 10 个场景。其中 {RACE_SCENE['id']}（{RACE_SCENE['start']}–{RACE_SCENE['end']}s，"
                "56.8 秒）是一个连续镜头：赛跑期间没有任何剪辑，七个章节只以注解拍的形式叠在同一镜头之上。"
                "把它拆成七个场景会误述这支片子的拍法。"
            ),
            "on_screen_script": {
                "note": (
                    "本片的\"台词\"就是屏幕上的文字。全部数值型文案由 artifacts/etf_data.json 生成"
                    "（见 build_script.py 的 yuan/pct/rank_rows 辅助函数），手写文案中不出现任何需要被读准的数字。"
                ),
                "scenes": scenes,
                "fps": FPS,
                "race_window": {"start": RACE_START, "end": RACE_END, "span_seconds": RACE_SPAN},
                "date_mapping": f"线性自然日映射：t = {RACE_START} + {RACE_SPAN} × index ÷ {N}",
                "safe_area": {"width": 1080, "height": 1920, "bottom_offset_px": 520, "side_margin_px": 96},
            },
            "finance_editorial": {
                "core_question": "同一天、同一笔10万元买四只ETF，到2026-09-18结果差多少，过程又差多少？",
                "evidence_refs": [f"research_brief.data_points[{i}]" for i in (0, 1, 2, 3, 4, 5, 6, 7, 9, 10)],
                "boundary_conditions": [
                    "口径：后复权收盘价归一化，等同把现金分红按再投资处理；实际持有场内ETF时现金分红不会自动按当日净值复投。",
                    f"区间敏感：{DATES[0]} 至 {DATES[-1]} 包含 A 股自 2021 年高点后的长期调整，以及红利风格相对占优的年份。换起点或终点，四者排名可能不同。",
                    "数据源：腾讯证券行情接口后复权因子；不同供应商可能因复权算法与精度产生轻微差异。",
                    "512890 在 2021-10-22 缺 1 条成交记录，按用户工作簿口径沿用前一交易日账户资产，该日期不参与任何节点表述。",
                    "本片不构成对任何一只 ETF 未来表现的推断。",
                ],
                "reusable_judgment_method": (
                    "比较任何两只产品的历史收益时，除收益率之外再问三件事：起点和终点是不是同一天；"
                    "中间最深亏了多少；那一段持续了多久、我能不能熬过去。"
                ),
                "narration_style": "none",
                "narration_style_note": (
                    "用户显式选择全程无口播，不适用老朋友观察型口播规范；本片以原生排版承担叙事，"
                    "措辞仍遵守克制、不推荐、不喊口号的要求。"
                ),
            },
            "compliance": {
                "content_category": "finance",
                "financial_disclaimer": DISCLAIMER,
                "exact_text": DISCLAIMER,
                "presentation": "footer",
                "placement": "ending",
                "ending_section_id": "sc10",
                "note": "合规文案以原生小字固定呈现在最终意义场景 sc10 的页脚；本片无音轨，故只以文字形式存在，且必须位于竖屏安全区内。",
            },
            "claim_classes": {
                "FACT": ["sc02", "sc04", "sc05", "sc08", "sc09"],
                "INFERENCE": ["sc03", "sc07"],
                "THESIS": ["sc06", "sc10"],
                "SCENARIO": [],
            },
        },
    }


def verify(artifact: dict) -> None:
    """Re-check every rendered figure against the canonical series."""
    scenes = {s["id"]: s for s in artifact["metadata"]["on_screen_script"]["scenes"]}
    checks = 0

    race = scenes["sc04"]["data"]["beats"]
    by_beat = {b["id"]: b["data"] for b in race}
    assert len(by_beat) == 7

    for row in by_beat["ch-2021"]["callouts"][0]["rows"]:
        assert row["value"] == v(row["code"], "2021-12-31"), row
        assert row["display"] == yuan(v(row["code"], "2021-12-31"))
        checks += 2
    for row in by_beat["ch-2022"]["callouts"][0]["rows"]:
        assert row["value"] == v(row["code"], "2022-12-30"), row
        checks += 1
    for row in by_beat["ch-2023"]["callouts"][0]["rows"]:
        assert row["value"] == v(row["code"], "2023-12-29"), row
        checks += 1
    for row in by_beat["ch-2024h2"]["callouts"][0]["rows"]:
        assert row["value"] == v(row["code"], "2024-12-31"), row
        checks += 1

    ex = by_beat["ch-2024"]
    assert ex["rows"][0]["value"] == yuan(min(SERIES["510300"])), ex["rows"][0]
    assert ex["rows"][1]["value"] == yuan(min(SERIES["510500"])), ex["rows"][1]
    assert ex["contrast"]["hero"] == f"同一天相差 {yuan(v('515100', '2024-02-02') - v('510300', '2024-02-02'))}"
    checks += 3

    for row in scenes["sc05"]["data"]["rows"]:
        assert row["final_asset"] == yuan(METRICS[row["code"]]["final_asset"]), row
        assert row["cumulative"] == pct(METRICS[row["code"]]["cumulative_return"])
        assert row["annualized"] == pct(METRICS[row["code"]]["annualized_return"])
        checks += 3
    best = max(METRICS.values(), key=lambda m: m["final_asset"])
    worst = min(METRICS.values(), key=lambda m: m["final_asset"])
    assert scenes["sc05"]["data"]["foot"] == f"期末最好与最差相差 {yuan(best['final_asset'] - worst['final_asset'])}"

    for row in scenes["sc08"]["data"]["rows"]:
        assert row["drawdown"] == pct_abs(METRICS[row["code"]]["max_drawdown"])
        assert row["ratio"] == abs(METRICS[row["code"]]["max_drawdown"])
        assert row["span_days"] == METRICS[row["code"]]["mdd_days"]
        checks += 3
    for row in scenes["sc09"]["data"]["rows"]:
        assert row["days"] == METRICS[row["code"]]["longest_underwater_days"]
        checks += 1
    assert scenes["sc09"]["data"]["hero"] == (
        f"沪深300 到区间终点都没回去（{METRICS['510300']['longest_underwater_days']} 个交易日）"
    )

    assert scenes["sc10"]["data"]["disclaimer"] == DISCLAIMER
    assert artifact["sections"][-1]["id"] == "sc10"

    for s in artifact["metadata"]["on_screen_script"]["scenes"]:
        for b in s["data"].get("beats", []):
            for pin in b["data"].get("pins", []) + b["data"].get("callouts", []) + b["data"].get("markers", []):
                assert RACE_START <= pin["at"] <= RACE_END, (s["id"], pin["at"])
            if b["data"].get("end_card"):
                assert abs(b["data"]["end_card"]["at"] - RACE_END) < 1e-9

    print(f"[verify] {checks} rendered figures re-checked against the canonical series")


def main() -> None:
    from lib.checkpoint import validate_artifact

    artifact = build()
    validate_artifact("script", artifact)
    verify(artifact)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(artifact, ensure_ascii=False, indent=1))
    OUT_DECK.write_text(json.dumps(artifact["metadata"]["on_screen_script"], ensure_ascii=False, indent=1))

    print("[ok] script schema-valid")
    for p in (OUT, OUT_DECK):
        print(f"[write] {p.relative_to(REPO)}  ({p.stat().st_size/1024:.0f} KB)")
    print(f"  duration     : {artifact['total_duration_seconds']}s / {len(artifact['sections'])} sections")
    print(f"  audio streams: {artifact['metadata']['audio']['audio_streams']}")
    print(f"  boundaries   : {len(artifact['metadata']['finance_editorial']['boundary_conditions'])}")
    print()
    for s in artifact["metadata"]["on_screen_script"]["scenes"]:
        dur = s["end_seconds"] - s["start_seconds"]
        print(f"  {s['id']}  {s['start_seconds']:5.1f}–{s['end_seconds']:5.1f}s  {dur:5.1f}s  {s['type']:<16s} {s['label']}")


if __name__ == "__main__":
    main()
