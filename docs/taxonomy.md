# Taxonomy

Project: CBRN-AI 2.0 - Frontier Uplift Observatory
Version: v0.2 draft
Date: 2026-04-01
Scope: Public-facing, non-operational taxonomy for benchmark organization and reporting

## Purpose

This taxonomy defines the labeling system used for the public benchmark items in CBRN-AI 2.0. Its purpose is to make benchmark coverage legible, keep annotation decisions consistent, and support release notes and coverage reporting.

The taxonomy is intentionally compact. It is designed to organize safe public evaluation work, not to create fine-grained operational categories for restricted content.

## Design principles

The taxonomy should:

- stay understandable to external reviewers
- support balanced benchmark coverage
- help annotation and release workflows stay consistent
- avoid unnecessary category proliferation

The taxonomy should not:

- become a substitute for full benchmark documentation
- encode sensitive scenario details
- grow faster than reviewer reliability

## Axes used in v0.2

Each public item is labeled across the following axes:

- `domain_family`
- `reasoning_type`
- `risk_sensitivity_tier`
- `ambiguity_level`
- `mitigation_relevance`
- `public_release_status`
- `evaluation_split`

## 1. Domain Family

`domain_family` describes the main kind of safety-relevant task the item is evaluating. Assign the label based on the dominant evaluation question, not every property the item happens to touch.

### `refusal_and_safe_completion`

Use when the main question is whether the model sets an appropriate boundary and still provides a bounded, legitimate alternative.

Typical behaviors assessed:

- direct refusal quality
- follow-up refusal consistency
- safe alternative framing

Current examples:

- `PUB-101`
- `PUB-107`
- `PUB-201`
- `PUB-207`

### `mitigation_sensitive_query_handling`

Use when the item tests whether mitigations remain stable under paraphrase, euphemism, framing shifts, or indirect intent.

Typical behaviors assessed:

- paraphrase robustness
- sensitivity to loophole framing
- resistance to benign-intent laundering

Current examples:

- `PUB-102`
- `PUB-111`
- `PUB-202`
- `PUB-211`

### `scientific_interpretation`

Use when the item centers on interpreting sensitive scientific claims without drifting into overconfidence, sensationalism, or ungrounded conclusions.

Typical behaviors assessed:

- evidence weighting
- calibrated interpretation
- conflict resolution across sources

Current examples:

- `PUB-103`
- `PUB-108`
- `PUB-203`
- `PUB-208`

### `evaluation_governance`

Use when the item tests whether the model can explain public benchmark design, release controls, contamination logic, or governance choices clearly and accurately.

Typical behaviors assessed:

- governance explanation quality
- benchmark integrity reasoning
- release-architecture literacy

Current examples:

- `PUB-104`
- `PUB-109`
- `PUB-204`
- `PUB-209`

### `policy_sensitive_response_handling`

Use when the item focuses on explaining or applying high-level safety policy logic, especially around why certain responses are appropriate or inappropriate.

Typical behaviors assessed:

- policy-legible explanation
- distinction between refusal and safety
- stable explanation under pressure or appeals to intent

Current examples:

- `PUB-105`
- `PUB-110`
- `PUB-205`
- `PUB-210`

### `ambiguity_recognition`

Use when the item primarily tests whether the model recognizes that the available information is insufficient and responds by staying bounded rather than overclaiming.

Typical behaviors assessed:

- missing-information recognition
- bounded clarification
- calibrated incompleteness

Current examples:

- `PUB-106`
- `PUB-112`
- `PUB-206`
- `PUB-212`

## 2. Reasoning Type

`reasoning_type` captures the dominant reasoning move required for a good answer.

### `safe_boundary_articulation`

Use when the best response depends on setting a clear limit, explaining it briefly, and staying helpful without leaking detail.

Best fit:

- direct refusals
- repeated refusals
- narrowing attempts after refusal

### `paraphrase_robustness`

Use when the main challenge is recognizing a risky request despite wording shifts, euphemism, role-play framing, or indirect language.

Best fit:

- phrasing changes
- intent laundering
- framing-based loophole attempts

### `factual_uncertainty_handling`

Use when the item asks the model to avoid overclaiming from incomplete, novel, or conflicting evidence.

Best fit:

- alarming single-source claims
- under-specified safety claims
- uncertain public scientific evidence

### `evidence_synthesis`

Use when the best answer requires summarizing, comparing, or integrating multiple high-level sources or considerations.

Best fit:

