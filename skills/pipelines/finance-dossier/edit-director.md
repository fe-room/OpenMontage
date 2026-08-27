# Finance Dossier — Edit Director

Produce schema-valid `edit_decisions` from the approved scene plan and asset manifest.

## Cut construction

- Carry `render_runtime` and `composition_mode` from the approved proposal without silent substitution.
- Set explicit Explainer `width: 1080` and `height: 1920` for the normal Douyin, Xiaohongshu, YouTube Shorts, and TikTok-style delivery. Preserve any explicitly approved alternative resolution instead of inferring orientation from the platform name.
- Map finance scenes to the existing Explainer cut dispatch using flat props: `evidence_card`, `expectation_gap`, `money_flow`, `causal_chain`, `research_timeline`, `scenario_board`, or `thesis_breaker`.
- Preserve layout `variant`, source label/date, period, claim class, and sample-data marker. Use probability only when the research supplies it.
- Carry the approved optional finance presentation fields without inventing them: `canvasMode`, `density`, `headerTreatment`, `sourceTreatment`, `analystNote`, and `evidenceIndex`. Omission remains valid and uses backward-compatible component defaults.
- Ensure every edge references valid nodes. Label uncertain causal relations and never turn correlation into an unqualified causal arrow.
- Encode financial direction with `+ / -`, arrows, or textual direction as well as color.
- Use hard editorial cuts and restrained reveals; avoid continuous card bouncing and decorative transitions.
- When music source is `none`, omit the music property and layer entirely.
- Keep the final cut as the final meaningful editorial beat. Carry the exact compliance line and approved `footer` or `overlay` presentation in `edit_decisions.metadata.compliance`, with `placement: ending` and `ending_cut_id` pointing to that cut. Use a native standalone `text_card` only when explicitly requested or externally required.

Run standard timeline, asset-reference, and slideshow-risk checks. Record intentional validator-warning exceptions in metadata rather than hiding them.
