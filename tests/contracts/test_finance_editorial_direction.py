"""Contracts for Finance Dossier V1.3/V1.3.1 editorial direction and flexibility."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lib.content_policy import enforce_financial_disclaimer
from lib.finance_editorial import (
    EDITORIAL_MODES,
    REQUIRED_DIRECTION_FIELDS,
    extract_editorial_direction,
    mode_profile,
    normalize_editorial_direction,
)
from lib.finance_scene_variety import (
    FinanceSceneVarietyValidator,
    validate_finance_mode_signatures,
)
from lib.pipeline_loader import load_pipeline
from schemas.artifacts import validate_artifact


ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "finance-editorial-v1.3.json"
DISCLAIMER = "本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。"


def fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text())


def direction_from_case(case: dict) -> dict:
    keys = REQUIRED_DIRECTION_FIELDS | {"secondary_mode"}
    return {key: case[key] for key in keys if key in case}


def warning_codes(result: dict) -> set[str]:
    return {warning["code"] for warning in result["warnings"]}


def test_router_fixture_covers_ten_semantic_topics_and_all_modes():
    cases = fixture()["cases"]
    assert len(cases) == 10
    normalized = [normalize_editorial_direction(direction_from_case(case)) for case in cases]
    assert {item["primary_mode"] for item in normalized} == set(EDITORIAL_MODES)
    assert all(REQUIRED_DIRECTION_FIELDS <= set(item) for item in normalized)
    assert all(item.get("secondary_mode") != item["primary_mode"] for item in normalized)


@pytest.mark.parametrize(
    ("case_id", "primary", "secondary"),
    [
        ("01-research", "RESEARCH", None),
        ("02-market", "MARKET", None),
        ("03-macro", "MACRO", "EXPLAIN"),
        ("04-flow", "FLOW", None),
        ("05-explain", "EXPLAIN", None),
        ("06-research-flow", "RESEARCH", "FLOW"),
        ("07-market-macro", "MARKET", "MACRO"),
        ("08-macro-research", "MACRO", "RESEARCH"),
        ("09-macro-policy", "MACRO", None),
        ("10-explain-research", "EXPLAIN", "RESEARCH"),
    ],
)
def test_router_fixture_expected_mode_results(case_id: str, primary: str, secondary: str | None):
    case = next(item for item in fixture()["cases"] if item["id"] == case_id)
    direction = normalize_editorial_direction(direction_from_case(case))
    assert direction["primary_mode"] == primary
    assert direction.get("secondary_mode") == secondary
    assert direction["rationale"]
    assert direction["visual_priority"]
    assert direction["canvas_preference"]
    assert direction["hook_grammar"]
    assert direction["ending_grammar"]
    assert direction["key_anti_pattern"]


def test_router_is_instruction_driven_and_explicitly_not_keyword_only():
    text = (ROOT / "skills" / "creative" / "finance-editorial-direction.md").read_text()
    for signal in ("Question", "Mechanism", "Evidence", "Takeaway", "counterfactual test"):
        assert signal in text
    assert "Do not classify from entity names or isolated keywords" in text
    assert "美联储降息为什么可能影响英伟达估值" in text
    assert "primary mode and no more than one secondary mode" in text


def test_editorial_contract_rejects_invalid_hybrid_and_execution_leakage():
    base = direction_from_case(fixture()["cases"][0])
    with pytest.raises(ValueError, match="secondary_mode must differ"):
        normalize_editorial_direction({**base, "secondary_mode": "RESEARCH"})
    with pytest.raises(ValueError, match="Unsupported secondary_mode"):
        normalize_editorial_direction({**base, "secondary_mode": ["FLOW", "MACRO"]})
    with pytest.raises(ValueError, match="must not decide scene execution"):
        normalize_editorial_direction({**base, "scene_order": ["evidence", "ending"]})


def test_existing_artifact_metadata_is_the_extension_rail():
    direction = direction_from_case(fixture()["cases"][7])
    artifact = {"metadata": {"content_category": "finance", "editorial_direction": direction}}
    assert normalize_editorial_direction(extract_editorial_direction(artifact) or {})["primary_mode"] == "MACRO"
    assert extract_editorial_direction({}) is None


def test_mode_profiles_are_strategy_priors_not_scene_plans():
    forbidden = {"scene_order", "scene_count", "layout_variant", "animation", "coordinates"}
    for mode in EDITORIAL_MODES:
        profile = mode_profile(mode)
        assert profile["primary_question"]
        assert profile["grammar"]
        assert profile["evidence_priority"]
        assert profile["visual_priority"]
        assert forbidden.isdisjoint(profile)


def test_five_representative_scene_plans_are_schema_valid_and_materially_distinct():
    data = fixture()
    cases_by_mode = {}
    for case in data["cases"]:
        cases_by_mode.setdefault(case["primary_mode"], case)

    signatures = set()
    counts = []
    validator = FinanceSceneVarietyValidator()
    for mode, sample in data["representative_scene_plans"].items():
        scenes = sample["scenes"]
        counts.append(len(scenes))
        assert scenes
        assert not (
            scenes[-1].get("type") == "text_card"
            and scenes[-1].get("description") == DISCLAIMER
        )
        compliance = sample["metadata"]["compliance"]
        assert compliance["financial_disclaimer"] == DISCLAIMER
        assert compliance["presentation"] in {"footer", "overlay"}
        assert compliance["ending_scene_id"] == scenes[-1]["id"]
        assert all(scene.get("information_role") for scene in scenes)
        assert all(scene.get("shot_intent") for scene in scenes)
        assert all(scene.get("transition_in") for scene in scenes)
        scene_plan = {
            "version": "1.0",
            "metadata": {
                "editorial_direction": direction_from_case(cases_by_mode[mode]),
                **sample["metadata"],
            },
            "scenes": scenes,
        }
        validate_artifact("scene_plan", scene_plan)
        enforce_financial_disclaimer(
            "scene_plan",
            {
                "proposal_packet": {"content_category": "finance"},
                "scene_plan": scene_plan,
            },
        )
        result = validator.validate(scene_plan)
        assert "MODE_VISUAL_MISMATCH" not in warning_codes(result)
        signatures.add(tuple(scene.get("finance_scene_type", scene["type"]) for scene in scenes))
    assert len(signatures) == 5
    assert set(counts) != {6}
    assert "MODE_SIGNATURE_TOO_REGULAR" not in warning_codes(
        validate_finance_mode_signatures(data["representative_scene_plans"])
    )


def test_scene_count_is_emergent_not_a_fixed_six_scene_contract():
    plans = fixture()["representative_scene_plans"]
    counts = [len(plan["scenes"]) for plan in plans.values()]
    assert any(count != 6 for count in counts)
    scene_skill = (ROOT / "skills" / "pipelines" / "finance-dossier" / "scene-director.md").read_text()
    assert "Scene count is an output of the story" in scene_skill
    assert "Create a new scene only when the viewer's cognitive task materially changes" in scene_skill
    assert "Merge adjacent beats" in scene_skill
    assert "Split when" in scene_skill
    assert "Do not randomize scene count" in scene_skill


def test_causal_chain_is_optional_and_used_only_for_genuine_transmission_fixture():
    plans = fixture()["representative_scene_plans"]
    for mode in ("RESEARCH", "MARKET", "FLOW", "EXPLAIN"):
        assert all(
            scene.get("finance_scene_type") != "causal_chain"
            for scene in plans[mode]["scenes"]
        )
    macro_causal = [
        scene
        for scene in plans["MACRO"]["scenes"]
        if scene.get("finance_scene_type") == "causal_chain"
    ]
    assert len(macro_causal) == 1
    assert macro_causal[0]["mechanism_importance"] is True
    assert "A influences B influences C" in macro_causal[0]["shot_intent"]


def test_compound_mode_signature_is_advisory_but_equal_count_alone_is_not():
    equal_count_only = {
        mode: {"scenes": [{"id": f"{mode}-{i}", "type": "text_card", "description": f"Task {i}"} for i in range(4)]}
        for mode in ("RESEARCH", "MARKET", "FLOW")
    }
    # Make the component sequences distinct while retaining the same count.
    equal_count_only["MARKET"]["scenes"][1]["finance_scene_type"] = "research_timeline"
    equal_count_only["FLOW"]["scenes"][1]["finance_scene_type"] = "money_flow"
    assert "MODE_SIGNATURE_TOO_REGULAR" not in warning_codes(
        validate_finance_mode_signatures(equal_count_only)
    )

    suspicious = {
        mode: {
            "scenes": [
                {"id": f"{mode}-1", "finance_scene_type": "evidence_card", "description": "Evidence"},
                {"id": f"{mode}-2", "finance_scene_type": "causal_chain", "description": "Generic why"},
                {"id": f"{mode}-3", "type": "text_card", "description": DISCLAIMER},
            ]
        }
        for mode in ("RESEARCH", "MARKET", "FLOW")
    }
    result = validate_finance_mode_signatures(suspicious)
    assert result["valid"] is True
    assert "MODE_SIGNATURE_TOO_REGULAR" in warning_codes(result)


def test_editorial_advisories_extend_existing_variety_validator():
    cases = {case["primary_mode"]: case for case in fixture()["cases"]}

    flow_plan = {
        "metadata": {"editorial_direction": direction_from_case(cases["FLOW"])},
        "scenes": [
            {"id": f"f{i}", "finance_scene_type": "evidence_card", "description": "Allocation evidence", "start_seconds": i * 5, "end_seconds": (i + 1) * 5}
            for i in range(4)
        ],
    }
    assert "MODE_VISUAL_MISMATCH" in warning_codes(FinanceSceneVarietyValidator().validate(flow_plan))

    research_plan = {
        "metadata": {"editorial_direction": direction_from_case(cases["RESEARCH"])},
        "scenes": [
            {"id": f"r{i}", "finance_scene_type": "evidence_card", "description": "Company metric", "start_seconds": i * 5, "end_seconds": (i + 1) * 5}
            for i in range(4)
        ] + [{"id": "end", "type": "text_card", "description": DISCLAIMER, "start_seconds": 20, "end_seconds": 25}],
    }
    assert "MODE_COMPONENT_OVERUSE" in warning_codes(FinanceSceneVarietyValidator().validate(research_plan))

    market_direction = direction_from_case(next(case for case in fixture()["cases"] if case["id"] == "02-market"))
    market_plan = {
        "metadata": {"editorial_direction": market_direction},
        "scenes": [
            {"id": f"m{i}", "finance_scene_type": "evidence_card" if i < 3 else "document", "description": "Slow filing evidence", "start_seconds": i * 5, "end_seconds": (i + 1) * 5}
            for i in range(5)
        ],
    }
    assert "EDITORIAL_GRAMMAR_MISMATCH" in warning_codes(FinanceSceneVarietyValidator().validate(market_plan))


def test_pipeline_and_directors_consume_editorial_direction_without_new_pipeline():
    manifest = load_pipeline("finance-dossier")
    assert "creative/finance-editorial-direction" in manifest["required_skills"]
    assert manifest["version"] == "1.3.1"
    assert len([name for name in (ROOT / "pipeline_defs").glob("finance-dossier*.yaml")]) == 1
    skill_dir = ROOT / "skills" / "pipelines" / "finance-dossier"
    for director in ("research-director.md", "proposal-director.md", "script-director.md", "scene-director.md"):
        assert "editorial_direction" in (skill_dir / director).read_text().lower()
