# Finance Dossier — Research Director

Produce the existing `research_brief` artifact. Read `creative/finance-editorial-direction.md`, `creative/finance-storytelling.md`, and `meta/finance-video-editorial.md` first.

## Method

1. Fix the one core question the video will answer and set `content_category: finance` in canonical metadata.
2. Route that question semantically into one primary Editorial Mode and at most one useful secondary mode. Judge the question, mechanism, evidence required, and intended takeaway—not entity names or isolated keywords. Write the complete contract to `research_brief.metadata.editorial_direction`.
3. Build an evidence ledger using both the global source hierarchy and the mode prior:
   - `RESEARCH`: company filings, IR, earnings, statements, consensus/expectations, and company operating evidence;
   - `MARKET`: timestamped market data, announcements, official events, reaction windows, and reputable real-time reporting;
   - `MACRO`: central banks, official statistics, rates, agencies, and primary policy documents;
   - `FLOW`: segment disclosures, cost structures, industry research, and value-chain data;
   - `EXPLAIN`: authoritative conceptual sources and stable definitions where needed, without needless research overhead.
   Tier 1 still leads, Tier 2 adds context, and Tier 3 is only for question/sentiment discovery.
4. For every major claim, record `claim_class` (`FACT`, `INFERENCE`, `THESIS`, or `SCENARIO`), source URL/title, source tier, publication/event date, relevant period, comparison basis, and limitations. Store this in supported `data_points`, `sources`, and artifact metadata rather than inventing a new artifact type.
5. Reconcile conflicting definitions, periods, currencies, units, restatements, and adjusted versus reported metrics.
6. Identify the beats supported by the selected mode grammar. Do not manufacture an expectation gap for RESEARCH, a timeline for MARKET, a causal certainty for MACRO, an additive total for FLOW, or institutional complexity for EXPLAIN.
7. Discover at least three genuinely different angles. Hook and ending options should reflect Editorial Direction while remaining evidence-led.

## Fail conditions

- A major factual claim rests only on Tier 3.
- A number lacks material period/comparison context.
- An inference is written as fact.
- Consensus, probability, market price, forecast, or real-time value is invented.
- Editorial Direction contains more than one secondary mode or exact scene execution decisions.

Self-review against the manifest and checkpoint the schema-valid `research_brief`.
