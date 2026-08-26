# Finance Dossier

`finance-dossier` is OpenMontage's evidence-first finance video system. Its visual identity is a financial research dossier / editorial analyst desk: filings, source documents, annotations, data, mechanisms, and conditional decisions. It deliberately avoids broadcast-finance imitation, neon fintech, generic market montage, and decorative corporate imagery.

## Pipeline usage

Select `pipeline_defs/finance-dossier.yaml`. The pipeline follows the canonical lifecycle:

`research -> proposal -> script -> scene_plan -> assets -> edit -> compose -> cover -> publish`

It reuses the existing `research_brief`, `proposal_packet`, `script`, `scene_plan`, `asset_manifest`, `edit_decisions`, `render_report`, `cover_package`, and `publish_log` artifacts. Finance-specific scene meaning and Remotion props are additive fields in those contracts.

The pipeline always classifies the run as finance and applies the mandatory finance editorial policy. Every finished video ends with the native exact-text disclaimer required by `AGENT_GUIDE.md`.

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

The scene director groups these into `DOCUMENT`, `DATA`, `MECHANISM`, and `DECISION` families. After normal scene-plan schema validation, `write_checkpoint` automatically runs `FinanceSceneVarietyValidator` for this pipeline and attaches deduplicated advisory results at `review.finance_scene_variety`. The warnings cover monotony, card overuse, repeated types, low family diversity, missing mechanism visuals, and missing source anchors; they do not hard-fail creative choices.

## Evidence rules

Use Tier 1 sources first: regulators, exchanges, central banks, official statistics, company IR, filings, reports, releases, transcripts, and announcements. Tier 2 adds reputable news and research. Tier 3 may discover questions or sentiment but cannot solely support a major factual claim.

Classify important claims as `FACT`, `INFERENCE`, `THESIS`, or `SCENARIO`. Never present the latter three as facts. Include period, baseline, denominator, and comparison context where they materially affect a number. Never invent expected values, consensus, probability, prices, forecasts, or real-time data.

## Style principles

The `finance-dossier` playbook uses warm paper (`#F2EFE7`), ink (`#171715`), muted text (`#6C6860`), vermillion annotation (`#B44736`), deep teal (`#345C5B`), and ochre (`#C5A64A`). Direction always includes signs, arrows, or text labels; red/green color alone is not meaningful encoding.

Use asymmetric editorial grids, generous negative space, document crops, annotations, and one primary claim per frame. Motion should reveal evidence or reasoning through masks, underlines, crop/zoom, connector lines, progressive causal steps, subtle slides, and hard editorial cuts.

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
