from pathlib import Path

from lib.pipeline_loader import (
    get_conditional_skills,
    list_pipelines,
    load_pipeline,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FINANCE_SKILL = "meta/finance-video-editorial"


def _production_pipelines() -> list[str]:
    result = []
    for name in list_pipelines():
        if name == "framework-smoke":
            continue
        manifest = load_pipeline(name)
        if manifest.get("deliverable_type", "video") == "video":
            result.append(name)
    return result


def test_every_production_pipeline_declares_finance_as_conditional_only():
    for name in _production_pipelines():
        manifest = load_pipeline(name)
        assert FINANCE_SKILL not in manifest.get("required_skills", [])
        assert any(
            rule.get("skill") == FINANCE_SKILL
            and rule.get("when") == {"content_category": "finance"}
            for rule in manifest.get("conditional_skills", [])
        ), f"{name} is missing the conditional finance editorial skill"


def test_finance_context_activates_skill_and_non_finance_does_not():
    manifest = load_pipeline("animated-explainer")

    assert get_conditional_skills(
        manifest,
        context={"content_category": "finance"},
        stage_name="script",
    ) == [FINANCE_SKILL]
    assert get_conditional_skills(
        manifest,
        context={"content_category": "technology"},
        stage_name="script",
    ) == []
    assert get_conditional_skills(manifest, context=None, stage_name="script") == []


def test_routing_reads_canonical_artifact_context_and_honors_stage_allowlist():
    manifest = load_pipeline("animated-explainer")
    context = {"artifacts": {"proposal_packet": {"content_category": "Finance"}}}

    assert get_conditional_skills(
        manifest, context=context, stage_name="scene_plan"
    ) == [FINANCE_SKILL]
    assert get_conditional_skills(
        manifest, context=context, stage_name="nonexistent_stage"
    ) == []


def test_finance_skill_contains_activation_boundary_and_four_iron_rules():
    text = (PROJECT_ROOT / "skills/meta/finance-video-editorial.md").read_text()

    assert "content_category: finance" in text
    assert "For every other category" in text
    assert "question -> data/case/live-record verification -> conclusion" in text
    assert "one core question" in text
    assert "plain-language explanation" in text
    assert "reusable judgment method" in text
    assert "For non-finance productions this entire review gate is skipped" in text
