"""Contracts and profiles for Finance Dossier editorial direction.

OpenMontage keeps creative judgment in director instructions. This module does
not classify a topic by keywords or choose a scene sequence; it validates and
normalizes the small strategy object that the Editorial Router writes into the
metadata of existing canonical artifacts.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


EDITORIAL_MODES = ("RESEARCH", "MARKET", "MACRO", "FLOW", "EXPLAIN")
CLASSIFICATION_CONFIDENCE = ("high", "medium", "low")
CANVAS_MODES = ("paper", "document", "data", "margin-note", "dark-ink", "full-bleed")
DENSITY_LEVELS = ("sparse", "standard", "dense")


MODE_PROFILES: dict[str, dict[str, Any]] = {
    "RESEARCH": {
        "primary_question": "What is happening inside the company, and what is the market pricing?",
        "grammar": ["ANOMALY", "EVIDENCE", "EXPECTATION", "MECHANISM", "IMPLICATION", "THESIS_CHANGE"],
        "evidence_priority": ["company_filings", "investor_relations", "financial_statements", "market_expectations"],
        "visual_priority": ["document", "evidence_card", "expectation_gap", "chart", "causal_chain", "thesis_breaker"],
        "canvas_preference": ["paper", "document", "margin-note", "data"],
        "key_anti_pattern": "Do not turn every data point into an EvidenceCard or force a deterministic stock call.",
    },
    "MARKET": {
        "primary_question": "What moved, when, what triggered it, and what transmission matters next?",
        "grammar": ["WHAT_MOVED", "WHEN", "TRIGGER", "TRANSMISSION", "WHAT_NEXT"],
        "evidence_priority": ["timestamped_market_data", "official_announcements", "event_timeline", "reaction_window"],
        "visual_priority": ["research_timeline", "chart", "causal_chain", "document"],
        "canvas_preference": ["data", "full-bleed", "dark-ink", "paper"],
        "key_anti_pattern": "Do not use slow filing-page pacing or claim a single cause when alternatives remain plausible.",
    },
    "MACRO": {
        "primary_question": "How does one macro variable transmit through the system into another variable or asset?",
        "grammar": ["VARIABLE", "TRANSMISSION", "SECOND_ORDER_EFFECT", "IMPACT", "CHAIN_BREAKER"],
        "evidence_priority": ["central_banks", "official_statistics", "rates_data", "policy_documents"],
        "visual_priority": ["causal_chain", "research_timeline", "chart", "document", "scenario_board"],
        "canvas_preference": ["data", "document", "full-bleed", "margin-note"],
        "key_anti_pattern": "Do not make conditional or contested transmission look deterministic through simple arrows.",
    },
    "FLOW": {
        "primary_question": "Where does money or value flow, who captures it, and where is the bottleneck?",
        "grammar": ["SOURCE", "ALLOCATION", "VALUE_CAPTURE", "BOTTLENECK", "IMPLICATION"],
        "evidence_priority": ["segment_disclosures", "cost_structures", "industry_research", "value_chain_data"],
        "visual_priority": ["money_flow", "causal_chain", "evidence_card", "chart"],
        "canvas_preference": ["data", "full-bleed", "margin-note"],
        "key_anti_pattern": "Do not use Sankey for non-additive metrics, unrelated numbers, or decorative complexity.",
    },
    "EXPLAIN": {
        "primary_question": "What is the mechanism, and what single example makes it understandable?",
        "grammar": ["QUESTION", "MECHANISM", "EXAMPLE", "MISUNDERSTANDING", "TAKEAWAY"],
        "evidence_priority": ["authoritative_conceptual_sources", "stable_definitions", "worked_example"],
        "visual_priority": ["causal_chain", "chart", "money_flow", "evidence_card"],
        "canvas_preference": ["paper", "data", "margin-note"],
        "key_anti_pattern": "Do not add institutional-research complexity merely to appear professional.",
    },
}


REQUIRED_DIRECTION_FIELDS = {
    "primary_mode",
    "audience_task",
    "rationale",
    "evidence_priority",
    "visual_priority",
    "canvas_preference",
    "density_profile",
    "hook_grammar",
    "ending_grammar",
    "key_editorial_risk",
    "key_anti_pattern",
    "classification_confidence",
}


def mode_profile(mode: str) -> dict[str, Any]:
    """Return a copy of the editorial prior for one supported mode."""

    normalized = str(mode).strip().upper()
    if normalized not in MODE_PROFILES:
        raise ValueError(f"Unsupported Finance Dossier editorial mode: {mode!r}")
    return deepcopy(MODE_PROFILES[normalized])


def extract_editorial_direction(artifact: Mapping[str, Any]) -> dict[str, Any] | None:
    """Read the additive contract from a canonical artifact or its metadata."""

    direct = artifact.get("editorial_direction")
    if isinstance(direct, Mapping):
        return dict(direct)
    metadata = artifact.get("metadata")
    if isinstance(metadata, Mapping):
        nested = metadata.get("editorial_direction")
        if isinstance(nested, Mapping):
            return dict(nested)
    return None


def normalize_editorial_direction(direction: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and normalize an instruction-produced Editorial Direction.

    The contract intentionally contains strategy, not exact scene order, layout,
    timing, animation, or scene count.
    """

    missing = sorted(REQUIRED_DIRECTION_FIELDS - set(direction))
    if missing:
        raise ValueError(f"Editorial Direction is missing required fields: {', '.join(missing)}")

    normalized = deepcopy(dict(direction))
    primary = str(normalized["primary_mode"]).strip().upper()
    if primary not in EDITORIAL_MODES:
        raise ValueError(f"Unsupported primary_mode: {primary!r}")
    normalized["primary_mode"] = primary

    secondary_value = normalized.get("secondary_mode")
    if secondary_value in (None, ""):
        normalized.pop("secondary_mode", None)
    else:
        secondary = str(secondary_value).strip().upper()
        if secondary not in EDITORIAL_MODES:
            raise ValueError(f"Unsupported secondary_mode: {secondary!r}")
        if secondary == primary:
            raise ValueError("secondary_mode must differ from primary_mode")
        normalized["secondary_mode"] = secondary

    confidence = str(normalized["classification_confidence"]).strip().lower()
    if confidence not in CLASSIFICATION_CONFIDENCE:
        raise ValueError("classification_confidence must be high, medium, or low")
    normalized["classification_confidence"] = confidence

    for field in ("rationale", "evidence_priority", "visual_priority", "canvas_preference"):
        value = normalized[field]
        if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
            raise ValueError(f"{field} must be a non-empty list of strings")

    invalid_canvas = sorted(set(normalized["canvas_preference"]) - set(CANVAS_MODES))
    if invalid_canvas:
        raise ValueError(f"Unsupported canvas_preference values: {', '.join(invalid_canvas)}")

    density = normalized["density_profile"]
    if not isinstance(density, Mapping):
        raise ValueError("density_profile must be an object")
    required_density = {"opening", "body", "evidence", "ending"}
    if set(density) != required_density:
        raise ValueError("density_profile must contain exactly opening, body, evidence, and ending")
    for phase, level in density.items():
        if level not in DENSITY_LEVELS:
            raise ValueError(f"Unsupported density level for {phase}: {level!r}")

    forbidden_execution_fields = {
        "scene_order", "scene_count", "scene_layouts", "layout_variant",
        "animation", "coordinates", "x", "y",
    }
    leaked = sorted(forbidden_execution_fields & set(normalized))
    if leaked:
        raise ValueError(f"Editorial Direction must not decide scene execution fields: {', '.join(leaked)}")

    allowed_fields = REQUIRED_DIRECTION_FIELDS | {"secondary_mode"}
    unsupported = sorted(set(normalized) - allowed_fields)
    if unsupported:
        raise ValueError(f"Unsupported Editorial Direction fields: {', '.join(unsupported)}")

    for field in (
        "audience_task", "hook_grammar", "ending_grammar",
        "key_editorial_risk", "key_anti_pattern",
    ):
        if not isinstance(normalized[field], str) or not normalized[field].strip():
            raise ValueError(f"{field} must be a non-empty string")

    return normalized
