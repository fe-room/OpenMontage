# Finance Dossier — Scene Director

Produce the existing `scene_plan`. Read the approved direction carried in `script.metadata.editorial_direction` (or the approved `proposal_packet` if needed), use it as a visual-planning prior, and copy it unchanged to `scene_plan.metadata.editorial_direction` for advisory validation. For each scene, use additive finance fields (`finance_scene_type`, `finance_family`, `claim_class`, `source_anchor`, `mechanism_importance`, `layout_variant`, and `finance_justification`) only where applicable.

## Planning

1. Assign each beat to `DOCUMENT`, `DATA`, `MECHANISM`, or `DECISION` by information responsibility. Editorial Mode biases the mix but never forces a component:
   - `RESEARCH` often uses document/paper/margin-note, evidence, and expectation only when real expectations matter;
   - `MARKET` often uses data/dark-ink/full-bleed, timeline, chart, and faster visual pacing; use a causal visual only when transmission, rather than chronology or reaction data, is the actual task;
   - `MACRO` often uses data/document, timeline, conditions, and explicit uncertainty; use a causal chain only when a directional transmission path genuinely must be followed;
   - `FLOW` often makes `money_flow` the hero on data/full-bleed canvases; prefer sankey-lite only for meaningful additive allocation and do not add a second causal chain when the flow plus annotation already explains the bottleneck;
   - `EXPLAIN` often uses paper/data and a simple comparison, chart, or diagram without institutional dossier density.
2. Choose scene type and deterministic layout variant from the information structure:
   - DOCUMENT: document crop or `research_timeline`.
   - DATA: chart, `evidence_card`, or `expectation_gap`.
   - MECHANISM: `money_flow` or `causal_chain`.
   - DECISION: `scenario_board`, `thesis_breaker`, or watch list.
3. Give every major FACT/data scene a readable `source_anchor` with source label/date and period when relevant.
4. Before choosing `causal_chain`, ask whether the core information is actually directional—A influences B, which influences C—and whether the evidence supports that reading. Words such as “为什么”, “because”, “导致”, or “影响” are not sufficient. Prefer `research_timeline` for chronology, `money_flow` for allocation, `expectation_gap` for expected versus actual, a chart for movement/trend, document/evidence for proof, `scenario_board` for conditional futures, or a simpler text/diagram composition when those structures fit better. When a causal path is useful but uncertain, use `causal_chain.hypothesis: true`, uncertain edges, and language such as “可能通过”, “常见传导路径”, or “一个可能机制”.
5. For videos around 45 seconds or longer, prefer at least three useful families. Do not add a family merely to satisfy a count.
6. Run `FinanceSceneVarietyValidator` and record warnings. Resolve monotony, card overuse, unsupported mechanism visuals, missing anchors, `MODE_VISUAL_MISMATCH`, `EDITORIAL_GRAMMAR_MISMATCH`, and `MODE_COMPONENT_OVERUSE` when substantively valid; all remain advisory and intentional choices may be justified.
7. Keep one primary claim per frame. Motion should uncover documents, draw annotations/connectors, or reveal reasoning.
8. Keep the final scene editorial: it should complete the approved audience task through a watch list, thesis condition, what-next frame, bottleneck implication, takeaway, or another evidence-supported ending. Normally attach the exact disclaimer through `scene_plan.metadata.compliance` as `footer` or `overlay`, with `placement: ending` and `ending_scene_id` identifying this final scene. A standalone disclaimer scene is allowed only when explicitly requested or externally required.

## Emergent scene boundaries

Scene count is an output of the story, never a mode parameter. Start from `audience_task` and ask: what minimum sequence of cognitive steps lets the viewer complete it? Create a new scene only when the viewer's cognitive task materially changes—for example question → evidence, evidence → comparison, comparison → mechanism, event → reaction, concept → worked example, or allocation → bottleneck. Consider information complexity, argument transitions, visual reset necessity, cognitive load, and the approved duration; never target a count because a mode “usually” has that many parts.

Merge adjacent beats when they answer the same audience question, use closely related evidence, fit one understandable composition, and need no major cognitive reset. Expected value, actual value, and delta should normally be one `expectation_gap`, not three scenes. Split when one composition would force the viewer to hold incompatible mental models—for example market move, trigger evidence, conditional transmission, and what-next may require separate tasks. Optimize for clarity, not the fewest scenes and not visual-family quotas.

Record the cognitive task in `information_role`, why the visual earns its place in `shot_intent`, and the cognitive transition in `transition_in` or planning notes. Do not randomize scene count, component choice, or ending to manufacture variety.

## V1.2 editorial composition

- Prefer Chinese for narrative meaning. Use English primarily for taxonomy, source labels, issue numbers, periods, and other metadata.
- Preserve Chinese phrase integrity in headlines. Default to at most two lines, reduce size and tracking modestly before wrapping, and never strand one Chinese character on a line.
- Use vertical space intentionally. Organize primary scenes as headline → evidence or visualization → interpretation → analyst note → source, normally occupying about 55–70% of the usable portrait canvas without crowding it.
- Choose canvas treatment by information structure, not rotation or novelty:
  - document evidence usually fits `document` or `margin-note`;
  - data comparisons usually fit `paper` or `data`;
  - mechanisms usually fit `data` or `full-bleed`;
  - decisions usually fit `paper` or `margin-note`.
- A scene type may use more than one compatible canvas treatment. A sequence should feel like one publication without looking like one repeated master template.
- Use `full`, `compact`, or `none` header treatment according to visual density. Preserve source readability through `full`, `compact`, or `inline` source treatment.
- Use editorial annotations only when they explain, question, or emphasize evidence. Keep to 0–2 meaningful annotations per scene and avoid decorative doodles.
- Prefer rules, alignment, typographic grouping, underlines, brackets, and spacing before adding a bordered card.
- Preserve one primary claim per frame. Newly available space is for evidence, context, interpretation, annotations, and sources—not another unrelated claim.
- Prefer `sankey-lite` for allocation, capital flow, cost structure, revenue distribution, or value flow. Use `horizontal` only for an essentially sequential or extremely small/simple dataset.
- Choose density by information responsibility: `sparse` for a hero claim, `standard` for normal explanation, and `dense` for timelines, source pages, or compact tables. Do not default every scene to sparse.
- Build editorial rhythm across quiet, dense, hero, document, mechanism, and decision beats. This is a creative pacing principle, not a deterministic alternation rule.

Atelier plans still use these conceptual families and source rules, but must not import the reusable finance components.

Editorial Mode never decides exact scene order, count, per-scene layout variant, coordinates, card placement, or animation. A scene plan should express the same Finance Dossier brand with different editorial organization—not five themes and not one template repeated five ways.
