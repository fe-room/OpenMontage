# Finance Video Editorial Policy

## Activation Boundary

Read and apply this skill only after intake, idea, or proposal classifies the
production as `content_category: finance`. It is a conditional editorial layer,
not a default pipeline stage. For every other category, do not apply these
rules, do not add finance-specific artifacts, and continue through the selected
pipeline unchanged.

This policy supplements the chosen pipeline director; it does not replace the
pipeline, its stage order, or its approval gates.

## Governing Principle

Use this order:

`question -> data/case/live-record verification -> conclusion -> expression`

Never choose a conclusion first and search for supporting evidence afterward.
A counterintuitive angle is welcome; a counterfactual one is not. Every material
conclusion must be traceable to data, a real case, or an explicitly identified
live/account record.

## Stage Integration

### Intake / Idea / Proposal

- Reduce the piece to one core question. If deleting a proposed beat does not
  weaken the answer, remove that beat.
- Build the angle from evidence already found, not from a desired hot take.
- Put a conflict, direct question, counterintuitive result, contradiction, or
  real experiment inside the first 5-10 seconds. Do not open with background,
  greetings, episode history, or “today we will discuss”.
- Record the core question and the evidence needed to answer it in the brief or
  proposal. Do not approve a conclusion whose evidence plan is missing.

### Research

- Research the question, not a predetermined thesis.
- For each material claim, preserve the source, date/as-of time, market or
  instrument scope, measurement definition, and relevant comparison period.
- Separate observed facts from interpretation. Conflicting or inconclusive
  evidence must survive into the script as uncertainty or a boundary condition.
- Do not collect numbers merely to make the video look authoritative. Every
  retained dataset must answer a named sub-question that advances the core one.

### Script

Prefer this eight-beat structure when creating an original finance short:

1. Hook — conflict, question, counterintuitive result, or real experiment.
2. Common belief — what viewers usually assume.
3. Doubt — the missing variable or weakness in that assumption.
4. Verification — real data, historical case, or live/account evidence.
5. Key result — only the numbers needed to answer the question.
6. Plain-language explanation — explain first, then name the technical term.
7. Boundary conditions — where the conclusion does and does not apply.
8. Reusable judgment method — what the viewer should check next time.

The structure may be adapted for source-led, localization, or clip-selection
pipelines, but the four requirements remain binding: evidence before conclusion,
one core question, plain-language explanation, and a reusable judgment method.

Writing rules:

- Sound like a rational, data-minded friend, with light natural wit where it
  fits. Avoid classroom scaffolding such as “first, second, finally”.
- Translate terms such as drawdown, ex-dividend, valuation, volatility, and
  capital gain immediately into ordinary language or a concrete analogy.
- Each chart and number must answer an explicit question and move the reasoning
  forward. Remove decorative statistics.
- State probabilistic claims probabilistically. Include assumptions and scope.
  Do not use unsupported absolutes such as “一定”, “必赚”, “稳赚”, “千万别买”,
  “90%的人都会”, or “XX就是骗局”.
- End the editorial content with a method the viewer can reuse, not merely the
  creator's opinion.

For auditability, record these values under `script.metadata.finance_editorial`:

```json
{
  "core_question": "The single question this video answers",
  "evidence_refs": ["research_brief.data_points[0]"],
  "boundary_conditions": ["The scope or condition that limits the result"],
  "reusable_judgment_method": "What viewers should check next time"
}
```

After the reusable judgment method, append the mandatory disclaimer as its own
final script section, exactly as defined in `AGENT_GUIDE.md`. The disclaimer is
compliance copy, not a substitute for boundary conditions.

### Scene Plan / Assets / Edit

- Give every chart, table, stat card, or comparison one declared question it
  answers and link it to the supporting source reference.
- Render precision-critical numbers, labels, dates, and charts natively in the
  composition. Never rely on AI-generated imagery to reproduce financial data.
- Preserve units, baselines, time ranges, axes, and comparison definitions.
  Avoid truncated axes or visual scale choices that exaggerate the conclusion.
- Remove any visual or number that does not advance the core question.
- Keep the reusable judgment method as the final editorial beat, followed only
  by the mandatory exact-text disclaimer card.

### Compose / Publish

- Inspect the rendered numbers and charts against their source values.
- Confirm qualifications and boundary conditions remain readable and are not
  rushed by pacing or obscured by captions.
- Do not turn a qualified script into an absolute title, cover, caption, or
  description. The publishing hook may be sharp, but it may not overstate the
  evidence.
- Apply the existing financial disclaimer end-card verification without change.

## Finance Review Gate

For `content_category: finance`, the reviewer treats any failure of the four
iron rules as critical and proposes a concrete fix:

1. Evidence was selected to prove a predetermined conclusion.
2. A hook or claim sacrifices factual accuracy for impact.
3. Specialist language is left unexplained for ordinary viewers.
4. The video gives an answer but no reusable judgment method.

Also verify:

- the first 10 seconds creates a genuine “what happens next?” question;
- the whole piece answers one core question;
- every material claim has a traceable evidence reference;
- every number or chart advances the reasoning;
- probability and boundary conditions are stated honestly;
- `script.metadata.finance_editorial` records the question, evidence,
  boundaries, and method;
- the mandatory exact disclaimer remains the final item at every required
  downstream stage.

For non-finance productions this entire review gate is skipped.
