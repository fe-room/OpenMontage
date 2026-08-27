"""Deterministic warning-only validation for finance-dossier scene plans.

The generic variation checker evaluates cinematography. This module evaluates the
finance scene grammar: evidence anchors, conceptual families, mechanism coverage,
and component repetition. It never hard-fails a production; directors review the
warnings and may record a deliberate justification for a simple plan.
"""

from __future__ import annotations

from collections import Counter
import json
import re
from typing import Any

from lib.finance_editorial import extract_editorial_direction, normalize_editorial_direction


FINANCE_TYPES = {
    "document",
    "chart",
    "evidence_card",
    "expectation_gap",
    "money_flow",
    "causal_chain",
    "research_timeline",
    "scenario_board",
    "thesis_breaker",
    "watch_list",
}
CARD_LIKE_TYPES = {"stat_card", "kpi_grid", "evidence_card", "expectation_gap"}
MECHANISM_TYPES = {"money_flow", "causal_chain"}
FACTUAL_TYPES = {"chart", "evidence_card", "expectation_gap", "research_timeline"}
LEGACY_FINANCIAL_DATA_TYPES = {"stat_card", "kpi_grid"}
FINANCIAL_NUMBER_RE = re.compile(
    r"(?:[-+−]?\d[\d,.]*(?:\.\d+)?\s*(?:%|％|bps?|pts?|元|万元|亿元|美元|倍))"
    r"|(?:[¥￥$€]\s*[-+−]?\d[\d,.]*(?:\.\d+)?)",
    re.IGNORECASE,
)
TRANSMISSION_TERMS = {"transmission", "transmit", "causal", "传导", "因果路径"}


def _finance_type(scene: dict[str, Any]) -> str:
    explicit = scene.get("finance_scene_type") or scene.get("visual_type")
    if explicit:
        return str(explicit).strip().lower()
    return str(scene.get("type", "unspecified")).strip().lower()


def _family(scene: dict[str, Any]) -> str | None:
    explicit = scene.get("finance_family")
    if explicit:
        return str(explicit).strip().upper()
    scene_type = _finance_type(scene)
    if scene_type in {"document", "research_timeline"}:
        return "DOCUMENT"
    if scene_type in {"chart", "stat_card", "kpi_grid", "evidence_card", "expectation_gap"}:
        return "DATA"
    if scene_type in MECHANISM_TYPES:
        return "MECHANISM"
    if scene_type in {"scenario_board", "thesis_breaker", "watch_list"}:
        return "DECISION"
    return None


def _warn(code: str, message: str, scene_ids: list[str] | None = None) -> dict[str, Any]:
    return {"code": code, "message": message, "scene_ids": scene_ids or []}


def _contains_financial_number(scene: dict[str, Any]) -> bool:
    """Detect a numerical finance claim without treating any number as a fact."""

    fields = {
        key: scene.get(key)
        for key in (
            "description", "information_role", "stat", "primaryValue",
            "supportingMetrics", "chartData", "metrics", "value",
        )
        if scene.get(key) is not None
    }
    return bool(FINANCIAL_NUMBER_RE.search(json.dumps(fields, ensure_ascii=False)))


def _requires_source_anchor(scene: dict[str, Any], scene_type: str) -> bool:
    claim_class = str(scene.get("claim_class", "")).strip().upper()
    if claim_class:
        return claim_class == "FACT"
    if scene_type in FACTUAL_TYPES:
        return True
    return scene_type in LEGACY_FINANCIAL_DATA_TYPES and _contains_financial_number(scene)


