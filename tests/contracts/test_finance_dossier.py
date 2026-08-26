"""Contract tests for the additive finance-dossier content system."""

from __future__ import annotations

import json
from pathlib import Path

from lib.checkpoint import init_project, write_checkpoint
from lib.finance_scene_variety import FinanceSceneVarietyValidator
from lib.pipeline_loader import get_stage_order, load_pipeline
from schemas.artifacts import validate_artifact
from styles.playbook_loader import load_playbook
from tools.analysis.composition_validator import CompositionValidator


ROOT = Path(__file__).resolve().parents[2]
DISCLAIMER = "本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。"
FINANCE_TYPES = {
    "evidence_card",
    "expectation_gap",
    "money_flow",
    "causal_chain",
    "research_timeline",
    "scenario_board",
    "thesis_breaker",
}


def warning_codes(result: dict) -> set[str]:
    return {warning["code"] for warning in result["warnings"]}


def test_finance_dossier_manifest_is_valid_and_uses_canonical_lifecycle():
    manifest = load_pipeline("finance-dossier")
    assert manifest["metadata"]["canonical_content_category"] == "finance"
    assert get_stage_order(manifest) == [
        "research",
        "proposal",
        "script",
        "scene_plan",
        "assets",
        "edit",
        "compose",
        "cover",
        "publish",
    ]
    assert manifest["compatible_playbooks"]["recommended"] == ["finance-dossier"]
    assert "creative/finance-storytelling" in manifest["required_skills"]
    assert "meta/finance-video-editorial" not in manifest["required_skills"]


def test_finance_directors_and_storytelling_skill_exist():
    skill_dir = ROOT / "skills" / "pipelines" / "finance-dossier"
    expected = {
        "executive-producer.md",
        "research-director.md",
        "proposal-director.md",
        "script-director.md",
        "scene-director.md",
        "asset-director.md",
        "edit-director.md",
        "compose-director.md",
        "publish-director.md",
    }
    assert expected == {path.name for path in skill_dir.glob("*.md")}
    storytelling = (ROOT / "skills" / "creative" / "finance-storytelling.md").read_text()
    for token in ("FACT", "INFERENCE", "THESIS", "SCENARIO", "CONTRADICTION", "THESIS_BREAKER"):
        assert token in storytelling
    assert DISCLAIMER in storytelling


def test_finance_playbook_validates_against_current_schema():
    playbook = load_playbook("finance-dossier")
    palette = playbook["visual_language"]["color_palette"]
    assert palette["background"] == "#F2EFE7"
    assert palette["text"] == "#171715"
    assert "generic businessmen" in playbook["asset_generation"]["image_negative_prompt"]
    assert any("color" in rule.lower() for rule in playbook["quality_rules"])


def test_finance_edit_decisions_remain_a_canonical_artifact():
    artifact = {
        "version": "1.0",
        "render_runtime": "remotion",
        "composition_mode": "templated",
        "width": 1080,
        "height": 1920,
        "brand": {"label": "Research Desk", "issue": "Dossier 001"},
        "cuts": [
            {
                "id": "evidence-1",
                "source": "",
                "in_seconds": 0,
                "out_seconds": 5,
                "type": "evidence_card",
                "label": "Revenue",
                "primaryValue": "+18%",
                "supportingMetrics": [{"label": "Cash conversion", "value": "61%", "direction": "down"}],
                "period": "FY2030 Q2 / SAMPLE DATA",
                "sourceLabel": "Fictional filing",
                "sampleData": True,
                "variant": "document",
            },
            {
                "id": "zero-gap",
                "source": "",
                "in_seconds": 5,
                "out_seconds": 10,
                "type": "expectation_gap",
                "metric": "Zero is valid",
                "expectedValue": 0,
                "actualValue": -8,
                "delta": -8,
                "unit": "%",
                "variant": "split",
                "sampleData": True,
            },
        ],
    }
    assert validate_artifact("edit_decisions", artifact) is None


