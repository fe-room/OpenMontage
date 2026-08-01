"""Enforce semantic motion coverage planning for generated explainers.

Capability discovery alone is insufficient: an agent can see available stock
and generated-video providers, decide they are not core dependencies, and then
silently omit footage that would add meaning to selected beats. These tests keep
the beat-classification, three-path comparison, decision log, and reviewer
enforcement discoverable to fresh-session agents.
"""

from __future__ import annotations

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent.parent


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_agent_guide_carries_semantic_motion_hard_rule():
    guide = _read("AGENT_GUIDE.md")
    assert "Semantic Motion Coverage Audit (HARD RULE)" in guide
    assert "Precision-critical" in guide
    assert "Semantic-motion candidate" in guide
    assert "Decorative-only" in guide
    assert "Composition-only" in guide
    assert "Light hybrid" in guide
    assert "Footage-led" in guide
    assert 'subject: "Visual coverage strategy"' in guide


def test_explainer_proposal_director_requires_beat_classification_and_three_paths():
    body = _read("skills/pipelines/explainer/proposal-director.md")
    for token in (
        "precision_critical",
        "semantic_motion_candidate",
        "decorative_only",
        "Composition-only",
        "Light hybrid",
        "Footage-led",
        "motion_commitment",
        "Visual coverage strategy",
    ):
        assert token in body
    assert "not a core dependency" in body


def test_reviewer_treats_silent_footage_omission_as_critical():
    body = _read("skills/meta/reviewer.md")
    assert "Semantic Motion Coverage Review" in body
    assert "Capability discovery is not coverage planning" in body
    assert "Optional to delivery does not mean useless to presentation" in body
    assert "No `motion_commitment` / `Visual coverage strategy` decision is logged" in body
    assert body.count("**CRITICAL**") >= 1


def test_animated_explainer_manifest_reviews_visual_coverage_strategy():
    manifest = yaml.safe_load(_read("pipeline_defs/animated-explainer.yaml"))
    proposal = next(stage for stage in manifest["stages"] if stage["name"] == "proposal")
    review_text = "\n".join(proposal["review_focus"])
    assert "Semantic motion coverage audit" in review_text
    assert "composition-only, light-hybrid, and footage-led" in review_text
    assert "motion_commitment" in review_text
    assert "not a core dependency" in review_text
