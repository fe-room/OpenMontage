"""Cross-stage editorial policies that must fail closed.

Creative classification remains an agent decision. Once a production is marked
as financial, however, the required disclaimer is enforced here so a later
stage cannot accidentally omit it.
"""

from __future__ import annotations

from typing import Any, Mapping


FINANCIAL_DISCLAIMER_ZH = (
    "本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。"
)

_FINANCIAL_CATEGORIES = {"finance", "financial", "金融", "财经", "投资"}


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


def enforce_financial_disclaimer(stage: str, artifacts: Mapping[str, Any]) -> None:
    """Enforce the financial end-card contract at every downstream boundary."""
    if not is_financial_production(artifacts):
        return

    if stage == "script":
        sections = artifacts.get("script", {}).get("sections", [])
        if not sections or not _contains_exact_disclaimer(sections[-1].get("text")):
            raise ContentPolicyError(
                "Financial video policy: the final script section must contain the exact "
                f"disclaimer: {FINANCIAL_DISCLAIMER_ZH}"
            )

    elif stage == "scene_plan":
        scenes = artifacts.get("scene_plan", {}).get("scenes", [])
        final = scenes[-1] if scenes else {}
        if final.get("type") != "text_card" or not _contains_exact_disclaimer(
            final.get("description")
        ):
            raise ContentPolicyError(
                "Financial video policy: the final scene must be a text_card whose "
                f"description contains the exact disclaimer: {FINANCIAL_DISCLAIMER_ZH}"
            )

    elif stage == "edit":
        cuts = artifacts.get("edit_decisions", {}).get("cuts", [])
        final = cuts[-1] if cuts else {}
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
