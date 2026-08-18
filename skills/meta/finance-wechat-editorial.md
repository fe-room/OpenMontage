# Finance Video → WeChat Editorial Policy

## Activation Boundary

Use this policy only for the `finance-wechat-article` derivative pipeline. The
source must be a completed OpenMontage finance project or a local finance video.
It does not change the original video's pipeline or publish status.

## Product Principle

The article is not the video's transcript. Treat both as outputs of the same
research:

- the video earns attention with the question, conflict, conclusion, and
  strongest evidence;
- the article preserves data sources, definitions, calculations, charts,
  counterexamples, limitations, complete reasoning, and reusable methods.

The branch exists to build a searchable finance research archive, not to turn
every posted video into text.

## Screening Contract

Score exactly four questions, one point for `yes` and zero for `no`:

1. Will the question still matter in six months?
2. Did the video leave important reasoning, method, or evidence unfinished?
3. Is there data, a chart, a calculation, or a research process worth saving?
4. Can it join a durable series or archive?

Interpret totals exactly:

- `3-4`: `strongly_recommended` — proceed unless the user declines.
- `2`: `recommended` — explain the tradeoff and let the user decide.
- `0-1`: `not_recommended` — `skip`, unless an explicit evergreen question
  upgrades a timely/emotional topic before research begins.

The approved action is one of `write`, `upgrade_then_write`, or `skip`. A
completed `skip` is a successful terminal outcome: no research, visuals, or
packaging should run.

## Article Tiers

- `A_core_research`: data experiments and important investment questions;
  target 1500-3000+ Chinese characters.
- `B_knowledge_extension`: ETF, valuation, dividends, market-cap and other
  durable concepts; target 800-1500 Chinese characters.
- `C_experiment_log`: period updates for a long-running experiment; target
  500-1000 Chinese characters.

Choose the tier by content responsibility, not by screening score.

## Evidence Before Conclusion

Use this order:

`approved question -> data/case/live record -> method -> result -> explanation -> boundaries -> takeaway`

- Preserve source, access date, as-of date, market/instrument scope, sample,
  metric definition, and calculation rule for each material claim.
- Separate `observed_fact`, `calculation`, and `interpretation`.
- Keep conflicting or inconclusive evidence. Qualify probabilities and avoid
  unsupported absolutes such as “一定”, “稳赚”, “必赚”, or “千万别买”.
- Historical data is evidence about history, not a promise about the future.
- Every dataset and every figure must answer a named sub-question.

## Default Article Structure

1. Open with a specific question, misconception, scene, or data conflict.
2. State “先说结论” within the opening section; do not hide the answer.
3. Explain data range, sample, indicator definitions, and calculation rules.
4. Show only the 2-5 pieces of evidence that carry the argument.
5. Explain why the result may occur in ordinary language.
6. Present counterexamples, limitations, and where the conclusion stops.
7. End with no more than three reusable takeaways.

For data experiments, prefer the eight-section pattern: why test it, conclusion,
method, result, surprising details, mechanism, limitations, reader method. For
experiment logs, use: current event, current data, meaningful changes, judgment
change, next plan.

## Writing and Title Rules

- Prefer question, data-validation, or honest counterintuitive titles.
- The first 200 Chinese characters must explain why the article is worth time.
- Use a subheading every 300-500 Chinese characters; keep paragraphs to roughly
  2-5 mobile lines.
- Explain a technical term on first use. Example: explain what drawdown feels
  like before relying on the word “最大回撤”.
- A reader scanning headings and bold text should recover roughly 70% of the
  reasoning.
- Do not inflate a qualified conclusion in the title, cover, digest, or series
  label.

## Visual Rules

- Use a short problem-led cover with native exact text.
- Own data charts come first, explanatory diagrams second, necessary source
  screenshots third. Decorative stock imagery is normally rejected.
- A figure answers one question. Its title states the conclusion, not merely
  “图1” or “分组表现”.
- Show source, date range, unit, and statistical definition under each chart.
- Precision-critical labels and numbers must be rendered deterministically;
  never ask an image model to reproduce financial data or Chinese cover text.
- Verify at phone width and remove any figure that does not advance the core
  question.

## Tail Module and Publication Boundary

Carry a data note, up to three related-reading links/placeholders, and this
exact sentence at the article tail:

> 本文用于财经知识和数据研究记录，不构成对具体证券的买卖建议。

The pipeline packages local files only. It must not log in to, upload to, save a
remote draft in, or publish on WeChat Official Accounts. The user performs the
platform publication after reviewing the package.

## Critical Findings

Treat these as critical and revise before proceeding:

- a transcript was lightly reformatted instead of creating a distinct article;
- a 0-1 topic proceeds without an approved evergreen upgrade;
- a material claim has no traceable source or its scope/date/definition is lost;
- a chart combines unrelated questions, hides its statistical definition, or
  visually exaggerates the conclusion;
- the article omits counterevidence, limitations, or a reusable judgment method;
- the exact disclaimer is absent or not at the tail;
- packaging attempts any remote publication action.