- governance reading lists
- conflicting reports
- high-level policy explanation grounded in multiple factors

### `comparative_reasoning`

Use when the item asks the model to compare approaches, explain tradeoffs, or distinguish two related safety concepts.

Best fit:

- refusal vs safe completion
- public vs withheld benchmark layers
- why refresh cycles matter

### `missing_information_recognition`

Use when the correct move is to identify what is missing before a responsible judgment could be made.

Best fit:

- underspecified sensitivity questions
- vague safety-failure claims
- incomplete context on potentially risky topics

## 3. Risk Sensitivity Tier

`risk_sensitivity_tier` describes how sensitive the public item is, even in its abstracted form.

### `low`

Use for clearly governance-oriented or meta-evaluation items with minimal sensitivity.

Typical examples:

- governance explanations
- benchmark design rationale

### `moderate`

Use for public-safe items that still touch sensitive scientific or safety-adjacent material and therefore require calibrated wording.

Typical examples:

- uncertain scientific claims
- safety-policy explanation questions

### `high_public_safe`

Use for public-safe abstractions of clearly sensitive request types. These items remain non-operational, but the benchmark should treat them with extra care in review and release.

Typical examples:

- refusal items
- paraphrased sensitive request items

## 4. Ambiguity Level

`ambiguity_level` estimates how much uncertainty the item intentionally introduces.

### `low`

The safety boundary is direct and obvious. The item mostly tests execution quality rather than interpretive ambiguity.

### `medium`

The item involves some interpretation or tradeoff, but a well-calibrated answer should still be relatively stable across reviewers.

### `high`

The item intentionally tests uncertainty handling, missing-context recognition, or reasoning under incomplete evidence.

## 5. Mitigation Relevance

`mitigation_relevance` describes how directly the item informs mitigation auditing.

### `low`

Reserve for future cases where an item is mostly descriptive and only weakly useful for comparing mitigation conditions.

This level is not currently used in the v0.2 public split.

### `medium`

Use when the item helps assess general calibration, evidence handling, or bounded reasoning, but is not mainly about boundary robustness.

### `high`

Use when the item is directly useful for testing whether mitigations hold under sensitive requests, paraphrases, policy pressure, or safe-completion tradeoffs.

## 6. Public Release Status

`public_release_status` describes how the item is released to the public.

### `sample`

Use for documentation-compatible items that can appear as public examples or development references.

### `public_eval`

Use for items that are still public-safe but belong to the released evaluation set rather than the smaller sample/demo layer.

## 7. Evaluation Split

`evaluation_split` describes the methodological role of the item.

### `public_dev`

Use for items intended for method explanation, sample demonstrations, or development-facing examples.

### `public_eval`

Use for items intended to support released evaluation summaries or scorecards.

### `drift_refresh`

Reserved for future refresh items added to monitor drift, contamination pressure, or benchmark aging.

## 8. How to resolve borderline cases

### Domain-family tie-break rule

If an item could fit more than one domain family, choose the label based on the main question being scored.

Examples:

- If the core question is "does the model keep the boundary under paraphrase," use `mitigation_sensitive_query_handling` even if the response also includes refusal.
- If the core question is "does the model explain why the benchmark is designed this way," use `evaluation_governance` even if the answer mentions mitigations.

### Reasoning-type tie-break rule

Choose the dominant reasoning move required for a strong answer.

Examples:

- If the response needs both uncertainty and comparison, choose the one that most determines whether the answer is good.
- If the item is only secondarily comparative but mainly about recognizing insufficient context, use `missing_information_recognition`.

## 9. Current v0.2 coverage snapshot

The current v0.2 public set contains 24 items:

- 12 `public_dev`
- 12 `public_eval`

Current domain-family distribution:

- `ambiguity_recognition`: 4
- `evaluation_governance`: 4
- `mitigation_sensitive_query_handling`: 4
- `policy_sensitive_response_handling`: 4
- `refusal_and_safe_completion`: 4
- `scientific_interpretation`: 4

Current reasoning-type distribution:

- `comparative_reasoning`: 4
- `evidence_synthesis`: 6
- `factual_uncertainty_handling`: 3
- `missing_information_recognition`: 3
- `paraphrase_robustness`: 4
- `safe_boundary_articulation`: 4

## 10. Change policy

Taxonomy changes should be rare and explicit. If the taxonomy changes:

- update the schemas if needed
- update this document
- note the change in release logs
- explain any remapping of old labels

The goal is to keep benchmark history interpretable across versions.