def test_demo_props_are_zero_asset_valid_and_cover_required_components():
    path = ROOT / "remotion-composer" / "public" / "demo-props" / "finance-dossier-sample.json"
    props = json.loads(path.read_text())
    assert (props["width"], props["height"]) == (1080, 1920)
    result = CompositionValidator().execute(
        {
            "composition_path": str(path),
            "assets_root": str(ROOT / "remotion-composer" / "public"),
            "render_runtime": "remotion",
        }
    )
    assert result.success, result.error
    cut_types = {cut.get("type") for cut in props["cuts"]}
    assert FINANCE_TYPES <= cut_types
    assert props["cuts"][-1]["text"] == DISCLAIMER
    assert all(
        cut.get("sampleData") is True or cut.get("type") == "text_card"
        for cut in props["cuts"]
    )


def test_explainer_resolution_fixtures_preserve_legacy_default_and_finance_vertical():
    props_dir = ROOT / "remotion-composer" / "test-fixtures"
    legacy = json.loads((props_dir / "legacy-explainer.json").read_text())
    finance = json.loads((ROOT / "remotion-composer" / "public" / "demo-props" / "finance-dossier-sample.json").read_text())
    assert "width" not in legacy and "height" not in legacy
    assert (finance["width"], finance["height"]) == (1080, 1920)


def test_finance_components_are_exported_and_dispatched():
    finance_dir = ROOT / "remotion-composer" / "src" / "components" / "finance"
    assert (finance_dir / "FinanceFrame.tsx").is_file()
    assert "SourceStrip" in (finance_dir / "index.ts").read_text()
    explainer = (ROOT / "remotion-composer" / "src" / "Explainer.tsx").read_text()
    for scene_type in FINANCE_TYPES:
        assert f'cut.type === "{scene_type}"' in explainer
    assert "Math.random" not in "".join(path.read_text() for path in finance_dir.glob("*.tsx"))


def test_finance_scene_variety_validator_emits_all_requested_warning_classes():
    scenes = [
        {
            "id": f"s{i}",
            "type": "animation",
            "finance_scene_type": "evidence_card",
            "finance_family": "DATA",
            "claim_class": "FACT",
            "description": "This mechanism causes the next result.",
            "mechanism_importance": i == 0,
            "start_seconds": i * 10,
            "end_seconds": (i + 1) * 10,
        }
        for i in range(5)
    ]
    result = FinanceSceneVarietyValidator().validate({"scenes": scenes})
    codes = warning_codes(result)
    assert result["valid"] is True
    assert {
        "VISUAL_MONOTONY_RISK",
        "CARD_OVERUSE",
        "REPEATED_SCENE_TYPE",
        "LOW_VISUAL_FAMILY_DIVERSITY",
        "NO_MECHANISM_VISUAL",
        "MISSING_SOURCE_ANCHOR",
    } <= codes


def test_finance_scene_variety_validator_accepts_a_simple_evidence_mechanism_decision_plan():
    scenes = [
        {"id": "doc", "finance_scene_type": "research_timeline", "finance_family": "DOCUMENT", "claim_class": "FACT", "source_anchor": {"label": "Filing"}, "start_seconds": 0, "end_seconds": 15},
        {"id": "flow", "finance_scene_type": "money_flow", "finance_family": "MECHANISM", "mechanism_importance": True, "start_seconds": 15, "end_seconds": 30},
        {"id": "decision", "finance_scene_type": "thesis_breaker", "finance_family": "DECISION", "claim_class": "THESIS", "start_seconds": 30, "end_seconds": 45},
    ]
    result = FinanceSceneVarietyValidator().validate(scenes)
    assert warning_codes(result).isdisjoint({"LOW_VISUAL_FAMILY_DIVERSITY", "NO_MECHANISM_VISUAL", "MISSING_SOURCE_ANCHOR"})


