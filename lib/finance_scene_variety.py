"""Deterministic warning-only validation for finance-dossier scene plans.

The generic variation checker evaluates cinematography. This module evaluates the
finance scene grammar: evidence anchors, conceptual families, mechanism coverage,
and component repetition. It never hard-fails a production; directors review the
warnings and may record a deliberate justification for a simple plan.
"""

from __future__ import annotations

from collections import Counter
from typing import Any


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
MECHANISM_TERMS = {
    "because",
    "causes",
    "causal",
    "mechanism",
    "drives",
    "leads to",
    "flows to",
    "transmission",
    "因果",
    "机制",
    "导致",
    "传导",
    "流向",
}


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
        if not mechanism_needed:
            combined_text = " ".join(
                f"{scene.get('description', '')} {scene.get('information_role', '')}".lower()
                for scene in scenes
            )
            mechanism_needed = any(term in combined_text for term in MECHANISM_TERMS)
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
            important_fact = scene.get("claim_class") == "FACT" or scene_type in FACTUAL_TYPES
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

        return {
            "valid": True,
            "warnings": warnings,
            "summary": {
                "scene_count": len(scenes),
                "duration_seconds": duration,
                "families": sorted(families),
                "type_counts": dict(sorted(type_counts.items())),
            },
        }


def validate_finance_scene_variety(
    scene_plan: dict[str, Any] | list[dict[str, Any]],
) -> dict[str, Any]:
    """Functional entry point for directors and tests."""

    return FinanceSceneVarietyValidator().validate(scene_plan)
