# Finance Dossier

`finance-dossier` is OpenMontage's evidence-first finance video system. Its visual identity is a financial research dossier / editorial analyst desk: filings, source documents, annotations, data, mechanisms, and conditional decisions. It deliberately avoids broadcast-finance imitation, neon fintech, generic market montage, and decorative corporate imagery.

## Pipeline usage

Select `pipeline_defs/finance-dossier.yaml`. The pipeline follows the canonical lifecycle:

`research -> proposal -> script -> scene_plan -> assets -> edit -> compose -> cover -> publish`

It reuses the existing `research_brief`, `proposal_packet`, `script`, `scene_plan`, `asset_manifest`, `edit_decisions`, `render_report`, `cover_package`, and `publish_log` artifacts. Finance-specific scene meaning and Remotion props are additive fields in those contracts.

## Editorial Direction

Finance Dossier is one brand system. Editorial Mode is the storytelling strategy used inside that brand; it is not a visual theme, template, renderer, or separate pipeline. The instruction-driven Editorial Router reads the core question, mechanism, evidence required, and intended viewer takeaway before broad research, then records one `primary_mode` and at most one `secondary_mode` in the existing artifact metadata rail:

`research_brief.metadata.editorial_direction → proposal_packet.metadata.editorial_direction → script.metadata.editorial_direction → scene_plan.metadata.editorial_direction`

Proposal confirms or revises the research-stage direction from actual evidence. Script and Scene Directors consume it as a prior while retaining creative judgment over beat order, scene count, existing component choice, V1.2 canvas treatment, density, header, and animation.

- `RESEARCH` asks what is happening inside a company and what the market is pricing. It prioritizes filings, operating evidence, expectations when real, mechanisms, and thesis-changing conditions.
- `MARKET` asks what moved, when, what triggered it, and what transmission matters next. It prioritizes timestamped evidence and faster data-led pacing without claiming one cause prematurely.
- `MACRO` asks how a variable or policy transmits through the system. It prioritizes primary policy/statistical sources, conditional causal chains, second-order effects, and chain breakers.
- `FLOW` asks where money or value goes, who captures it, and where the bottleneck lies. It prefers `money_flow` or other mechanism visuals only when the values are genuinely linked or additive.
- `EXPLAIN` asks how a finance mechanism works and which single example makes it understandable. It may stay simple and educational rather than simulating institutional research complexity.

Hybrid stories use one supporting lens, never three modes. Examples include `RESEARCH + FLOW` for Costco membership economics, `MARKET + MACRO` for a timestamped dollar/gold move, `MACRO + RESEARCH` for rates transmitting into growth-stock valuation, and `EXPLAIN + RESEARCH` for free cash flow versus net income.

Mode never forces a component. In particular, `ExpectationGap`, sankey-lite, and `ThesisBreaker` appear only when their semantics fit. `FinanceSceneVarietyValidator` retains its V1.2 warnings and adds advisory mode checks for visual mismatch, grammar mismatch, component overuse, and compound mode-signature regularity; equal scene counts alone do not warn and normal creative choices do not hard-fail.

Scene count is emergent. Create a new scene only when the viewer's cognitive task materially changes; merge adjacent beats that answer the same question in one understandable composition, and split only when clarity requires a visual or mental reset. Editorial modes provide preferences, not mandatory sequences or component checklists.

`causal_chain` is reserved for genuine directional mechanisms. Chronology, allocation, expected-versus-actual, data movement, proof, and conditional futures should use the existing timeline, money-flow, expectation-gap, chart, document/evidence, or scenario treatments when those structures fit better.

The pipeline always classifies the run as finance and preserves the exact native disclaimer required by `AGENT_GUIDE.md`. Normal Finance Dossier work renders it as quiet footer/overlay metadata on the final meaningful editorial scene; an explicitly requested or externally required standalone card remains supported. Compliance must not replace the editorial ending.

## Resolution and brand

Finance short-form props use explicit `"width": 1080, "height": 1920` for Douyin, Xiaohongshu, YouTube Shorts, and TikTok-style delivery. The same `Explainer` composition supports other explicitly requested sizes; it does not infer or override orientation. Legacy Explainer props without dimensions remain 1920×1080.

Public identity is optional: `"brand": {"label": "老朋友研究所", "series": "FINANCE DOSSIER", "issue": "DOSSIER 038"}`. With no brand object, frames use a clean `FINANCE DOSSIER` label and never expose the OpenMontage engine name.

## Daily vs hero

