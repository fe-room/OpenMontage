"""Step 4 — scene_plan for etf-100k-four-fund-race.

Single owner of: artifacts/scene_plan.json

Derives scenes from the approved script and attaches finance-scene metadata,
using only the closed vocabularies declared in scene_plan.schema.json.

Vocabulary note: the schema's `finance_scene_type` enum has no plain "card" for
a pure typography beat, so the opening/turn/closing scenes omit both
`finance_scene_type` and `finance_family` deliberately — they are framing type,
not finance-evidence scenes. That omission is the accurate record, not a gap.

Runs the real FinanceSceneVarietyValidator and stores its output verbatim so
advisory warnings are reviewed rather than hidden.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

OUT = PROJECT / "artifacts" / "scene_plan.json"
SCRIPT = json.loads((PROJECT / "artifacts" / "script.json").read_text())
DATA = json.loads((PROJECT / "artifacts" / "etf_data.json").read_text())
DATES = DATA["dates"]

ASSET_DATA = {
    "type": "data",
    "description": "四只ETF自 2020-07-03 起的 1510 个交易日账户资产序列、回撤与未创新高统计（由用户工作簿导出）",
    "source": "provided",
}
ASSET_COPY = {
    "type": "copy_deck",
    "description": "本片屏幕文案与注解节点表；所有数值由数据生成，不含手写数字",
    "source": "generate",
}

# finance_scene_type is validated against a closed enum:
# document | chart | evidence_card | expectation_gap | money_flow | causal_chain
# | research_timeline | scenario_board | thesis_breaker | watch_list
# `type` is validated against: talking_head | broll | animation | character_scene
# | diagram | text_card | transition | generated | screen_recording
SCENE_META = {
    "sc01": {
        "type": "text_card", "narrative_role": "establish_context",
        "layout_variant": "question-cascade",
        "information_role": "frame_the_comparison",
        "shot_size": "establishing",
        "framing": "full-frame type, no chart yet",
        "movement": "三行文字依次落定，无缩放无旋转",
        "shot_intent": "在 4.6 秒内建立「同一天、同一笔钱、同一终点」的可比前提，不解释任何概念",
        "anchor": {"label": "区间起点与初始资金，见口径说明", "period": f"{DATES[0]} 起", "tier": 1},
        "assets": [ASSET_COPY],
        "claim_class": "THESIS",
    },
    "sc02": {
        "type": "diagram", "narrative_role": "introduce_subject",
        "layout_variant": "chip-row",
        "information_role": "establish_identities",
        "shot_size": "insert",
        "framing": "四张身份牌竖向排列，每张含色点、名称、代码与定位",
        "movement": "身份牌逐张落定，每张 0.18 秒收势",
        "shot_intent": "在曲线出现之前让观众认识四条线的身份与代码，后续跟随标签才有指代对象",
        "anchor": {
            "label": "基金公司与交易所公开产品资料：名称、代码、跟踪指数、成立时间",
            "url": "https://etf.sse.com.cn/fundtrends/c/5733322.shtml",
            "period": "截至 2026-09", "tier": 1,
        },
        "assets": [ASSET_COPY],
        "finance_family": "DATA", "finance_scene_type": "evidence_card", "claim_class": "FACT",
    },
    "sc03": {
        "type": "text_card", "narrative_role": "establish_context",
        "layout_variant": "rule-sheet",
        "information_role": "declare_measurement_terms",
        "shot_size": "insert",
        "framing": "四行键值对，左对齐，等宽数字",
        "movement": "逐行淡入后 START 落定",
        "shot_intent": "口径前置：先说明这是分红按再投资处理的总回报，避免观众误读为账户里收到的现金分红",
        "anchor": {
            "label": "用户工作簿「口径说明」工作表：后复权口径、账户资产公式、区间端点",
            "period": f"{DATES[0]} 至 {DATES[-1]}", "tier": 1,
        },
        "assets": [ASSET_COPY],
        "finance_family": "DOCUMENT", "finance_scene_type": "document", "claim_class": "INFERENCE",
    },
    "sc04": {
        "type": "animation", "narrative_role": "deliver_payload",
        "layout_variant": "normalized-line-race",
        "information_role": "carry_the_whole_evidence",
        "shot_size": "wide",
        "framing": "单一连续坐标系：纵轴账户资产（元），横轴日期，¥100,000 虚线起跑线与线下水下带",
        "movement": "clipPath 自左向右揭示；末端双行数值签跟随边界并做竖向防重叠；年份刻度随进度点亮",
        "shot_intent": "把「同一起点、同一时间、不同路径」变成可看见的连续过程；七个注解拍承载章节，全程不剪辑",
        "anchor": {
            "label": "腾讯证券行情接口 日线后复权（hfq），1510 个交易日，四个数值取自同一截面",
            "url": "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get",
            "period": f"{DATES[0]} 至 {DATES[-1]}", "tier": 2,
        },
        "assets": [ASSET_DATA],
        "finance_family": "DATA", "finance_scene_type": "chart", "claim_class": "FACT",
        "hero_moment": True,
    },
    "sc05": {
        "type": "diagram", "narrative_role": "deliver_payload",
        "layout_variant": "result-ledger",
        "information_role": "state_the_outcome",
        "shot_size": "insert",
        "framing": "四行台账，三列数字右对齐，等宽字体",
        "movement": "按资产降序逐行落定；页脚差值先计数再精确落到真值",
        "shot_intent": "先让观众记住结果再拆过程；停留 6.4 秒供阅读",
        "anchor": {
            "label": "同区间的最终资产、累计收益率与年化收益率，口径与曲线场景一致",
            "url": "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get",
            "period": f"{DATES[0]} 至 {DATES[-1]}", "tier": 2,
        },
        "assets": [ASSET_DATA],
        "finance_family": "DATA", "finance_scene_type": "evidence_card", "claim_class": "FACT",
        "hero_moment": True,
    },
    "sc06": {
        "type": "text_card", "narrative_role": "build_tension",
        "layout_variant": "single-turn",
        "information_role": "reset_the_question",
        "shot_size": "establishing",
        "framing": "单行主句，两行支撑句",
        "movement": "主句硬切出现，支撑句随后",
        "shot_intent": "把观众注意力从「结果」切换到「过程」，为回撤的两张图铺垫",
        "anchor": {"label": "最大回撤幅度与其跨度，来源见紧接的两个场景", "tier": 2},
        "assets": [ASSET_COPY],
        "claim_class": "THESIS",
        "hero_moment": True,
    },
    "sc07": {
        "type": "diagram", "narrative_role": "comparison",
        "layout_variant": "rule-compare",
        "information_role": "explain_the_divergence",
        "shot_size": "wide",
        "framing": "两栏规则对照（各含三根示意权重条），下方一条限定说明",
        "movement": "先左栏后右栏，最后一栏限定说明淡入",
        "shot_intent": "回答「为什么路径会分化」：差别在指数的加权规则，不在基金经理",
        "anchor": {
            "label": "中证指数有限公司编制公告（沪深300 与中证500 按调整市值加权）；上海证券交易所 ETF 产品页（中证红利低波动指数按股息率加权）",
            "url": "http://www.csindex.com.cn/#/about/newsDetail?id=5421",
            "period": "现行编制方案，截至 2026-08 公开资料", "tier": 1,
        },
        "assets": [ASSET_COPY],
        "finance_family": "MECHANISM", "finance_scene_type": "causal_chain",
        "claim_class": "INFERENCE", "mechanism_importance": True,
        "finance_justification": (
            "全片唯一的机制镜头，且它的链条只有两跳是确定的：加权规则 → 成分股权重分布 → 选出的股票集合不同。"
            "第三跳（因此这段区间里表现分化）还依赖风格环境，所以画面用两栏规则对照 + 明确限定文字，"
            "而不是一条确定的箭头。选 causal_chain 是因为观众任务确实是在追问「为什么路径不同」，"
            "且 mechanism_importance=true；chart 或 evidence_card 都无法表达两套规则的对照。"
        ),
    },
    "sc08": {
        "type": "animation", "narrative_role": "evidence",
        "layout_variant": "zero-baseline-bars",
        "information_role": "quantify_the_pain",
        "shot_size": "insert",
        "framing": "四根横向柱共用零基线，数值落在柱端",
        "movement": "柱体按幅度降序从基线长出；回撤跨度天数随后淡入",
        "shot_intent": "给出回撤幅度的可比视图；零基线，绝不截断横轴放大差异",
        "anchor": {
            "label": "每日账户资产相对此前历史峰值的最大跌幅，四只同一算法",
            "url": "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get",
            "period": f"峰值日与低点日见各行标注，区间 {DATES[0]} 至 {DATES[-1]}", "tier": 2,
        },
        "assets": [ASSET_DATA],
        "finance_family": "DATA", "finance_scene_type": "chart", "claim_class": "FACT",
        "finance_justification": (
            "与紧邻的下一场同为 chart，但两者回答两个不同问题、用两种不同图形："
            "本场回答「跌了多少」（幅度，零基线横向柱），下一场回答「等了多久」（持续时间，时间条）。"
            "这正是本片的核心论点——幅度相近而跨度相差近20倍——并列出现是论点的结构要求，不是版式重复。"
        ),
    },
    "sc09": {
        "type": "animation", "narrative_role": "evidence",
        "layout_variant": "underwater-strips",
        "information_role": "quantify_the_wait",
        "shot_size": "insert",
        "framing": "四条横向日期条，未创新高区间填深色，右侧标交易日数",
        "movement": "条带自左向右绘制，计数随后落定；仍未回本的那一段闪烁一次",
        "shot_intent": "本片最锋利的发现：回撤不只是幅度问题，是能不能熬过去的问题",
        "anchor": {
            "label": "当日账户资产低于此前历史最高值的连续区间，按交易日计数",
            "url": "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get",
            "period": "各自最长的一段未创新高区间，见各行标注", "tier": 2,
        },
        "assets": [ASSET_DATA],
        "finance_family": "DATA", "finance_scene_type": "chart", "claim_class": "FACT",
        "hero_moment": True,
    },
    "sc10": {
        "type": "text_card", "narrative_role": "resolution",
        "layout_variant": "group-close",
        "information_role": "complete_the_judgment",
        "shot_size": "establishing",
        "framing": "三行分组 + 主句 + 可复用方法 + 口径小字 + 原生合规页脚",
        "movement": "分组先出现，主句其次，方法再次；页脚静止可读",
        "shot_intent": "给出可复用的判断动作与边界条件，并以原生页脚完成强制合规呈现",
        "anchor": {
            "label": "全片数据来源与编制规则来源的合并声明；合规文案为 AGENT_GUIDE 原文",
            "period": f"{DATES[0]} 至 {DATES[-1]}", "tier": 2,
        },
        "assets": [ASSET_COPY],
        "claim_class": "THESIS",
        "hero_moment": True,
    },
}


def build() -> dict:
    scenes = []
    for s in SCRIPT["metadata"]["on_screen_script"]["scenes"]:
        m = SCENE_META[s["id"]]
        dur = round(s["end_seconds"] - s["start_seconds"], 1)
        scene = {
            "id": s["id"],
            "type": m["type"],
            "description": (
                f"{s['label']}。{m['shot_intent']}。"
                f"画面：{m['framing']}；动态：{m['movement']}。停留 {dur} 秒。"
            ),
            "start_seconds": s["start_seconds"],
            "end_seconds": s["end_seconds"],
            "script_section_id": s["id"],
            "framing": m["framing"],
            "movement": m["movement"],
            "transition_in": "冷开场，无转场铺垫" if s["id"] == "sc01" else "硬切，无转场效果",
            "transition_out": "硬切",
            "shot_language": {
                "shot_size": m["shot_size"],
                "camera_movement": "static",
                "lighting_key": "high_key",
                "depth_of_field": "deep",
                "color_temperature": "cool",
            },
            "shot_intent": m["shot_intent"],
            "narrative_role": m["narrative_role"],
            "information_role": m["information_role"],
            "hero_moment": m.get("hero_moment", False),
            "texture_keywords": ["instrument-plate", "fine-grid", "monospace-numerals", "zero-baseline"],
            "claim_class": m["claim_class"],
            "source_anchor": m["anchor"],
            "layout_variant": m["layout_variant"],
            "required_assets": m["assets"],
            "overlay_notes": (
                "竖屏安全区：可读文字限定在 y ≤ 1400、x ∈ [96, 984]。"
                + (
                    "本场为连续镜头，七个注解拍（"
                    + "、".join(b["label"] for b in s["data"]["beats"])
                    + "）叠在同一镜头之上，不产生剪辑点。"
                    if s["id"] == "sc04"
                    else ""
                )
            ),
        }
        if "finance_family" in m:
            scene["finance_family"] = m["finance_family"]
        if "finance_scene_type" in m:
            scene["finance_scene_type"] = m["finance_scene_type"]
        if "mechanism_importance" in m:
            scene["mechanism_importance"] = m["mechanism_importance"]
        if "finance_justification" in m:
            scene["finance_justification"] = m["finance_justification"]
        scenes.append(scene)

    return {
        "version": "1.0",
        "style_playbook": "finance-dossier",
        "scenes": scenes,
        "metadata": {
            "content_category": "finance",
            "canvas": SCRIPT["metadata"]["on_screen_script"]["safe_area"],
            "structure_note": SCRIPT["metadata"]["structure_note"],
            "compliance": {
                **SCRIPT["metadata"]["compliance"],
                "ending_scene_id": "sc10",
                "note": (
                    "合规文案以原生小字固定呈现在最终意义场景 sc10 的页脚（presentation=footer，"
                    "embedded 形态），不朗读、不单独成卡。本片无音轨，故该文案只以文字形式存在，"
                    "且必须位于竖屏安全区（距底 520px）之内。"
                ),
            },
            "scene_roles": {s["id"]: s["role"] for s in SCRIPT["metadata"]["on_screen_script"]["scenes"]},
            "runtime_locks": {"render_runtime": "remotion", "composition_mode": "atelier",
                              "renderer_family": "explainer-data"},
            "vocabulary_note": (
                "开场、转折与结尾三场是纯排版框定场景，schema 的 finance_scene_type 枚举里没有对应值，"
                "因此这三场有意不带 finance_scene_type 与 finance_family —— 它们不是财经证据场景。"
            ),
        },
    }


def main() -> None:
    from lib.checkpoint import validate_artifact
    from lib.finance_scene_variety import validate_finance_scene_variety

    payload = build()
    brief = json.loads((PROJECT / "artifacts" / "research_brief.json").read_text())
    payload["metadata"]["editorial_direction"] = brief["metadata"]["editorial_direction"]

    validate_artifact("scene_plan", payload)

    verdict = validate_finance_scene_variety(payload)
    payload["metadata"]["variety_validation"] = verdict
    validate_artifact("scene_plan", payload)

    scenes = payload["scenes"]
    assert scenes[0]["start_seconds"] == 0.0
    for a, b in zip(scenes, scenes[1:]):
        assert a["end_seconds"] <= b["start_seconds"] + 1e-9, (a["id"], b["id"])
    for s in scenes:
        d = s["end_seconds"] - s["start_seconds"]
        assert d >= 2.0, (s["id"], d)
    for s in scenes:
        if s.get("claim_class") == "FACT":
            assert s.get("source_anchor", {}).get("label"), s["id"]

    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1))
    print("[ok] scene_plan schema-valid")
    print(f"[write] {OUT.relative_to(REPO)}  ({OUT.stat().st_size/1024:.0f} KB)")
    summ = verdict["summary"]
    print(f"  scenes       : {summ['scene_count']}  duration {summ['duration_seconds']:g}s")
    print(f"  families     : {summ['families']}")
    print(f"  type counts  : {summ['type_counts']}")
    print(f"  editorial    : {summ['editorial_mode']}")
    print(f"  warnings     : {len(verdict['warnings'])}")
    for w in verdict["warnings"]:
        print(f"    ! {w['code']}")
        print(f"      {w['message'][:150]}")
        print(f"      scenes: {w['scene_ids']}")


if __name__ == "__main__":
    main()
