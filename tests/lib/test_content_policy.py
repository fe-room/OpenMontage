import pytest

from lib.checkpoint import CheckpointValidationError, write_checkpoint
from lib.content_policy import (
    FINANCIAL_DISCLAIMER_ZH,
    ContentPolicyError,
    enforce_financial_disclaimer,
)


def _finance_context() -> dict:
    return {"proposal_packet": {"content_category": "finance"}}


def test_non_financial_production_is_unchanged():
    enforce_financial_disclaimer(
        "script",
        {
            "proposal_packet": {"content_category": "technology"},
            "script": {"sections": [{"text": "普通结尾"}]},
        },
    )


def test_financial_script_requires_exact_disclaimer_in_final_section():
    artifacts = _finance_context()
    artifacts["script"] = {"sections": [{"text": "市场有风险。"}]}

    with pytest.raises(ContentPolicyError, match="final script section"):
        enforce_financial_disclaimer("script", artifacts)

    artifacts["script"]["sections"].append({"text": FINANCIAL_DISCLAIMER_ZH})
    enforce_financial_disclaimer("script", artifacts)


def test_financial_scene_plan_requires_disclaimer_as_final_text_card():
    artifacts = _finance_context()
    artifacts["scene_plan"] = {
        "scenes": [
            {"type": "text_card", "description": FINANCIAL_DISCLAIMER_ZH},
            {"type": "generated", "description": "logo"},
        ]
    }

    with pytest.raises(ContentPolicyError, match="final scene"):
        enforce_financial_disclaimer("scene_plan", artifacts)

    artifacts["scene_plan"]["scenes"].append(
        {"type": "text_card", "description": FINANCIAL_DISCLAIMER_ZH}
    )
    enforce_financial_disclaimer("scene_plan", artifacts)


def test_financial_edit_requires_disclaimer_as_final_text_card_cut():
    artifacts = _finance_context()
    artifacts["edit_decisions"] = {
        "cuts": [{"type": "text_card", "text": "不构成投资建议"}]
    }

    with pytest.raises(ContentPolicyError, match="final edit cut"):
        enforce_financial_disclaimer("edit", artifacts)

    artifacts["edit_decisions"]["cuts"][-1]["text"] = FINANCIAL_DISCLAIMER_ZH
    enforce_financial_disclaimer("edit", artifacts)


def test_financial_compose_requires_rendered_end_frame_confirmation():
    artifacts = _finance_context()
    artifacts["final_review"] = {"checks": {"compliance": {}}}

    with pytest.raises(ContentPolicyError, match="present, exact, readable"):
        enforce_financial_disclaimer("compose", artifacts)

    artifacts["final_review"]["checks"]["compliance"] = {
        "financial_disclaimer_present": True,
        "financial_disclaimer_exact": True,
        "financial_disclaimer_readable": True,
        "financial_disclaimer_at_end": True,
    }
    enforce_financial_disclaimer("compose", artifacts)


def test_checkpoint_loads_upstream_classification_and_fails_closed(tmp_path):
    brief = {
        "version": "1.0",
        "title": "市场入门",
        "content_category": "finance",
        "hook": "理解市场",
        "key_points": ["风险与收益"],
        "tone": "educational",
        "style": "clean-professional",
        "target_platform": "generic",
        "target_duration_seconds": 30,
    }
    write_checkpoint(tmp_path, "finance-video", "idea", "completed", {"brief": brief})

    bad_script = {
        "version": "1.0",
        "title": "市场入门",
        "total_duration_seconds": 30,
        "sections": [
            {"id": "s1", "text": "普通结尾", "start_seconds": 0, "end_seconds": 30}
        ],
    }
    with pytest.raises(CheckpointValidationError, match="Financial video policy"):
        write_checkpoint(
            tmp_path,
            "finance-video",
            "script",
            "completed",
            {"script": bad_script},
        )