- Daily or routine finance content normally uses `composition_mode: templated` with the deterministic finance component grammar in the existing Remotion `Explainer` composition.
- Hero or deep-research work may use `composition_mode: atelier`. It retains the dossier palette, typography, source treatment, evidence orientation, and analytical restraint, but follows the bespoke doctrine: reuse engine knowledge, never reusable finance components or prior creative compositions.

The proposal still compares Remotion and HyperFrames and waits for explicit runtime approval.

## Scene types

- `evidence_card`: claim, primary value, supporting metrics, period, source, and interpretation; variants `hero-number`, `comparison`, `document`, `table`.
- `expectation_gap`: expected versus actual with an explicit delta; variants `split`, `stacked`, `delta`, `reveal`.
- `money_flow`: deterministic nodes and directed value-flow edges; variants `vertical`, `horizontal`, `radial`, `split`, `sankey-lite`.
- `causal_chain`: directed reasoning with positive, negative, or uncertain relations. Use hypothesis labeling when evidence does not establish causality.
- `research_timeline`: sourced events in horizontal or vertical layouts.
- `scenario_board`: conditional named cases with triggers, optional sourced probabilities, and metrics to watch.
- `thesis_breaker`: one to four conditions that would invalidate or materially weaken a thesis.
- `SourceStrip`: reusable readable period/source/date metadata and `SAMPLE DATA` labeling.

Finance scenes also accept additive presentation controls without creating new scene types: `canvasMode` (`paper`, `document`, `data`, `margin-note`, `dark-ink`, `full-bleed`), `density` (`sparse`, `standard`, `dense`), `headerTreatment` (`full`, `compact`, `none`), `sourceTreatment` (`full`, `compact`, `inline`), plus optional `analystNote` and real `evidenceIndex` metadata. Omitting these fields preserves the V1.1-compatible defaults.

The scene director groups these into `DOCUMENT`, `DATA`, `MECHANISM`, and `DECISION` families. After normal scene-plan schema validation, `write_checkpoint` automatically runs `FinanceSceneVarietyValidator` for this pipeline and attaches deduplicated advisory results at `review.finance_scene_variety`. The warnings cover monotony, card overuse, repeated types, low family diversity, missing mechanism visuals, and missing source anchors; they do not hard-fail creative choices.

## Evidence rules

Use Tier 1 sources first: regulators, exchanges, central banks, official statistics, company IR, filings, reports, releases, transcripts, and announcements. Tier 2 adds reputable news and research. Tier 3 may discover questions or sentiment but cannot solely support a major factual claim.

Classify important claims as `FACT`, `INFERENCE`, `THESIS`, or `SCENARIO`. Never present the latter three as facts. Include period, baseline, denominator, and comparison context where they materially affect a number. Never invent expected values, consensus, probability, prices, forecasts, or real-time data.

## Style principles

The `finance-dossier` playbook uses warm paper (`#F2EFE7`), ink (`#171715`), muted text (`#6C6860`), vermillion annotation (`#B44736`), deep teal (`#345C5B`), and ochre (`#C5A64A`). Direction always includes signs, arrows, or text labels; red/green color alone is not meaningful encoding.

Use asymmetric editorial grids, generous negative space, document crops, annotations, and one primary claim per frame. Motion should reveal evidence or reasoning through masks, underlines, crop/zoom, connector lines, progressive causal steps, subtle slides, and hard editorial cuts.

Narrative language is Chinese-first; English is reserved mainly for publication taxonomy and metadata. Finance headlines use a deterministic two-line fitting strategy with semantic break preference and Chinese orphan protection. Canvas and header/source treatments vary according to information structure so scenes belong to the same publication without repeating one master template.

## Demo

The zero-key curated demo is `remotion-composer/public/demo-props/finance-dossier-sample.json`. Every value is explicitly fictional or labeled `SAMPLE DATA`; it is designed for a 1080×1920 render.

Local validation:

```bash
cd remotion-composer
npm ci
npm run typecheck
npm run bundle:remotion
npm run validate:remotion
npm run smoke:finance
```

The smoke command discovers both legacy and vertical metadata contracts, then renders representative fictional stills for evidence, all four expectation-gap variants, horizontal and Sankey-lite money flow, timeline, and scenario components into `remotion-composer/out/finance-smoke/`.

## Example prompt

> Create a 60-75 second Chinese finance short about why strong company results can still disappoint the market. Use the finance-dossier pipeline. Focus on expectation gaps, evidence, and the conditions that would change the thesis.
