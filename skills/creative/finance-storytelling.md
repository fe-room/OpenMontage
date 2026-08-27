# Finance Storytelling — Dossier Grammar

Use this skill for `finance-dossier` research, scripts, scene plans, and reviews. The creative identity is a financial research dossier / editorial analyst desk: source documents, evidence, annotations, causal reasoning, and restrained data visualization. It must not resemble generic AI finance, financial television, a trading terminal, neon fintech, or a corporate explainer.

## Source hierarchy

Rank evidence before writing:

1. **Tier 1:** regulators, exchanges, central banks, national statistics agencies, company investor relations, filings, annual or quarterly reports, earnings releases, earnings-call transcripts, and official announcements.
2. **Tier 2:** major financial news organizations, reputable industry research, and established research institutions.
3. **Tier 3:** commentary, forums, and social media. Use Tier 3 to discover questions or sentiment, never as the sole support for a major factual claim.

For each important claim, record one conceptual class:

- `FACT` — directly supported by evidence.
- `INFERENCE` — a reasoned reading of facts; label the reasoning step.
- `THESIS` — the video's current analytical view; state boundary conditions.
- `SCENARIO` — a conditional future case, not a prediction.

Never present `INFERENCE`, `THESIS`, or `SCENARIO` as `FACT`. Every numerical claim should include the relevant period, denominator, baseline, and comparison context whenever those affect interpretation. Never invent analyst consensus, expected values, probabilities, prices, forecasts, or real-time data to fill a visual.

## Narrative grammar

First read `creative/finance-editorial-direction.md`. Its primary mode identifies the editorial question; this skill governs evidence discipline and the shared Finance Dossier voice. Mode is not a theme and does not force components.

Do not default to `hook -> three points -> conclusion`. Prefer this reasoning sequence, omitting stages that do not serve the topic:

`ANOMALY -> CONVENTIONAL EXPLANATION -> EVIDENCE -> MECHANISM -> EXPECTATION -> IMPLICATION -> WHAT WOULD CHANGE THE THESIS`

Choose the opening by information responsibility:

- `CONTRADICTION` — two apparently incompatible facts.
- `STRANGE_NUMBER` — a number whose meaning is not obvious until context arrives.
- `DOCUMENT_REVEAL` — a filing, release, transcript, or official record changes the reading.
- `EXPECTATION_GAP` — results and prior expectations diverge.

Choose an ending that keeps uncertainty useful:

- `SCENARIO_BOARD` — conditional cases and their triggers.
- `THESIS_BREAKER` — evidence that would invalidate or materially weaken the thesis.
- `WATCH_LIST` — specific metrics, dates, filings, or events to monitor.
- `OPEN_QUESTION` — the unresolved question and what evidence could answer it.

Avoid repeating the same opening, beat order, or ending across consecutive productions when another grammar better fits the evidence.

The anomaly-to-thesis sequence is most natural for `RESEARCH`, not a universal finance template. `MARKET`, `MACRO`, `FLOW`, and `EXPLAIN` use their own preferred reasoning grammars from Editorial Direction. Preserve one brand while allowing materially different pacing, evidence order, and endings.

## Scene families

Classify each scene by its conceptual job:

- `DOCUMENT`: filing, source document, official announcement, or reference evidence.
- `DATA`: stat, chart, `evidence_card`, or `expectation_gap`.
- `MECHANISM`: `money_flow` or `causal_chain`.
- `DECISION`: `scenario_board`, `thesis_breaker`, or a watch list.

For videos around 45 seconds or longer, prefer at least three useful families when the topic supports them. Do not force decorative variety. If the script makes an important mechanism claim, visualize it; if evidence supports only correlation, label a causal diagram as a hypothesis and use uncertain relations.

## Editorial visual and motion rules

- One primary claim per frame.
- Put a readable source anchor on major factual and data scenes.
- Prefer documents, deterministic diagrams, and charts over generic stock footage.
- Never use market imagery as filler.
- Financial direction requires `+ / -`, arrows, or textual labels; color alone is insufficient.
- Motion reveals reasoning: mask a source passage, draw an underline, follow a connector, reveal a causal step, or crop into a document.
- Use deterministic layout variants selected by information structure, not random decoration. If cosmetic randomness is unavoidable, seed it; never use `Math.random()` per frame.
- Keep sources and evidence metadata readable on a 1080×1920 mobile render.

## Templated vs atelier

- Routine or daily finance content: recommend `composition_mode: templated` and the reusable finance component grammar.
- Hero or deep-research content: consider `composition_mode: atelier`, preserve the finance-dossier palette, typography, source treatment, evidence orientation, and restraint, but do not import or reassemble reusable finance scenes. Follow `skills/meta/bespoke-composition.md`: reuse engine knowledge, not creative compositions.

## Compliance ending

Every Finance Dossier video carries this native exact text at the end, unchanged:

> 本视频仅作知识分享，不构成任何投资建议。市场有风险，投资需谨慎。

Normally render it as a quiet footer or overlay on the final meaningful editorial scene and carry the presentation through artifact `metadata.compliance`. The ending itself must still answer the audience task. Use a standalone exact-text card only when explicitly requested or required by an external platform, legal, or workflow policy. Never bake the line into generated imagery.