def _editorial_warnings(
    scene_plan: dict[str, Any],
    scenes: list[dict[str, Any]],
    scene_types: list[str],
) -> tuple[list[dict[str, Any]], str | None]:
    """Return mode-aware advisory warnings without overriding creative choice."""

    raw_direction = extract_editorial_direction(scene_plan)
    if raw_direction is None:
        return [], None
    try:
        direction = normalize_editorial_direction(raw_direction)
    except ValueError as exc:
        return [_warn("EDITORIAL_DIRECTION_INVALID", str(exc))], None

    mode = direction["primary_mode"]
    warnings: list[dict[str, Any]] = []
    justified = any(scene.get("finance_justification") for scene in scenes)
    type_counts = Counter(scene_types)
    mechanism_count = sum(type_counts[item] for item in MECHANISM_TYPES)

    if mode == "FLOW" and mechanism_count == 0 and not justified:
        warnings.append(
            _warn(
                "MODE_VISUAL_MISMATCH",
                "FLOW is the primary editorial mode, but the plan has no money_flow or causal_chain treatment for its central allocation/value-capture question.",
            )
        )
    direction_text = " ".join(
        [str(direction.get("audience_task", ""))]
        + [str(item) for item in direction.get("rationale", [])]
    ).lower()
    directional_task = any(term in direction_text for term in TRANSMISSION_TERMS)

    if mode == "MACRO" and directional_task and mechanism_count == 0 and not justified:
        warnings.append(
            _warn(
                "MODE_VISUAL_MISMATCH",
                "MACRO is the primary editorial mode, but the plan has no mechanism visual for transmission or conditional second-order effects.",
            )
        )
    elif mode == "EXPLAIN" and mechanism_count == 0 and direction["audience_task"] == "understand_mechanism" and not justified:
        warnings.append(
            _warn(
                "MODE_VISUAL_MISMATCH",
                "EXPLAIN asks the viewer to understand a mechanism, but the plan has no causal_chain or money_flow treatment.",
            )
        )

    document_like = sum(type_counts[item] for item in ("document", "evidence_card"))
    market_language = sum(type_counts[item] for item in ("research_timeline", "chart", "causal_chain"))
    if mode == "MARKET" and len(scenes) >= 5 and document_like / len(scenes) > 0.5 and market_language == 0 and not justified:
        warnings.append(
            _warn(
                "EDITORIAL_GRAMMAR_MISMATCH",
                "The MARKET plan is dominated by filing/evidence-card pacing without a timing, move, or transmission treatment.",
            )
        )

    explain_complexity = sum(type_counts[item] for item in ("document", "scenario_board", "thesis_breaker"))
    if mode == "EXPLAIN" and len(scenes) >= 5 and explain_complexity / len(scenes) > 0.5 and not justified:
        warnings.append(
            _warn(
                "EDITORIAL_GRAMMAR_MISMATCH",
                "The EXPLAIN plan is dominated by document/decision treatments; verify that institutional complexity helps the concept rather than styling it as research.",
            )
        )

    evidence_ids = [
        str(scene.get("id", ""))
        for scene in scenes
        if _finance_type(scene) == "evidence_card"
    ]
    if mode == "RESEARCH" and len(evidence_ids) >= 3 and len(evidence_ids) / len(scenes) > 0.5 and not justified:
        warnings.append(
            _warn(
                "MODE_COMPONENT_OVERUSE",
                "RESEARCH is dominated by EvidenceCard; use documents, charts, mechanisms, or decision treatments where they better express the evidence.",
                evidence_ids,
            )
        )

    unsupported_causal_ids = [
        str(scene.get("id", ""))
        for scene in scenes
        if _finance_type(scene) == "causal_chain"
        and not scene.get("mechanism_importance")
        and not scene.get("finance_justification")
    ]
    if unsupported_causal_ids:
        warnings.append(
            _warn(
                "MODE_COMPONENT_OVERUSE",
                "CausalChain appears without an explicit directional mechanism need; verify that chronology, comparison, flow, evidence, chart, scenario, or a simpler diagram would not fit better.",
                unsupported_causal_ids,
            )
        )

    return warnings, mode


