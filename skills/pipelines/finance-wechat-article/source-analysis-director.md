# Source Analysis Director — Finance WeChat Article

## Objective

Ground the derivative in what the source video actually says. Produce
`wechat_source_analysis`; do not score or write the article yet.

## Process

1. Prefer an OpenMontage source project's `research_brief`, `proposal_packet` or
   `brief`, `script`, `scene_plan`, `edit_decisions`, and final render.
2. If only a local video exists, use `transcriber` and inspect representative
   frames with `frame_sampler`. Write outputs inside the child workspace.
3. Verify the source is finance content. If it is not, fail this pipeline and
   route the user to a general article workflow instead of applying finance
   rules.
4. Reduce the source to one core question and list its actual conclusions.
5. Separate evidence visibly shown from depth omitted by short-video limits:
   source data, sample selection, calculations, charts, counterexamples,
   limitations, cases, or reusable tools.
6. Classify time sensitivity honestly. “Intraday” and “days” are warning signals,
   not automatic upgrades to evergreen value.
7. Record only real expansion opportunities. An opportunity is not evidence yet.

## Quality Checklist

- [ ] Source project/path and artifact/transcript provenance are present.
- [ ] Core question is one sentence.
- [ ] Conclusions and omitted depth are not inferred beyond the source.
- [ ] Time sensitivity is explicit.
- [ ] No article prose or screening score has leaked into this artifact.
