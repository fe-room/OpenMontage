# Executive Producer — Finance WeChat Article

## When to Use

Use this skill when the requested deliverable is a WeChat Official Account
article derived from a finance video or finance-video project. Read
`meta/finance-wechat-editorial` before the first stage and keep it active for all
stages.

## Source and Workspace Contract

Initialize a new child workspace with pipeline type `finance-wechat-article`.
Do not modify the source video's artifacts. Record its project ID or local path
in `wechat_source_analysis.source` and write all outputs under the new project:

```text
projects/<article-project>/
  artifacts/
  assets/images/
  deliverables/wechat/
    article.md
    images/
    sources.md
    manifest.json
```

## Serial Flow

Execute exactly:

`source_analysis -> screening -> evidence -> drafting -> visuals -> packaging`

Before each stage, read that stage's director skill. Validate its primary
artifact, self-review against the manifest, and write the checkpoint.

## Branching and Gates

- `screening` is always a human gate. Present the four scores, total, rationale,
  article tier, series placement, and recommendation.
- If the user approves `skip`, complete the screening checkpoint with
  `approved_action: skip` and end the run successfully. The manifest's
  `halt_when` rule makes this resumable.
- If the user approves `upgrade_then_write`, the upgraded question replaces the
  source question for evidence and drafting. Never research the discarded hot
  take as though it were still the article question.
- `evidence`, `drafting`, and `visuals` are separate human gates. Approval at an
  earlier gate never pre-approves a later one.
- Run the deterministic local packager only after the visual package is approved.

## Cross-Stage Checks

- Screening evidence must be traceable to source analysis.
- Every draft claim reference must resolve into `finance_article_research`.
- Every chart spec must resolve to one research question and source set.
- Rendered chart values, labels, dates, and units must match research exactly.
- The title, digest, cover, and body must express the same qualified conclusion.
- The exact article disclaimer must survive draft and package validation.

## Completion

Completion means a schema-valid local package exists and
`manual_publish_required` is true. Do not report the article as published.
