# Finance Editorial Direction — Semantic Router

Use this skill at the start of Finance Dossier research and confirm its result at proposal. It routes one Finance Dossier brand into an editorial strategy; it does not select a visual theme, create a pipeline, prescribe an exact scene sequence, or replace director judgment.

## Decision method

Classify the editorial task before collecting a broad source pile. Read four signals together:

1. **Question:** What must the episode answer?
2. **Mechanism:** Is the central reasoning company internals, a timestamped move, macro transmission, value allocation, or concept explanation?
3. **Evidence:** Which evidence would actually settle the question?
4. **Takeaway:** What should the viewer be able to judge or explain afterward?

Do not classify from entity names or isolated keywords. Run the counterfactual test: remove company, asset, and institution names from the topic; the remaining causal question should still support the chosen mode. For example, “美联储降息为什么可能影响英伟达估值？” is primarily `MACRO`, secondarily `RESEARCH`, when the core chain is rate → discount rate → growth-stock valuation → company context.

Choose exactly one primary mode and no more than one secondary mode. A secondary mode must change evidence or reasoning priorities; do not add it merely because another entity type appears in the title. If three modes seem plausible, state the dominant viewer task and discard the weakest one.

## Modes

### RESEARCH

- Question: what is happening inside this company, and what is the market pricing?
- Prior grammar: `ANOMALY → EVIDENCE → EXPECTATION → MECHANISM → IMPLICATION → THESIS CHANGE`.
- Evidence: filings, investor relations, earnings, statements, consensus or expectations, and company operating evidence.
- Existing visual priorities: document, `evidence_card`, `expectation_gap`, chart, `research_timeline`, `causal_chain`, `thesis_breaker`, `scenario_board`.
- Canvas prior: paper, document, margin-note, data.
- Anti-pattern: do not turn every data point into an EvidenceCard; do not make a deterministic stock call; do not equate reported results with consensus.

### MARKET

- Question: what moved, when, what triggered it, and what transmission matters next?
- Prior grammar: `WHAT MOVED → WHEN → TRIGGER → TRANSMISSION → WHAT NEXT`.
- Evidence: timestamped market data, announcements, official events, reaction windows, and reputable real-time reporting.
- Existing visual priorities: `research_timeline`, chart, `causal_chain`, concise evidence; use `expectation_gap` only when expectations explain the move.
- Canvas prior: data, full-bleed, dark-ink, compact paper. Pacing is faster and more immediate than RESEARCH.
- Anti-pattern: do not impose filing-page pacing on a simple move, decorate with candlesticks, force a ThesisBreaker ending, or claim one cause while alternatives remain plausible.

### MACRO

- Question: how does one macro variable transmit into another variable, the economy, or an asset?
- Prior grammar: `VARIABLE → TRANSMISSION → SECOND-ORDER EFFECT → IMPACT → CHAIN BREAKER`.
- Evidence: central banks, official statistics, rates, government agencies, and primary policy documents.
- Existing visual priorities: `causal_chain`, `research_timeline`, chart, document, and `scenario_board` when uncertainty matters.
- Canvas prior: data, document, full-bleed, margin-note.
- Anti-pattern: do not imply that correlation proves causation or make a conditional transmission path look deterministic through a single clean arrow.

### FLOW

- Question: where does money or value flow, who captures it, and where is the bottleneck?
- Prior grammar: `SOURCE → ALLOCATION → VALUE CAPTURE → BOTTLENECK → IMPLICATION`.
- Evidence: segment disclosures, cost structures, industry research, supply-chain and value-chain data.
- Existing visual priorities: `money_flow`, sankey-lite, `causal_chain`, `evidence_card`, and supporting charts.
- Canvas prior: data, full-bleed, margin-note.
- Anti-pattern: do not use Sankey because several numbers exist. Confirm that flows are meaningfully additive or linked; unrelated metrics must not be presented as a conserved total.

### EXPLAIN

- Question: what is the mechanism, and what one example makes it understandable?
- Prior grammar: `QUESTION → MECHANISM → EXAMPLE → MISUNDERSTANDING → TAKEAWAY`.
- Evidence: authoritative conceptual sources where needed, stable definitions, and a clear worked example. Avoid research overhead that adds no truth value.
- Existing visual priorities: `causal_chain`, comparison through existing data scenes, simple chart, text/diagram, and `money_flow` only when useful.
- Canvas prior: paper, data, margin-note.
- Anti-pattern: do not force institutional research density, ThesisBreaker, ScenarioBoard, or excessive sourcing onto a stable educational concept.

## Hybrid and fallback rules

- `RESEARCH + FLOW`: company economics are the primary judgment; value capture explains them.
- `MARKET + MACRO`: the immediate move is primary; macro transmission explains it.
- `MACRO + RESEARCH`: system transmission is primary; company valuation or fundamentals supply the endpoint context.
- `EXPLAIN + MACRO`: conceptual understanding is primary; macro mechanics provide the domain.
- `FLOW + RESEARCH`: allocation is the primary question; company disclosures ground the answer.

If confidence is low, still choose one primary mode and explain the ambiguity. Fall back to `RESEARCH` only for genuine evidence-based financial analysis. Use `EXPLAIN` for stable conceptual questions. Never fall back to `MARKET`, because that would invent time sensitivity.

## Artifact contract

Write the result to `metadata.editorial_direction` in `research_brief`. Proposal may refine it after evidence review and must carry the approved result into `proposal_packet.metadata.editorial_direction`. Scene Director copies the approved object into `scene_plan.metadata.editorial_direction` so advisory validation has local context.

Required strategy fields:

```yaml
editorial_direction:
  primary_mode: MACRO
  secondary_mode: RESEARCH  # optional; at most one
  classification_confidence: high  # high | medium | low
  audience_task: understand_mechanism
  rationale:
    - "The core story is rate transmission into growth-stock valuation."
  evidence_priority: [central_banks, rates_data, company_context]
  visual_priority: [causal_chain, chart, expectation_gap]
  canvas_preference: [data, margin-note, paper]
  density_profile:
    opening: sparse
    body: standard
    evidence: dense
    ending: sparse
  hook_grammar: CONTRADICTION
  ending_grammar: WATCH_LIST
  key_editorial_risk: "Do not imply a deterministic valuation response."
  key_anti_pattern: "Do not force company-report pacing onto a transmission story."
```

These are priors, not commands. Do not include exact scene order, scene count, layout variants, coordinates, animation, or card placement. Those remain Script and Scene Director decisions.

`visual_priority` is a ranked candidate set, never a component checklist. In particular, the presence of `causal_chain` means “consider it if the audience task requires a supported directional mechanism,” not “insert one because this mode explains why.” Scene count and component selection must emerge from cognitive transitions and information structure.
