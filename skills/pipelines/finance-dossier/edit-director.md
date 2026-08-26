# Finance Dossier — Edit Director

Produce schema-valid `edit_decisions` from the approved scene plan and asset manifest.

## Cut construction

- Carry `render_runtime` and `composition_mode` from the approved proposal without silent substitution.
- Map finance scenes to the existing Explainer cut dispatch using flat props: `evidence_card`, `expectation_gap`, `money_flow`, `causal_chain`, `research_timeline`, `scenario_board`, or `thesis_breaker`.
- Preserve layout `variant`, source label/date, period, claim class, and sample-data marker. Use probability only when the research supplies it.
- Ensure every edge references valid nodes. Label uncertain causal relations and never turn correlation into an unqualified causal arrow.
- Encode financial direction with `+ / -`, arrows, or textual direction as well as color.
- Use hard editorial cuts and restrained reveals; avoid continuous card bouncing and decorative transitions.
- When music source is `none`, omit the music property and layer entirely.
- Make the final cut a native `text_card` containing exactly `本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。`

Run standard timeline, asset-reference, and slideshow-risk checks. Record intentional validator-warning exceptions in metadata rather than hiding them.
