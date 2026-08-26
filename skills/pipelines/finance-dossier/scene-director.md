# Finance Dossier — Scene Director

Produce the existing `scene_plan`. For each scene, use additive finance fields (`finance_scene_type`, `finance_family`, `claim_class`, `source_anchor`, `mechanism_importance`, `layout_variant`, and `finance_justification`) only where applicable.

## Planning

1. Assign each beat to `DOCUMENT`, `DATA`, `MECHANISM`, or `DECISION` by information responsibility.
2. Choose scene type and deterministic layout variant from the information structure:
   - DOCUMENT: document crop or `research_timeline`.
   - DATA: chart, `evidence_card`, or `expectation_gap`.
   - MECHANISM: `money_flow` or `causal_chain`.
   - DECISION: `scenario_board`, `thesis_breaker`, or watch list.
3. Give every major FACT/data scene a readable `source_anchor` with source label/date and period when relevant.
4. Use `causal_chain.hypothesis: true` and uncertain edges when evidence establishes correlation rather than causation.
5. For videos around 45 seconds or longer, prefer at least three useful families. Do not add a family merely to satisfy a count.
6. Run `FinanceSceneVarietyValidator` and record warnings. Resolve monotony, card overuse, unsupported mechanism visuals, and missing anchors when the warning is substantively valid; justify intentional simplicity.
7. Keep one primary claim per frame. Motion should uncover documents, draw annotations/connectors, or reveal reasoning.
8. Make the final scene a native `text_card` containing exactly `本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。` and hold it long enough to read.

Atelier plans still use these conceptual families and source rules, but must not import the reusable finance components.
