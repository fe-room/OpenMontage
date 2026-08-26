# Finance Dossier — Research Director

Produce the existing `research_brief` artifact. Read `creative/finance-storytelling.md` and `meta/finance-video-editorial.md` first.

## Method

1. Fix the one core question the video will answer and set `content_category: finance` in canonical metadata.
2. Build an evidence ledger using the source hierarchy: Tier 1 first, Tier 2 for context, Tier 3 only for question/sentiment discovery.
3. For every major claim, record `claim_class` (`FACT`, `INFERENCE`, `THESIS`, or `SCENARIO`), source URL/title, source tier, publication/event date, relevant period, comparison basis, and limitations. Store this in supported `data_points`, `sources`, and artifact metadata rather than inventing a new artifact type.
4. Reconcile conflicting definitions, periods, currencies, units, restatements, and adjusted versus reported metrics.
5. Identify the anomaly, conventional explanation, evidence, plausible mechanism, expectations, implications, and thesis-changing evidence that the available sources actually support.
6. Discover at least three genuinely different angles using the four hook grammars. Do not manufacture angles unsupported by sources.

## Fail conditions

- A major factual claim rests only on Tier 3.
- A number lacks material period/comparison context.
- An inference is written as fact.
- Consensus, probability, market price, forecast, or real-time value is invented.

Self-review against the manifest and checkpoint the schema-valid `research_brief`.
