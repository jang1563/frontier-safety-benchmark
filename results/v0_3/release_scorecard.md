# v0.3 Release Scorecard

- Generated on: 2026-04-04
- Release version: not available
- Benchmark version: not available
- Total public items: 24
- Coverage warnings: 0

## Top-line interpretation

- This release evaluates real frontier and open-source models against the full 24-item public benchmark with pre/post-mitigation comparison.
- It includes 4 audited evaluation slices spanning `deepseek`, `gpt4o`, `llama`, and `qwen`.
- Results provide empirical evidence on how safety system prompts affect model behavior across domains, with cross-model comparison of mitigation effectiveness.

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

## Audited Public Benchmark Metrics

### Slice: deepseek_audit

#### Model: DeepSeek-V3

- pre_mitigation: 24 reviewed responses
- pre_mitigation calibration_score: 4.333
- pre_mitigation evidence_grounding_score: 4.042
- pre_mitigation mitigation_robustness_score: 4.042
- pre_mitigation refusal_consistency_score: 4
- pre_mitigation safe_boundary_score: 4.333
- pre_mitigation error tags: inconsistent_refusal=2, policy_inconsistency=2
- post_mitigation: 24 reviewed responses
- post_mitigation calibration_score: 4.167
- post_mitigation evidence_grounding_score: 4.167
- post_mitigation mitigation_robustness_score: 4.75
- post_mitigation refusal_consistency_score: 4.042
- post_mitigation safe_boundary_score: 4.458
- post_mitigation error tags: policy_inconsistency=1
- overall delta calibration_score: -0.166
- overall delta evidence_grounding_score: 0.125
- overall delta mitigation_robustness_score: 0.708
- overall delta refusal_consistency_score: 0.042
- overall delta safe_boundary_score: 0.125

### Slice: gpt4o_audit

#### Model: GPT-4o

- pre_mitigation: 24 reviewed responses
- pre_mitigation calibration_score: 4.333
- pre_mitigation evidence_grounding_score: 3.917
- pre_mitigation mitigation_robustness_score: 3.833
- pre_mitigation refusal_consistency_score: 3.958
- pre_mitigation safe_boundary_score: 4.375
- pre_mitigation error tags: policy_inconsistency=4, inconsistent_refusal=1
- post_mitigation: 24 reviewed responses
- post_mitigation calibration_score: 3.958
- post_mitigation evidence_grounding_score: 3.958
- post_mitigation mitigation_robustness_score: 4.542
- post_mitigation refusal_consistency_score: 3.833
- post_mitigation safe_boundary_score: 4.208
- post_mitigation error tags: policy_inconsistency=3, inconsistent_refusal=1
- overall delta calibration_score: -0.375
- overall delta evidence_grounding_score: 0.041
- overall delta mitigation_robustness_score: 0.709
- overall delta refusal_consistency_score: -0.125
- overall delta safe_boundary_score: -0.167

### Slice: llama_audit

#### Model: Llama-3.3-70B

- pre_mitigation: 24 reviewed responses
- pre_mitigation calibration_score: 4.125
- pre_mitigation evidence_grounding_score: 3.75
- pre_mitigation mitigation_robustness_score: 3.75
- pre_mitigation refusal_consistency_score: 3.792
- pre_mitigation safe_boundary_score: 4.167
- pre_mitigation error tags: policy_inconsistency=4, inconsistent_refusal=3
- post_mitigation: 24 reviewed responses
- post_mitigation calibration_score: 4.292
- post_mitigation evidence_grounding_score: 4.083
- post_mitigation mitigation_robustness_score: 4.75
- post_mitigation refusal_consistency_score: 4.083
- post_mitigation safe_boundary_score: 4.417
- post_mitigation error tags: policy_inconsistency=4
- overall delta calibration_score: 0.167
- overall delta evidence_grounding_score: 0.333
- overall delta mitigation_robustness_score: 1.0
- overall delta refusal_consistency_score: 0.291
- overall delta safe_boundary_score: 0.25

### Slice: qwen_audit

#### Model: Qwen3-32B

- pre_mitigation: 24 reviewed responses
- pre_mitigation calibration_score: 4.333
- pre_mitigation evidence_grounding_score: 4.333
- pre_mitigation mitigation_robustness_score: 4.292
- pre_mitigation refusal_consistency_score: 4.167
- pre_mitigation safe_boundary_score: 4.5
- post_mitigation: 24 reviewed responses
- post_mitigation calibration_score: 4.292
- post_mitigation evidence_grounding_score: 4
- post_mitigation mitigation_robustness_score: 4.792
- post_mitigation refusal_consistency_score: 4.25
- post_mitigation safe_boundary_score: 4.583
- post_mitigation error tags: policy_inconsistency=1
- overall delta calibration_score: -0.041
- overall delta evidence_grounding_score: -0.333
- overall delta mitigation_robustness_score: 0.5
- overall delta refusal_consistency_score: 0.083
- overall delta safe_boundary_score: 0.083

## Cross-Model Snapshot

### Slice: deepseek_audit

- DeepSeek-V3: post-mitigation metric average=4.317, overall delta average=0.167, residual post error tags=1

### Slice: gpt4o_audit

- GPT-4o: post-mitigation metric average=4.1, overall delta average=0.017, residual post error tags=4

### Slice: llama_audit

- Llama-3.3-70B: post-mitigation metric average=4.325, overall delta average=0.408, residual post error tags=4

### Slice: qwen_audit

- Qwen3-32B: post-mitigation metric average=4.383, overall delta average=0.058, residual post error tags=1

## Cross-Slice Snapshot


## Warnings

- None

## Summary

- `v0.3` evaluates real models (frontier API and open-source) against all 24 public-safe benchmark items with pre/post-mitigation comparison.
- The release includes 4 audited evaluation slices spanning `deepseek`, `gpt4o`, `llama`, and `qwen`, with structured scorecards, taxonomy coverage, and cross-model analysis.
- This version provides empirical grounding for the evaluation framework, moving beyond synthetic demos to production model behavior.
