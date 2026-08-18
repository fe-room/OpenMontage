"""Deterministic contracts for the finance-to-WeChat editorial branch.

Creative judgment remains in the pipeline skills.  This module only enforces
rules that are mechanical enough to fail closed: the four-question score,
score bands, low-score upgrade requirements, word-count tiers, and the exact
article disclaimer carried into the hand-off package.
"""

from __future__ import annotations

from typing import Any, Mapping


WECHAT_FINANCE_DISCLAIMER = (
    "本文用于财经知识和数据研究记录，不构成对具体证券的买卖建议。"
)

SCREENING_DIMENSIONS = (
    "evergreen_value",
    "unfinished_depth",
    "evidence_value",
    "series_fit",
)

ARTICLE_TIER_WORD_RANGES = {
    "A_core_research": (1500, 5000),
    "B_knowledge_extension": (800, 1800),
    "C_experiment_log": (500, 1200),
}


def validate_screening_semantics(data: Mapping[str, Any]) -> None:
    """Validate cross-field screening rules that JSON Schema cannot express."""
    factors = data.get("factors")
    if not isinstance(factors, Mapping):
        raise ValueError("wechat_content_screen.factors must be an object")

    scores: list[int] = []
    for name in SCREENING_DIMENSIONS:
        factor = factors.get(name)
        if not isinstance(factor, Mapping):
            raise ValueError(f"Missing screening factor: {name}")
        answer = factor.get("answer")
        score = factor.get("score")
        expected = 1 if answer is True else 0
        if answer not in (True, False) or score != expected:
            raise ValueError(
                f"Screening factor {name!r} must score 1 for yes and 0 for no"
            )
        scores.append(score)

    total = sum(scores)
    if data.get("total_score") != total:
        raise ValueError(
            f"wechat_content_screen.total_score must equal factor sum {total}"
        )

    expected_band = (
        "strongly_recommended" if total >= 3
        else "recommended" if total == 2
        else "not_recommended"
    )
    if data.get("selection_band") != expected_band:
        raise ValueError(
            f"Score {total} requires selection_band={expected_band!r}"
        )

    action = data.get("approved_action")
    upgrade = data.get("upgrade_path") or {}
    if total <= 1 and action == "write":
        raise ValueError(
            "A 0-1 score cannot go straight to writing; skip it or upgrade the topic first"
        )
    if action == "upgrade_then_write":
        if not upgrade.get("can_upgrade") or not str(
            upgrade.get("upgraded_question", "")
        ).strip():
            raise ValueError(
                "upgrade_then_write requires can_upgrade=true and an upgraded_question"
            )


def validate_article_tier(data: Mapping[str, Any]) -> None:
    """Keep the chosen article tier and target length aligned."""
    tier = data.get("article_tier")
    if tier not in ARTICLE_TIER_WORD_RANGES:
        return
    minimum, maximum = ARTICLE_TIER_WORD_RANGES[tier]
    target = data.get("target_word_count")
    if not isinstance(target, int) or not minimum <= target <= maximum:
        raise ValueError(
            f"{tier} target_word_count must be between {minimum} and {maximum}"
        )


def validate_exact_disclaimer(data: Mapping[str, Any]) -> None:
    """Require the exact finance article disclaimer in drafts and packages."""
    value = data.get("disclaimer")
    if value != WECHAT_FINANCE_DISCLAIMER:
        raise ValueError(
            "Finance WeChat disclaimer must be exact: "
            f"{WECHAT_FINANCE_DISCLAIMER}"
        )


def validate_wechat_artifact(name: str, data: Mapping[str, Any]) -> None:
    """Dispatch deterministic semantic checks for registered artifacts."""
    if name == "wechat_content_screen":
        validate_screening_semantics(data)
    elif name == "wechat_article_draft":
        validate_article_tier(data)
        validate_exact_disclaimer(data)
    elif name == "wechat_article_package":
        validate_exact_disclaimer(data)
