# v0.2 Demo Release Scorecard

- Generated on: 2026-04-03
- Release version: v0.2.0-demo
- Benchmark version: 0.2.0-draft
- Total public items: 24
- Coverage warnings: 0

## Top-line interpretation

- This demo package shows benchmark breadth, taxonomy balance, and release hygiene for the public-safe layer.
- It combines structural release signals with 4 audited release slices spanning `public_dev` and `public_eval`.
- The strongest current signal is that the package now has balanced public splits, explicit taxonomy, reproducible metadata, and an empirical mitigation-audit comparison layer.

## By Split

- public_dev: 12
- public_eval: 12

## By Domain Family

- ambiguity_recognition: 4
- evaluation_governance: 4
- mitigation_sensitive_query_handling: 4
- policy_sensitive_response_handling: 4
- refusal_and_safe_completion: 4
- scientific_interpretation: 4

## By Reasoning Type

- comparative_reasoning: 4
- evidence_synthesis: 6
- factual_uncertainty_handling: 3
- missing_information_recognition: 3
- paraphrase_robustness: 4
- safe_boundary_articulation: 4

## By Mitigation Relevance

- high: 15
- medium: 9

## By Ambiguity Level

- high: 12
- low: 2
- medium: 10

## Release Manifest Artifact Types

- documentation: 5
- input: 6
- metadata: 5
- output: 21

## Audited Public Benchmark Metrics

### Slice: public_dev_audit

#### Model: demo-model-v0.2

- pre_mitigation: 12 reviewed responses
- pre_mitigation calibration_score: 2.333
- pre_mitigation evidence_grounding_score: 2.083
- pre_mitigation mitigation_robustness_score: 2.083
- pre_mitigation refusal_consistency_score: 3.5
- pre_mitigation safe_boundary_score: 3.583
- pre_mitigation error tags: incomplete_safe_alternative=4, unsupported_certainty=4, inconsistent_refusal=3, policy_inconsistency=3, overconfidence=2, false_reassurance=2
- post_mitigation: 12 reviewed responses
- post_mitigation calibration_score: 4.833
- post_mitigation evidence_grounding_score: 4.583
- post_mitigation mitigation_robustness_score: 4.667
- post_mitigation refusal_consistency_score: 4.583
- post_mitigation safe_boundary_score: 4.583
- overall delta calibration_score: 2.5
- overall delta evidence_grounding_score: 2.5
- overall delta mitigation_robustness_score: 2.584
- overall delta refusal_consistency_score: 1.083
- overall delta safe_boundary_score: 1.0

#### Model: strict-model-v0.2

- pre_mitigation: 12 reviewed responses
- pre_mitigation calibration_score: 2.333
- pre_mitigation evidence_grounding_score: 2.083
- pre_mitigation mitigation_robustness_score: 2.25
- pre_mitigation refusal_consistency_score: 3.5
- pre_mitigation safe_boundary_score: 3.75
- pre_mitigation error tags: unsupported_certainty=4, incomplete_safe_alternative=3, inconsistent_refusal=3, policy_inconsistency=3, false_reassurance=2, overconfidence=1
- post_mitigation: 12 reviewed responses
- post_mitigation calibration_score: 4
- post_mitigation evidence_grounding_score: 3.667
- post_mitigation mitigation_robustness_score: 3.75
- post_mitigation refusal_consistency_score: 4.583
- post_mitigation safe_boundary_score: 4.583
- post_mitigation error tags: incomplete_safe_alternative=1
- overall delta calibration_score: 1.667
- overall delta evidence_grounding_score: 1.584
- overall delta mitigation_robustness_score: 1.5
- overall delta refusal_consistency_score: 1.083
- overall delta safe_boundary_score: 0.833

### Slice: public_dev_audit_slice_b

#### Model: demo-model-v0.2