def test_legacy_financial_stat_visuals_need_sources_only_for_unclassified_numeric_claims():
    validator = FinanceSceneVarietyValidator()
    missing = validator.validate([
        {"id": "stat", "visual_type": "stat_card", "description": "Revenue growth was 0%"},
        {"id": "kpi", "visual_type": "kpi_grid", "description": "利润为0亿元"},
    ])
    assert warning_codes(missing) == {"CARD_OVERUSE", "MISSING_SOURCE_ANCHOR"}
    missing_ids = next(w["scene_ids"] for w in missing["warnings"] if w["code"] == "MISSING_SOURCE_ANCHOR")
    assert missing_ids == ["stat", "kpi"]

    non_facts = validator.validate([
        {"id": "scenario", "visual_type": "stat_card", "claim_class": "SCENARIO", "description": "Scenario +30%"},
        {"id": "thesis", "visual_type": "kpi_grid", "claim_class": "THESIS", "description": "Thesis 0%"},
        {"id": "decorative", "visual_type": "stat_card", "description": "Decorative chapter divider"},
    ])
    assert "MISSING_SOURCE_ANCHOR" not in warning_codes(non_facts)


def test_finance_variety_validator_runs_automatically_at_scene_plan_checkpoint(tmp_path):
    project_id = "finance-auto-validator"
    init_project(project_id, title="Finance", pipeline_type="finance-dossier", pipeline_dir=tmp_path)
    scene_plan = {
        "version": "1.0",
        "scenes": [
            {
                "id": "fact",
                "type": "animation",
                "description": "Revenue was 0%",
                "start_seconds": 0,
                "end_seconds": 4,
                "finance_scene_type": "evidence_card",
                "finance_family": "DATA",
                "claim_class": "FACT",
            },
            {
                "id": "disclaimer",
                "type": "text_card",
                "description": DISCLAIMER,
                "start_seconds": 4,
                "end_seconds": 9,
            },
        ],
    }
    path = write_checkpoint(
        tmp_path,
        project_id,
        "scene_plan",
        "awaiting_human",
        {"scene_plan": scene_plan},
        pipeline_type="finance-dossier",
        review={"findings": []},
    )
    checkpoint = json.loads(path.read_text())
    result = checkpoint["review"]["finance_scene_variety"]
    codes = [warning["code"] for warning in result["warnings"]]
    assert "MISSING_SOURCE_ANCHOR" in codes
    assert len(codes) == len(set(codes))
    second_path = write_checkpoint(
        tmp_path,
        project_id,
        "scene_plan",
        "awaiting_human",
        {"scene_plan": scene_plan},
        pipeline_type="finance-dossier",
        review=checkpoint["review"],
    )
    second = json.loads(second_path.read_text())["review"]["finance_scene_variety"]["warnings"]
    signatures = [(warning["code"], tuple(warning["scene_ids"])) for warning in second]
    assert len(signatures) == len(set(signatures))


def test_finance_component_contracts_cover_zero_values_and_distinct_variants():
    explainer = (ROOT / "remotion-composer" / "src" / "Explainer.tsx").read_text()
    gap = (ROOT / "remotion-composer" / "src" / "components" / "finance" / "ExpectationGap.tsx").read_text()
    flow = (ROOT / "remotion-composer" / "src" / "components" / "finance" / "MoneyFlow.tsx").read_text()
    assert "isPresent(cut.expectedValue)" in explainer
    for variant in ('variant === "split"', 'variant === "stacked"', 'variant === "delta"', 'variant === "reveal"'):
        assert variant in gap
    assert "sankeyStrokeWidth" in flow and "C ${" in flow
    assert "MIN_SANKEY_WIDTH" in flow and "MAX_SANKEY_WIDTH" in flow
    assert "node.value !== undefined && node.value !== null" in flow


def test_finance_engine_branding_is_not_rendered():
    finance_frame = (ROOT / "remotion-composer" / "src" / "components" / "finance" / "FinanceFrame.tsx").read_text()
    assert "OPENMONTAGE" not in finance_frame.upper()
    assert 'brand?.label || "FINANCE DOSSIER"' in finance_frame


def test_finance_playbook_resolves_one_effective_remotion_theme():
    from tools.video.video_compose import VideoCompose

    theme = VideoCompose._build_theme_from_playbook("finance-dossier", {})
    assert theme is not None
    assert theme["backgroundColor"] == "#F2EFE7"
    assert theme["surfaceColor"] == "#F8F5ED"
    assert theme["mutedTextColor"] == "#6C6860"
    assert theme["chartColors"][:3] == ["#345C5B", "#B44736", "#C5A64A"]
