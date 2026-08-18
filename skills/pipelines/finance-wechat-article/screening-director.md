# Screening Director — Finance WeChat Article

## Objective

Decide whether the source deserves a durable article. Produce
`wechat_content_screen` and stop at the mandatory human gate.

## Four-Question Score

Give exactly one point for `yes`, zero for `no`, and cite concrete evidence from
`wechat_source_analysis` for each answer:

1. `evergreen_value` — will the question still matter in six months?
2. `unfinished_depth` — did short-video limits leave important material out?
3. `evidence_value` — is data, a chart, a calculation, or a method worth saving?
4. `series_fit` — can this become part of a durable series/archive?

Map totals exactly: 3-4 strongly recommended, 2 recommended, 0-1 not
recommended. The semantic validator rejects inconsistent totals and bands.

## Upgrade Logic

For a short-lived topic, ask whether it can become a durable question. Example:
replace an intraday complaint with a question about recurring investor behavior.
Set `upgrade_then_write` only when `can_upgrade` is true and the upgraded
question is concrete. A vague “make it more evergreen” is not an upgrade path.

## Tier and Series

Choose one tier only if writing remains viable:

- A: core research/data experiment;
- B: durable knowledge extension;
- C: long-running experiment log.

Name a real series when possible, such as 财经数据实验室、红利ETF系列、实盘实验记录、财经研究工具箱.

## Human Gate

Present the scorecard and recommend `write`, `upgrade_then_write`, or `skip`.
Write `awaiting_human` and end the turn. After the user's decision, write the
same stage `completed`, set `human_approved: true`, and record the chosen
`approved_action`. `skip` ends the pipeline successfully.

## Quality Checklist

- [ ] Every score has evidence, not enthusiasm.
- [ ] Band equals the numeric score.
- [ ] 0-1 never goes straight to `write`.
- [ ] Upgrade question is durable and materially different.
- [ ] The user's action is explicit and preserved.