class FinanceSceneVarietyValidator:
    """Return deterministic warnings for a scene list or scene_plan artifact."""

    def validate(self, scene_plan: dict[str, Any] | list[dict[str, Any]]) -> dict[str, Any]:
        scenes = scene_plan if isinstance(scene_plan, list) else scene_plan.get("scenes", [])
        warnings: list[dict[str, Any]] = []
        if not scenes:
            return {"valid": True, "warnings": [], "summary": {"scene_count": 0}}

        scene_types = [_finance_type(scene) for scene in scenes]
        type_counts = Counter(scene_types)
        most_common_type, most_common_count = type_counts.most_common(1)[0]

        if len(scenes) >= 4 and most_common_count / len(scenes) > 0.5:
            warnings.append(
                _warn(
                    "VISUAL_MONOTONY_RISK",
                    f"{most_common_type} appears in {most_common_count}/{len(scenes)} scenes; verify that the repeated treatment is justified by the evidence structure.",
                    [str(s.get("id", "")) for s in scenes if _finance_type(s) == most_common_type],
                )
            )

        card_ids = [str(scene.get("id", "")) for scene in scenes if _finance_type(scene) in CARD_LIKE_TYPES]
        if card_ids and len(card_ids) / len(scenes) > 0.4:
            warnings.append(
                _warn(
                    "CARD_OVERUSE",
                    f"Card-like scenes account for {len(card_ids)}/{len(scenes)} scenes ({len(card_ids) / len(scenes):.0%}), above the 40% review threshold.",
                    card_ids,
                )
            )

        for previous, current in zip(scenes, scenes[1:]):
            repeated_type = _finance_type(previous)
            if (
                repeated_type in FINANCE_TYPES
                and repeated_type == _finance_type(current)
                and not previous.get("finance_justification")
                and not current.get("finance_justification")
            ):
                warnings.append(
                    _warn(
                        "REPEATED_SCENE_TYPE",
                        f"Consecutive scenes repeat {repeated_type} without an explicit finance_justification.",
                        [str(previous.get("id", "")), str(current.get("id", ""))],
                    )
                )

        duration = max((float(scene.get("end_seconds", 0) or 0) for scene in scenes), default=0.0)
        families = {family for scene in scenes if (family := _family(scene))}
        if duration >= 45 and len(families) < 3:
            warnings.append(
                _warn(
                    "LOW_VISUAL_FAMILY_DIVERSITY",
                    f"A {duration:g}s plan uses {len(families)} finance visual families ({', '.join(sorted(families)) or 'none'}); prefer three when the topic supports them.",
                )
            )

        mechanism_needed = any(bool(scene.get("mechanism_importance")) for scene in scenes)
        if mechanism_needed and not any(scene_type in MECHANISM_TYPES for scene_type in scene_types):
            warnings.append(
                _warn(
                    "NO_MECHANISM_VISUAL",
                    "The plan contains an important mechanism explanation but no money_flow or causal_chain scene.",
                )
            )

        missing_source_ids: list[str] = []
        for scene in scenes:
            scene_type = _finance_type(scene)
            important_fact = _requires_source_anchor(scene, scene_type)
            if important_fact and not scene.get("source_anchor") and not scene.get("finance_justification"):
                missing_source_ids.append(str(scene.get("id", "")))
        if missing_source_ids:
            warnings.append(
                _warn(
                    "MISSING_SOURCE_ANCHOR",
                    "Important factual/data scenes are missing readable source_anchor context.",
                    missing_source_ids,
                )
            )

        editorial_mode = None
        if isinstance(scene_plan, dict):
            mode_warnings, editorial_mode = _editorial_warnings(scene_plan, scenes, scene_types)
            warnings.extend(mode_warnings)

        return {
            "valid": True,
            "warnings": warnings,
            "summary": {
                "scene_count": len(scenes),
                "duration_seconds": duration,
                "families": sorted(families),
                "type_counts": dict(sorted(type_counts.items())),
                "editorial_mode": editorial_mode,
            },
        }


def validate_finance_scene_variety(
    scene_plan: dict[str, Any] | list[dict[str, Any]],
) -> dict[str, Any]:
    """Functional entry point for directors and tests."""

    return FinanceSceneVarietyValidator().validate(scene_plan)


def validate_finance_mode_signatures(
    plans: dict[str, dict[str, Any]] | list[dict[str, Any]],
) -> dict[str, Any]:
    """Review a current fixture/project plan set for compound template signals.

    This is deliberately local and advisory. Equal scene counts alone never
    trigger a warning; the count must coincide with another repeated structural
    signature such as universal CausalChain or universal standalone disclaimers.
    """

    items = list(plans.values()) if isinstance(plans, dict) else list(plans)
    if len(items) < 3:
        return {"valid": True, "warnings": [], "summary": {"plan_count": len(items)}}

    scene_lists = [item.get("scenes", []) for item in items]
    counts = [len(scenes) for scenes in scene_lists]
    signatures = [tuple(_finance_type(scene) for scene in scenes) for scenes in scene_lists]
    same_count = len(set(counts)) == 1
    same_sequence = len(set(signatures)) == 1
    causal_in_every_plan = all(
        any(_finance_type(scene) == "causal_chain" for scene in scenes)
        for scenes in scene_lists
    )
    standalone_in_every_plan = all(
        bool(scenes)
        and _finance_type(scenes[-1]) == "text_card"
        and "不构成" in str(scenes[-1].get("description", ""))
        for scenes in scene_lists
    )

    warnings: list[dict[str, Any]] = []
    if same_sequence or (
        same_count and (causal_in_every_plan or standalone_in_every_plan)
    ):
        repeated = []
        if same_count:
            repeated.append(f"the same {counts[0]}-scene count")
        if same_sequence:
            repeated.append("the same component sequence")
        if causal_in_every_plan:
            repeated.append("CausalChain in every plan")
        if standalone_in_every_plan:
            repeated.append("a standalone disclaimer in every plan")
        warnings.append(
            _warn(
                "MODE_SIGNATURE_TOO_REGULAR",
                "Representative editorial modes share compound template signals: "
                + ", ".join(repeated)
                + ". Re-check scene boundaries against each audience_task; do not vary them randomly.",
            )
        )

    return {
        "valid": True,
        "warnings": warnings,
        "summary": {
            "plan_count": len(items),
            "scene_counts": counts,
            "same_scene_count": same_count,
            "same_component_sequence": same_sequence,
            "causal_chain_in_every_plan": causal_in_every_plan,
            "standalone_disclaimer_in_every_plan": standalone_in_every_plan,
        },
    }