- pre_mitigation: 12 reviewed responses
- pre_mitigation calibration_score: 3.167
- pre_mitigation evidence_grounding_score: 3.083
- pre_mitigation mitigation_robustness_score: 3.167
- pre_mitigation refusal_consistency_score: 4.167
- pre_mitigation safe_boundary_score: 4.167
- post_mitigation: 12 reviewed responses
- post_mitigation calibration_score: 4.917
- post_mitigation evidence_grounding_score: 4.667
- post_mitigation mitigation_robustness_score: 4.667
- post_mitigation refusal_consistency_score: 4.583
- post_mitigation safe_boundary_score: 4.583
- overall delta calibration_score: 1.75
- overall delta evidence_grounding_score: 1.584
- overall delta mitigation_robustness_score: 1.5
- overall delta refusal_consistency_score: 0.416
- overall delta safe_boundary_score: 0.416

#### Model: strict-model-v0.2

- pre_mitigation: 12 reviewed responses
- pre_mitigation calibration_score: 3
- pre_mitigation evidence_grounding_score: 2.917
- pre_mitigation mitigation_robustness_score: 3
- pre_mitigation refusal_consistency_score: 4.25
- pre_mitigation safe_boundary_score: 4.25
- pre_mitigation error tags: incomplete_safe_alternative=1
- post_mitigation: 12 reviewed responses
- post_mitigation calibration_score: 4
- post_mitigation evidence_grounding_score: 4
- post_mitigation mitigation_robustness_score: 4
- post_mitigation refusal_consistency_score: 4.583
- post_mitigation safe_boundary_score: 4.583
- overall delta calibration_score: 1
- overall delta evidence_grounding_score: 1.083
- overall delta mitigation_robustness_score: 1
- overall delta refusal_consistency_score: 0.333
- overall delta safe_boundary_score: 0.333

### Slice: public_eval_audit

#### Model: demo-model-v0.2

- pre_mitigation: 12 reviewed responses
- pre_mitigation calibration_score: 2
- pre_mitigation evidence_grounding_score: 1.667
- pre_mitigation mitigation_robustness_score: 2
- pre_mitigation refusal_consistency_score: 3.5
- pre_mitigation safe_boundary_score: 3.5
- pre_mitigation error tags: incomplete_safe_alternative=4, policy_inconsistency=4, overconfidence=4, unsupported_certainty=4, inconsistent_refusal=3, false_reassurance=3
- post_mitigation: 12 reviewed responses
- post_mitigation calibration_score: 4.75
- post_mitigation evidence_grounding_score: 4.583
- post_mitigation mitigation_robustness_score: 4.667
- post_mitigation refusal_consistency_score: 4.583
- post_mitigation safe_boundary_score: 4.583
- overall delta calibration_score: 2.75
- overall delta evidence_grounding_score: 2.916
- overall delta mitigation_robustness_score: 2.667
- overall delta refusal_consistency_score: 1.083
- overall delta safe_boundary_score: 1.083

#### Model: strict-model-v0.2

- pre_mitigation: 12 reviewed responses
- pre_mitigation calibration_score: 2.25
- pre_mitigation evidence_grounding_score: 1.917
- pre_mitigation mitigation_robustness_score: 2.083
- pre_mitigation refusal_consistency_score: 3.583
- pre_mitigation safe_boundary_score: 3.667
- pre_mitigation error tags: policy_inconsistency=4, unsupported_certainty=4, incomplete_safe_alternative=3, inconsistent_refusal=3, overconfidence=2, false_reassurance=2
- post_mitigation: 12 reviewed responses
- post_mitigation calibration_score: 4
- post_mitigation evidence_grounding_score: 3.667
- post_mitigation mitigation_robustness_score: 3.75
- post_mitigation refusal_consistency_score: 4.583
- post_mitigation safe_boundary_score: 4.583
- post_mitigation error tags: incomplete_safe_alternative=2
- overall delta calibration_score: 1.75
- overall delta evidence_grounding_score: 1.75
- overall delta mitigation_robustness_score: 1.667
- overall delta refusal_consistency_score: 1.0
- overall delta safe_boundary_score: 0.916

### Slice: public_eval_audit_slice_b

#### Model: demo-model-v0.2

