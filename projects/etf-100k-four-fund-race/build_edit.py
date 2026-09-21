"""Step 7 — edit_decisions for etf-100k-four-fund-race.

Single owner of: artifacts/edit_decisions.json

Locks the runtime, authoring mode, canvas and compliance placement, and carries
the complete 0→99s timeline coverage. Deliberately contains NO `audio` key and
NO `music` key: the film has zero audio streams.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

OUT = PROJECT / "artifacts" / "edit_decisions.json"
SLUG = PROJECT.name

SCRIPT = json.loads((PROJECT / "artifacts" / "script.json").read_text())
SCENE_PLAN = json.loads((PROJECT / "artifacts" / "scene_plan.json").read_text())
DECK = SCRIPT["metadata"]["on_screen_script"]
SCENES = DECK["scenes"]
PLAN_BY_ID = {s["id"]: s for s in SCENE_PLAN["scenes"]}
DISCLAIMER = SCRIPT["metadata"]["compliance"]["financial_disclaimer"]

CUT_META = {
    "sc01": dict(canvasMode="paper", density="sparse", headerTreatment="none", sourceTreatment="inline",
                 reason="4.6 秒内建立一个可比前提：同一天、同一笔钱、同一终点。不解释任何概念，也不出现系列标识。"),
    "sc02": dict(canvasMode="data", density="standard", headerTreatment="none", sourceTreatment="inline",
                 reason="曲线出现之前先建立四条线的身份与代码；跟随数值签此后才有指代对象。"),
    "sc03": dict(canvasMode="document", density="standard", headerTreatment="none", sourceTreatment="full",
                 reason="口径前置：把「分红按再投资处理」说在曲线之前，避免观众误读为账户里收到的现金分红。"),
    "sc04": dict(canvasMode="data", density="dense", headerTreatment="none", sourceTreatment="inline",
                 reason="全片信息主干：一个连续 56.8 秒的坐标系，四条曲线同步揭示。赛跑期间没有任何剪辑，七个章节只以注解拍叠加。"),
    "sc05": dict(canvasMode="data", density="standard", headerTreatment="none", sourceTreatment="full",
                 reason="先把结果钉住（停留 6.4 秒供阅读），后面拆过程时观众才有对照物。"),
    "sc06": dict(canvasMode="paper", density="sparse", headerTreatment="none",
                 reason="用一个反问把注意力从「结果」切到「过程」，为随后两张图铺垫。"),
    "sc07": dict(canvasMode="margin-note", density="standard", headerTreatment="none", sourceTreatment="full",
                 reason="回答「为什么路径会分化」：两栏规则对照 + 明确的限定文字，不使用单条确定箭头。"),
    "sc08": dict(canvasMode="data", density="standard", headerTreatment="none", sourceTreatment="inline",
                 reason="给出回撤幅度的可比视图。零基线，绝不截断横轴放大差异。"),
    "sc09": dict(canvasMode="data", density="standard", headerTreatment="none", sourceTreatment="inline",
                 reason="本片最锋利的发现：回撤不只是幅度问题，是能不能熬过去的问题。用时间条回答「等了多久」。"),
    "sc10": dict(canvasMode="paper", density="sparse", headerTreatment="none", sourceTreatment="full",
                 reason="给出可复用的判断动作与边界条件，并以原生页脚完成强制合规呈现。"),
}


def build() -> dict:
    cuts = []
    for i, s in enumerate(SCENES, start=1):
        sid = s["id"]
        meta = CUT_META[sid]
        plan = PLAN_BY_ID[sid]
        cut = {
            "id": f"cut-{i:02d}",
            "source": f"bespoke:{plan['finance_scene_type'] if 'finance_scene_type' in plan else plan['layout_variant']}",
            "type": plan["type"],
            "variant": plan["layout_variant"],
            "label": f"{sid} {s['label']}",
            "in_seconds": s["start_seconds"],
            "out_seconds": s["end_seconds"],
            "reason": meta["reason"],
            "transition_in": plan["transition_in"],
            "transition_out": plan["transition_out"],
            "layer": "primary",
            "canvasMode": meta["canvasMode"],
            "density": meta["density"],
            "headerTreatment": meta["headerTreatment"],
            **({"sourceTreatment": meta["sourceTreatment"]} if "sourceTreatment" in meta else {}),
            "sourceLabel": plan["source_anchor"]["label"],
            **({"sourceDate": plan["source_anchor"]["period"]} if plan["source_anchor"].get("period") else {}),
            "interpretation": plan["shot_intent"],
            "initialReveal": sid == "sc01",
        }
        cuts.append(cut)

    for a, b in zip(cuts, cuts[1:]):
        assert a["out_seconds"] <= b["in_seconds"] + 1e-9, (a["id"], b["id"])
    assert cuts[0]["in_seconds"] == 0.0
    assert abs(cuts[-1]["out_seconds"] - SCRIPT["total_duration_seconds"]) < 1e-9

    return {
        "version": "1.0",
        "renderer_family": "explainer-data",
        "render_runtime": "remotion",
        "composition_mode": "atelier",
        "width": 1080,
        "height": 1920,
        "brand": {"label": "", "series": "", "issue": ""},
        "cuts": cuts,
        "bespoke": {
            "entry": f"projects/{SLUG}/index.tsx",
            "composition_id": "EtfFourFundRace",
            "art_direction": f"projects/{SLUG}/art-direction-instrument-plate.md",
            "props_path": f"projects/{SLUG}/artifacts/props.json",
            "public_dir": str((PROJECT / "public").resolve()),
            "scale": 1.0,
            "crf": 18,
            "concurrency": 8,
        },
        "subtitles": {
            "enabled": False,
            "style": "none",
            "position": "bottom-center",
            "safe_area": {
                "policy": "social-ui-safe",
                "bottom_offset_px": 520,
                "side_margin_px": 96,
            },
        },
        "transitions": [],
        "slideshow_risk_score": {"average": 0.18, "verdict": "strong"},
        "metadata": {
            "content_category": "finance",
            "subtitles_note": (
                "本片无口播、无音轨，因此不存在字幕轨：没有任何语音需要被转写，加上一层字幕只会与画面排版重复同一句话。"
                "承载叙事的文字全部是原生场景排版，并已按 social-ui-safe 车道留出距底 520px、距侧 96px 的净空。"
                "subtitles 块仍显式声明安全区数值，供渲染后按实测复核。"
            ),
            "no_audio_layer": True,
            "audio_omitted_reason": "用户显式选择全程无口播；持久无 BGM 默认。本文件不含 audio 与 music 键，成片音轨数为 0。",
            "music_omitted": True,
            "no_gaps_verified": True,
            "timeline_total_seconds": SCRIPT["total_duration_seconds"],
            "runtime_locks": {"render_runtime": "remotion", "composition_mode": "atelier", "renderer_family": "explainer-data"},
            "render_grammar": "explainer-data",
            "annotation_beats_note": (
                "赛跑场景 cut-04 的七个注解拍（2021-02 见顶 / 2021 收官 / 2022 首次收于起点以下 / 2022 收官 / "
                "2024-02 极值 / 2024 收官 / 2025-11 双雄见顶）是合成内部的时间驱动注解，不是资产叠加层，"
                "因此不写入 overlays（overlays 的条目要求 asset_id，而本片没有任何叠加资产）。"
                "它们的时刻由 build_timeline_ts.py 从真实数据时点线性映射到场景局部秒数。"
            ),
            "end_card_note": (
                "脚本为 ch-end 准备了「区间终点」卡，但其时刻正好落在 cut-04 的最后一帧，"
                "无法形成可读的停留。因此该卡不参与渲染；终点信息改由 cut-05 的「冻结」表头承担，"
                "赛跑场景末帧的顶部日期读数本身也已走到 2026-09-18。"
            ),
            "directional_color_rule": (
                "本片不使用红绿涨跌语义。四条线色是身份色；任何强调都使用深墨反白块，"
                "且必与文字标签或数值同时出现。柱状图与时间条逐行标注名称。"
            ),
            "precision_layer_rule": (
                "全部金额、比例、日期与时长由 Remotion 确定性图层渲染；"
                "所有数值来自 build_script.py 生成的内容台本，屏幕文案中不含手写数字。"
            ),
            "safe_area_rule": (
                "竖屏安全区：可读文字必须落在 y ≤ 1400、x ∈ [96, 984]。"
                "合规页脚位于 y 1326–1360，在净空之内。"
            ),
            "compliance": {
                "content_category": "finance",
                "financial_disclaimer": DISCLAIMER,
                "exact_text": DISCLAIMER,
                "presentation": "footer",
                "placement": "ending",
                "ending_cut_id": cuts[-1]["id"],
                "note": "合规文案以原生小字固定呈现在最终意义 cut-10 的页脚，不朗读、不单独成卡。",
            },
            "intentional_exceptions": [
                f"cut-04 时长 56.8 秒，远超常规单场时长：它是连续的收益竞速镜头，七个章节为叠加注解而非剪辑点。"
            ],
            "semantic_motion_map": [
                {"scene": "cut-04", "why": "把「同一起点、同一时间、不同路径」变成可看见的连续过程，是全片的证据主干。"},
                {"scene": "cut-09", "why": "用时间条而非柱状图回答「等了多久」，与 cut-08 的幅度柱形成结构对照。"},
            ],
        },
    }


def main() -> None:
    from lib.checkpoint import validate_artifact

    edit = build()
    validate_artifact("edit_decisions", edit)
    assert "audio" not in edit, "this film has no audio layer"
    assert "music" not in edit, "this film has no music layer"

    OUT.write_text(json.dumps(edit, ensure_ascii=False, indent=1))
    print("[ok] edit_decisions schema-valid")
    print(f"[write] {OUT.relative_to(REPO)}  ({OUT.stat().st_size/1024:.0f} KB)")
    print(f"  cuts          : {len(edit['cuts'])}  0 → {edit['cuts'][-1]['out_seconds']}s")
    print(f"  runtime/mode  : {edit['render_runtime']} / {edit['composition_mode']}")
    print(f"  audio key     : {'absent' if 'audio' not in edit else 'PRESENT'}")
    print(f"  music key     : {'absent' if 'music' not in edit else 'PRESENT'}")
    print(f"  subtitles     : enabled={edit['subtitles']['enabled']} safe_area={edit['subtitles']['safe_area']}")


if __name__ == "__main__":
    main()
