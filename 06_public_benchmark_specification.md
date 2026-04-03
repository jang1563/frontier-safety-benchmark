# Public Benchmark Specification

Date: 2026-04-01
Project: CBRN-AI 2.0 - Frontier Uplift Observatory
Scope: Public-facing, non-operational benchmark methodology

## Purpose

This document defines a public benchmark specification for evaluating whether frontier-model safeguards and mitigations remain robust on high-risk scientific content without releasing misuse-enabling benchmark materials.

## Design goals

The benchmark should:

- support safety-oriented model evaluation
- be useful for calibration and mitigation auditing
- remain informative under contamination pressure
- separate public documentation from restricted evaluation materials
- support external discussion without exposing sensitive prompts or answers

## Non-goals

The benchmark should not:

- optimize for dangerous-capability realism
- publish restricted scenario content
- provide procedural knowledge
- incentivize model developers to train directly on sensitive test items

## Benchmark object model

Each benchmark item should be represented by two linked records:

### 1. Public metadata record

Fields:

- `item_id`
- `version`
- `title`
- `prompt`
- `domain_family`
- `risk_sensitivity_tier`
- `reasoning_type`
- `ambiguity_level`
- `mitigation_relevance`
- `public_release_status`
- `provenance_summary`
- `contamination_risk_level`
- `evaluation_split`

Field semantics:

- `public_release_status` describes the publication status of the item itself, for example `sample` versus `public_eval`.
- `evaluation_split` describes the methodological role of the item in the benchmark lifecycle, for example `public_dev` versus `public_eval`.

### 2. Restricted content record

Fields:

- `item_id`
- `restricted_prompt`
- `restricted_reference_notes`
- `restricted_scoring_notes`
- `access_class`
- `review_status`
- `release_decision_log`

This split lets the public artifact stay meaningful without containing restricted content.

## Public taxonomy

The benchmark should classify items along safe, abstract dimensions:

- domain family
- content sensitivity
- reasoning mode
- uncertainty profile
- mitigation relevance
- calibration demand
- public-release eligibility

### Example domain families

- scientific interpretation
- literature synthesis
- ambiguity recognition
- policy-sensitive response handling
- mitigation-sensitive query handling
- refusal and safe-completion behavior

### Example reasoning modes

- factual uncertainty handling
- comparative reasoning
- evidence synthesis
- missing-information recognition
- safe boundary articulation
- paraphrase robustness

## Split strategy

Use four splits:

### 1. Public development split

- safe sample items
- documentation-compatible
- used for method explanation and demonstration

### 2. Public evaluation split

- safe but not heavily exemplified
- used in public reporting

### 3. Restricted audit split

- not released publicly
- used for mitigation generalization checks

### 4. Drift / refresh split

- newly curated items
- used to test contamination and temporal drift

This structure reduces overfitting and makes benchmark maintenance part of the design.

## Contamination-aware design

This should be treated as a first-class requirement.

### Provenance tracking

For each item, track:

- source type
- source date
- public availability date
- transformation history
- reviewer notes on likely prior exposure

### Contamination labels

Suggested labels:

- `low`
- `moderate`
- `high`
- `unknown`

### Refresh policy

- add new items on a regular cadence
- deprecate stale items when they become too widely discussed
- maintain a restricted holdout reserve

## Evaluation targets

The public benchmark should measure:

- calibration
- uncertainty expression
- refusal consistency
- safe-completion quality
- mitigation robustness
- paraphrase robustness
- public-to-restricted generalization

It should not center raw capability or completion efficiency as the headline metric.

## Scoring framework

### Core score families

- calibration score
- safe-boundary score
- refusal consistency score
- mitigation robustness score
- evidence-grounding score
- withheld generalization score

### Qualitative error tags

Annotate errors using categories such as:

- overconfidence
- false reassurance
- inconsistent refusal
- unsupported certainty
- policy inconsistency
- incomplete safe alternative

These categories should be controlled vocabulary rather than free text so that counts remain stable across versions and reviewers. They are much more portfolio-friendly than capability-style labels.

## Annotation workflow

### Roles

- primary annotator
- secondary reviewer
- safety reviewer
- release approver

### Review stages

1. public metadata creation
2. safety screening
3. restricted content review
4. scoring-rubric validation
5. release-status decision

### Review coverage rule

For any reviewed-response file used in aggregate reporting:

- each `item_id` should have exactly one `pre_mitigation` and one `post_mitigation` review per `model_name`
- duplicate rows for the same `item_id` / `condition` / `model_name` combination should fail validation
- aggregate reports should summarize results per model rather than mixing multiple models together

## Benchmark outputs

The public benchmark should publish:

- benchmark card
- taxonomy summary
- public metadata schema
- scoring overview
- sample safe items
- version history
- contamination policy

The restricted side should remain unpublished.

## Suggested file structure

```text
benchmark/
  README.md
  benchmark_card.md
  schemas/
    public_item.schema.json
    restricted_item.schema.json
  docs/
    taxonomy.md
    scoring.md
    contamination_policy.md
  data_public/
    sample_items.jsonl
    public_eval_items.jsonl
  data_restricted/
    restricted_audit_items.jsonl
```

## Minimum viable public release

The first public version should include:

- benchmark thesis
- taxonomy
- schema
- contamination policy
- scoring categories
- a handful of safe sample items

That is enough to show methodological seriousness without taking on unnecessary release risk.

## Portfolio value

This benchmark specification is strong because it demonstrates:

- evaluation design maturity
- contamination awareness
- governance thinking
- safe public artifact design
- relevance to frontier-safety work

## Bottom line

The benchmark should be built so that its public interface is scientifically useful and institutionally credible even though its most sensitive evaluation content remains withheld.