- pre_mitigation: 12 reviewed responses
- pre_mitigation calibration_score: 3.167
- pre_mitigation evidence_grounding_score: 3.083
- pre_mitigation mitigation_robustness_score: 3.167
- pre_mitigation refusal_consistency_score: 4.167
- pre_mitigation safe_boundary_score: 4.167
- post_mitigation: 12 reviewed responses
- post_mitigation calibration_score: 5
- post_mitigation evidence_grounding_score: 4.667
- post_mitigation mitigation_robustness_score: 4.667
- post_mitigation refusal_consistency_score: 4.583
- post_mitigation safe_boundary_score: 4.583
- overall delta calibration_score: 1.833
- overall delta evidence_grounding_score: 1.584
- overall delta mitigation_robustness_score: 1.5
- overall delta refusal_consistency_score: 0.416
- overall delta safe_boundary_score: 0.416

#### Model: strict-model-v0.2

- pre_mitigation: 12 reviewed responses
- pre_mitigation calibration_score: 3
- pre_mitigation evidence_grounding_score: 2.917
- pre_mitigation mitigation_robustness_score: 3
- pre_mitigation refusal_consistency_score: 4.25
- pre_mitigation safe_boundary_score: 4.25
- pre_mitigation error tags: incomplete_safe_alternative=1
- post_mitigation: 12 reviewed responses
- post_mitigation calibration_score: 4
- post_mitigation evidence_grounding_score: 4
- post_mitigation mitigation_robustness_score: 4
- post_mitigation refusal_consistency_score: 4.583
- post_mitigation safe_boundary_score: 4.583
- overall delta calibration_score: 1
- overall delta evidence_grounding_score: 1.083
- overall delta mitigation_robustness_score: 1
- overall delta refusal_consistency_score: 0.333
- overall delta safe_boundary_score: 0.333

## Cross-Model Snapshot

### Slice: public_dev_audit

- demo-model-v0.2: post-mitigation metric average=4.65, overall delta average=1.933, residual post error tags=0
- strict-model-v0.2: post-mitigation metric average=4.117, overall delta average=1.333, residual post error tags=1

### Slice: public_dev_audit_slice_b

- demo-model-v0.2: post-mitigation metric average=4.683, overall delta average=1.133, residual post error tags=0
- strict-model-v0.2: post-mitigation metric average=4.233, overall delta average=0.75, residual post error tags=0

### Slice: public_eval_audit

- demo-model-v0.2: post-mitigation metric average=4.633, overall delta average=2.1, residual post error tags=0
- strict-model-v0.2: post-mitigation metric average=4.117, overall delta average=1.417, residual post error tags=2

### Slice: public_eval_audit_slice_b

- demo-model-v0.2: post-mitigation metric average=4.7, overall delta average=1.15, residual post error tags=0
- strict-model-v0.2: post-mitigation metric average=4.233, overall delta average=0.75, residual post error tags=0

## Cross-Slice Snapshot

### Scope: public_dev

- demo-model-v0.2: public_dev_audit: post avg=4.65, delta avg=1.933, post error tags=0; public_dev_audit_slice_b: post avg=4.683, delta avg=1.133, post error tags=0
- strict-model-v0.2: public_dev_audit: post avg=4.117, delta avg=1.333, post error tags=1; public_dev_audit_slice_b: post avg=4.233, delta avg=0.75, post error tags=0

### Scope: public_eval

- demo-model-v0.2: public_eval_audit: post avg=4.633, delta avg=2.1, post error tags=0; public_eval_audit_slice_b: post avg=4.7, delta avg=1.15, post error tags=0
- strict-model-v0.2: public_eval_audit: post avg=4.117, delta avg=1.417, post error tags=2; public_eval_audit_slice_b: post avg=4.233, delta avg=0.75, post error tags=0


## Warnings

- None

## Interview-ready summary

- `v0.2` expands the public-safe benchmark to 24 items with a balanced `public_dev` / `public_eval` split.
- The package now includes taxonomy and annotation docs, release metadata, coverage reporting, structured scorecards, and 4 audited release slices spanning `public_dev` and `public_eval`.
- The next credibility step is to add a refreshed benchmark version or external reviewer pass so the public audit layer supports stronger generalization claims rather than only internal synthetic demos.
