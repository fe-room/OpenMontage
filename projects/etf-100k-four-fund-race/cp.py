"""Write pipeline checkpoints for etf-100k-four-fund-race.

Usage:
    python cp.py <stage> <status> [--approved]

Artifacts are always passed as the FULL canonical artifact objects (never
paths) — passing a path raises "Artifact 'x' must be a JSON object matching
its schema".
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
REPO = PROJECT.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from lib.checkpoint import write_checkpoint  # noqa: E402

PIPELINE_DIR = REPO / "projects"
PROJECT_ID = PROJECT.name
ARTIFACTS_DIR = PROJECT / "artifacts"

STAGE_ARTIFACTS = {
    "research": ["research_brief"],
    "proposal": ["proposal_packet", "decision_log"],
    "script": ["script"],
    "scene_plan": ["scene_plan"],
    "assets": ["asset_manifest"],
    "edit": ["edit_decisions"],
    "compose": ["render_report", "final_review"],
    "cover": ["cover_package"],
    "publish": ["publish_log"],
}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("stage")
    ap.add_argument("status", choices=["in_progress", "completed", "awaiting_human", "failed"])
    ap.add_argument("--approved", action="store_true")
    ap.add_argument("--note")
    args = ap.parse_args()

    names = STAGE_ARTIFACTS[args.stage]
    artifacts = {}
    for name in names:
        p = ARTIFACTS_DIR / f"{name}.json"
        if not p.exists():
            if args.status == "in_progress":
                continue
            raise SystemExit(f"missing artifact for stage {args.stage}: {p}")
        artifacts[name] = json.loads(p.read_text())

    out = write_checkpoint(
        PIPELINE_DIR,
        PROJECT_ID,
        args.stage,
        args.status,
        artifacts,
        pipeline_type="finance-dossier",
        human_approved=args.approved,
        metadata={"note": args.note} if args.note else None,
    )
    rel = out.relative_to(REPO)
    print(f"[checkpoint] {rel}  status={args.status} approved={args.approved} artifacts={list(artifacts)}")


if __name__ == "__main__":
    main()
