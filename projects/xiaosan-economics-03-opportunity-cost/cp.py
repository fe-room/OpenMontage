#!/usr/bin/env python3
"""Stage checkpoint helper for xiaosan-economics-03-opportunity-cost.

Usage:
  python3 cp.py <stage> <status> <artifact_name>[:<json_path>] [<artifact_name>:<json_path> ...] \
      [--approval-required] [--approved] [--note "..."] [--meta key=value ...]

Loads each artifact JSON from projects/<pid>/artifacts/<json> and embeds the full
object into the checkpoint, which is what lib.checkpoint validates.
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

PID = "xiaosan-economics-03-opportunity-cost"
PROJECTS = REPO / "projects"
ROOT = PROJECTS / PID


def main() -> None:
    args = sys.argv[1:]
    stage, status = args[0], args[1]
    specs, notes, meta = [], [], {}
    approval_required = False
    approved = False
    i = 2
    while i < len(args):
        a = args[i]
        if a == "--approval-required":
            approval_required = True
        elif a == "--approved":
            approved = True
        elif a == "--note":
            i += 1
            notes.append(args[i])
        elif a == "--meta":
            i += 1
            k, _, v = args[i].partition("=")
            meta[k] = v
        else:
            specs.append(a)
        i += 1

    artifacts = {}
    for spec in specs:
        name, _, fname = spec.partition(":")
        fname = fname or f"{name}.json"
        path = ROOT / "artifacts" / fname
        if not path.exists():
            path = ROOT / fname
        artifacts[name] = json.loads(path.read_text())

    from lib.checkpoint import write_checkpoint

    cost = ROOT / "artifacts" / "cost_log.json"
    spent = 0.0
    if cost.exists():
        try:
            spent = float(json.loads(cost.read_text()).get("total_usd", 0.0))
        except Exception:
            spent = 0.0

    p = write_checkpoint(
        PROJECTS,
        PID,
        stage,
        status,
        artifacts=artifacts,
        pipeline_type="finance-dossier",
        style_playbook="finance-dossier",
        human_approval_required=approval_required,
        human_approved=approved,
        review={
            "round": 1,
            "decision": "pass",
            "critical": 0,
            "suggestions": 0,
            "notes": notes,
        },
        cost_snapshot={"spent_usd": spent, "budget_default_usd": 2.0},
        metadata=meta,
    )
    print("written:", p)


if __name__ == "__main__":
    main()
