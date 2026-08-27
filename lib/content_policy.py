"""Cross-stage editorial policies that must fail closed.

Creative classification remains an agent decision. Once a production is marked
as financial, however, the exact disclaimer is enforced here so a later stage
cannot accidentally omit it. Finance Dossier may carry the text as native
footer/overlay metadata on its editorial ending; legacy and explicitly required
standalone end cards remain supported.
"""

from __future__ import annotations

from typing import Any, Mapping


FINANCIAL_DISCLAIMER_ZH = (
    "本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。"
)

_FINANCIAL_CATEGORIES = {"finance", "financial", "金融", "财经", "投资"}
_EMBEDDED_PRESENTATIONS = {"footer", "overlay"}
_PRESENTATIONS = _EMBEDDED_PRESENTATIONS | {"standalone"}


class ContentPolicyError(ValueError):
    """Raised when a mandatory editorial policy is violated."""


def _category_from(value: Any) -> str | None:
    if not isinstance(value, Mapping):
        return None
    direct = value.get("content_category")
    if isinstance(direct, str):
        return direct.strip().lower()
    metadata = value.get("metadata")
    if isinstance(metadata, Mapping):
        nested = metadata.get("content_category")
        if isinstance(nested, str):
            return nested.strip().lower()
    return None


def is_financial_production(artifacts: Mapping[str, Any]) -> bool:
    """Return whether any canonical upstream artifact marks the video financial."""
    for name in ("brief", "research_brief", "proposal_packet"):
        category = _category_from(artifacts.get(name))
        if category in _FINANCIAL_CATEGORIES:
            return True
    return False


def _contains_exact_disclaimer(value: Any) -> bool:
    return isinstance(value, str) and FINANCIAL_DISCLAIMER_ZH in value


def _compliance_contract(artifact: Any) -> Mapping[str, Any] | None:
    if not isinstance(artifact, Mapping):
        return None
    metadata = artifact.get("metadata")
    if not isinstance(metadata, Mapping):
        return None
    compliance = metadata.get("compliance")
    return compliance if isinstance(compliance, Mapping) else None


def _validate_compliance_contract(
    stage: str,
    artifact: Mapping[str, Any],
    items_key: str,
    ending_id_key: str,
) -> str | None:
    """Validate an opt-in native compliance presentation and return its mode."""

    compliance = _compliance_contract(artifact)
    if compliance is None:
        return None
    presentation = compliance.get("presentation")
    if presentation not in _PRESENTATIONS:
        raise ContentPolicyError(
            f"Financial video policy: {stage} compliance presentation must be "
            "footer, overlay, or standalone."
        )
    if compliance.get("financial_disclaimer") != FINANCIAL_DISCLAIMER_ZH:
        raise ContentPolicyError(
            "Financial video policy: compliance metadata must preserve the exact "
            f"disclaimer: {FINANCIAL_DISCLAIMER_ZH}"
        )
    if compliance.get("placement") != "ending":
        raise ContentPolicyError(
            "Financial video policy: compliance metadata must use placement='ending'."
        )
    if presentation in _EMBEDDED_PRESENTATIONS:
        items = artifact.get(items_key, [])
        final = items[-1] if isinstance(items, list) and items else {}
        if not isinstance(final, Mapping) or compliance.get(ending_id_key) != final.get("id"):
            raise ContentPolicyError(
                f"Financial video policy: {ending_id_key} must identify the final "
                "meaningful editorial item that carries the native compliance line."
            )
    return str(presentation)


def enforce_financial_disclaimer(stage: str, artifacts: Mapping[str, Any]) -> None:
    """Enforce exact financial compliance without prescribing one ending shape."""
    if not is_financial_production(artifacts):
        return

    if stage == "script":
        script = artifacts.get("script", {})
        presentation = _validate_compliance_contract(
            "script", script, "sections", "ending_section_id"
        )
        sections = script.get("sections", [])
        if presentation in _EMBEDDED_PRESENTATIONS:
            return
        if not sections or not _contains_exact_disclaimer(sections[-1].get("text")):
            raise ContentPolicyError(
                "Financial video policy: the final script section must contain the exact "
                f"disclaimer: {FINANCIAL_DISCLAIMER_ZH}"
            )

    elif stage == "scene_plan":
        scene_plan = artifacts.get("scene_plan", {})
        presentation = _validate_compliance_contract(
            "scene_plan", scene_plan, "scenes", "ending_scene_id"
        )
        scenes = scene_plan.get("scenes", [])
        final = scenes[-1] if scenes else {}
        if presentation in _EMBEDDED_PRESENTATIONS:
            return
        if final.get("type") != "text_card" or not _contains_exact_disclaimer(
            final.get("description")
        ):
            raise ContentPolicyError(
                "Financial video policy: the final scene must be a text_card whose "
                f"description contains the exact disclaimer: {FINANCIAL_DISCLAIMER_ZH}"
            )

    elif stage == "edit":
        edit_decisions = artifacts.get("edit_decisions", {})
        presentation = _validate_compliance_contract(
            "edit", edit_decisions, "cuts", "ending_cut_id"
        )
        cuts = edit_decisions.get("cuts", [])
        final = cuts[-1] if cuts else {}
        if presentation in _EMBEDDED_PRESENTATIONS:
            return
        exact_text = any(
            _contains_exact_disclaimer(final.get(field))
            for field in ("text", "title", "subtitle")
        )
        if final.get("type") != "text_card" or not exact_text:
            raise ContentPolicyError(
                "Financial video policy: the final edit cut must be a text_card with "
                f"the exact disclaimer text: {FINANCIAL_DISCLAIMER_ZH}"
            )

    elif stage == "compose":
        edit_presentation = None
        edit_contract = _compliance_contract(artifacts.get("edit_decisions", {}))
        if edit_contract is not None:
            edit_presentation = edit_contract.get("presentation")
        compliance = (
            artifacts.get("final_review", {})
            .get("checks", {})
            .get("compliance", {})
        )
        if not (
            compliance.get("financial_disclaimer_present") is True
            and compliance.get("financial_disclaimer_exact") is True
            and compliance.get("financial_disclaimer_readable") is True
            and compliance.get("financial_disclaimer_at_end") is True
        ):
            raise ContentPolicyError(
                "Financial video policy: final_review must confirm the disclaimer is "
                "present, exact, readable, and shown at the end of the rendered video."
            )
        if edit_presentation in _EMBEDDED_PRESENTATIONS and compliance.get(
            "financial_disclaimer_presentation"
        ) != edit_presentation:
            raise ContentPolicyError(
                "Financial video policy: final_review must confirm the approved "
                f"{edit_presentation} compliance presentation on the editorial ending."
            )
