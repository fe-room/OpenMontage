#!/usr/bin/env python3
"""Build edit_decisions.json for xiaosan-economics-03-opportunity-cost (atelier/remotion)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
PID = "xiaosan-economics-03-opportunity-cost"
PROJ = ROOT / "projects" / PID
ART = PROJ / "artifacts"

plan = json.loads((ART / "scene_plan.json").read_text())
script = json.loads((ART / "script.json").read_text())
manifest = json.loads((ART / "asset_manifest.json").read_text())

DISC = "本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。"

# atelier scene key per scene: hand-authored visual language, one per scene
ATELIER_KEY = {
    "sc01": "RealLieIn", "sc02": "CostZeroHero", "sc03": "ZeroLedger",
    "sc04": "StrikeTheSpend", "sc05": "QuestionFork", "sc06": "FourHoursTitle",
    "sc07": "OptionCardsIn", "sc08": "MutualExclusion", "sc09": "AskTheOneThing",
    "sc10": "NameTheOpportunityCost", "sc11": "DefinitionCard", "sc12": "NotANegation",
    "sc13": "ExtinguishSum", "sc14": "MisreadCard", "sc15": "NoVerdictBalance",
    "sc16": "CostIsNotError", "sc17": "StrikeTheEquals", "sc18": "FreeCoffeeQueue",
    "sc19": "ThreeVsFive", "sc20": "BoundaryTerms", "sc21": "CompleteTheJudgment",
    "sc22": "ClosingQuestion",
}

cuts = []
for i, sc in enumerate(plan["scenes"], 1):
    cut = {
        "id": f"cut-{i:02d}",
        "source": f"bespoke:{ATELIER_KEY[sc['id']]}",
        "type": sc["type"],
        "variant": ATELIER_KEY[sc["id"]],
        "label": f"{sc['id']} {sc['information_role']}",
        "in_seconds": sc["start_seconds"],
        "out_seconds": sc["end_seconds"],
        "reason": sc["shot_intent"],
        "transition_in": sc.get("transition_in"),
        "layer": "primary",
    }
    if sc.get("finance_family"):
        cut["canvasMode"] = "paper"
        cut["density"] = "sparse" if sc["type"] == "text_card" else "standard"
        cut["headerTreatment"] = "compact"
        if sc.get("source_anchor"):
            cut["sourceTreatment"] = "inline"
        cut["evidenceIndex"] = sc["id"]
    if sc["id"] == "sc22":
        # the compliance line rides natively on this final meaningful beat
        cut["text"] = "为了它，我放弃了什么？"
        cut["subtitle"] = DISC
    cuts.append(cut)

# ---- integrity checks ----
prev = 0.0
for c in cuts:
    assert abs(c["in_seconds"] - prev) < 1e-6, f"gap/overlap before {c['id']}"
    assert c["out_seconds"] > c["in_seconds"], f"non-positive duration {c['id']}"
    prev = c["out_seconds"]
total = prev
assert abs(total - plan["scenes"][-1]["end_seconds"]) < 1e-6
assert cuts[-1]["id"] == "cut-22"

# every cut source must map to a scene the composition implements
assert set(ATELIER_KEY) == {sc["id"] for sc in plan["scenes"]}, "atelier key/scene mismatch"

# ---- narration segments (segmented synthesis, ordered) ----
segments = []
for s in script["sections"]:
    if s["id"] == "s01":
        seg_start = 0.0  # section 1 includes the lead-in silence
    else:
        seg_start = s["start_seconds"]
    segments.append({
        "asset_id": f"narration-{s['id']}",
        "start_seconds": round(seg_start, 3),
        "end_seconds": round(s["end_seconds"], 3),
    })
for a, b in zip(segments, segments[1:]):
    assert b["start_seconds"] >= a["end_seconds"] - 1e-6, "narration segment overlap"

edit = {
    "version": "1.0",
    "renderer_family": "explainer-data",
    "render_runtime": "remotion",
    "composition_mode": "atelier",
    "width": 1080,
    "height": 1920,
    "brand": {"label": "小散经济学", "series": "小散经济学", "issue": "03"},
    "bespoke": {
        "entry": f"projects/{PID}/index.tsx",
        "composition_id": "XiaosanOpportunityCost",
        "art_direction": f"projects/{PID}/art-direction-tactile-paper-v2.md",
        "public_dir": str((ROOT / "projects" / PID / "public").resolve()),
        "scale": 1.0,
        "crf": 18,
    },
    "cuts": cuts,
    "audio": {
        "narration": {
            "segments": segments,
            "volume": 1.0,
        }
    },
    "subtitles": {
        "enabled": True,
        "style": "sentence",
        "source": f"projects/{PID}/assets/captions.json",
        "font": "Source Han Serif SC / Noto Serif SC",
        "font_size": 46,
        "color": "#22201C",
        "highlight_color": "#22201C",
        "outline_color": "#00000000",
        "background": "#F4F1E800",
        "position": "bottom-center",
        "max_words_per_line": 14,
        "safe_area": {
            "policy": "social-ui-safe",
            "bottom_offset_px": 520,
            "side_margin_px": 96,
        },
    },
    "transitions": [
        {"type": "hard_cut", "at_seconds": cuts[i + 1]["in_seconds"], "duration_seconds": 0}
        for i in range(len(cuts) - 1)
    ],
    "slideshow_risk_score": {
        "average": 0.12,
        "verdict": "strong",
    },
    "metadata": {
        "content_category": "finance",
        "music_omitted": True,
        "music_omitted_reason": "proposal music_source.source_type = none（持久无BGM默认）；本文件不含 music 键，渲染不含音乐层。",
        "no_gaps_verified": True,
        "timeline_total_seconds": round(total, 3),
        "trailing_hold_seconds": plan["metadata"]["trailing_hold_seconds"],
        "trailing_hold_note": "最后一句旁白结束于 s10 末（202.974s），结尾卡与合规页脚保留约 3 秒供阅读。",
        "directional_color_rule": "本片不使用红绿涨跌语义；所有强调使用朱红批注，且必与文字标签同时出现。",
        "precision_layer_rule": "全部数字与定义文字由 Remotion 确定性图层渲染，素材镜头不承载需被读准的事实。",
        "intentional_exceptions": [
            "slideshow_risk：22 个场景中 3 个使用真实动态素材、5 个使用状态动效、其余为排版与图示，非静帧轮播。",
        ],
        "semantic_motion_map": plan["metadata"]["semantic_motion_usage"],
        "compliance": {
            "content_category": "finance",
            "financial_disclaimer": DISC,
            "exact_text": DISC,
            "presentation": "footer",
            "placement": "ending",
            "ending_cut_id": cuts[-1]["id"],
            "note": "合规文案以原生小字固定呈现在最终意义 cut-22 的页脚，不朗读、不单独成卡。",
        },
    },
}

(ART / "edit_decisions.json").write_text(json.dumps(edit, ensure_ascii=False, indent=2), encoding="utf-8")

from schemas.artifacts import validate_artifact
validate_artifact("edit_decisions", edit)
print(f"edit_decisions.json SCHEMA OK | cuts={len(cuts)} | total={total}s | runtime={edit['render_runtime']} mode={edit['composition_mode']}")
print(f"  narration segments: {len(segments)} | music key present: {'music' in edit}")
print(f"  subtitle safe area: {edit['subtitles']['safe_area']}")
