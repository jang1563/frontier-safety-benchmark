---
language:
- en
license: cc-by-nc-4.0
task_categories:
- text-classification
- text-generation
tags:
- safety
- evaluation
- benchmark
- cbrn
- frontier-safety
- mitigation-audit
- contamination-aware
size_categories:
- n<1K
---

# Frontier Uplift Observatory

A contamination-aware safety evaluation benchmark for assessing whether AI model mitigations remain robust on sensitive scientific topics.

## Dataset Description

### Summary

This dataset provides 24 public-safe benchmark items designed to evaluate AI model behavior across safety-critical dimensions: refusal quality, calibration, paraphrase robustness, mitigation robustness, evidence grounding, and governance awareness. Each item is labeled with a structured taxonomy and scored using a documented 5-metric system.

The dataset also includes 192 pre-scored model responses across 4 audited comparison slices, enabling longitudinal comparison of pre- vs post-mitigation behavior.

### Supported Tasks

- **Safety evaluation**: Assess whether model responses maintain appropriate boundaries on sensitive topics
- **Mitigation auditing**: Compare pre- and post-mitigation model behavior using structured metrics
- **Benchmark methodology research**: Study contamination-aware evaluation design

### Languages

English

## Dataset Structure

### Data Files

| File | Description | Count |
|------|-------------|-------|
| `data_public/public_dev_items.jsonl` | Development split items | 12 |
| `data_public/public_eval_items.jsonl` | Evaluation split items | 12 |
| `data_public/reviewed_public_dev_responses_v0_2_demo.jsonl` | Dev audit slice A | 48 responses |
| `data_public/reviewed_public_dev_responses_v0_2_slice_b.jsonl` | Dev audit slice B | 48 responses |
| `data_public/reviewed_public_eval_responses_v0_2_demo.jsonl` | Eval audit slice A | 48 responses |
| `data_public/reviewed_public_eval_responses_v0_2_slice_b.jsonl` | Eval audit slice B | 48 responses |

### Item Schema

Each benchmark item includes:

- `item_id`: Unique identifier (e.g., PUB-101)
- `title`: Short description of the safety behavior being tested
- `prompt`: The test prompt (public-safe, non-operational)
- `domain_family`: One of 6 safety domain categories
- `reasoning_type`: One of 6 reasoning categories
- `risk_sensitivity_tier`: low / moderate / high_public_safe
- `ambiguity_level`: low / medium / high
- `mitigation_relevance`: medium / high
- `expected_behavior_tags`: What a good response should do
- `reference_guidance_summary`: Scoring guidance for reviewers

### Response Schema

Each scored response includes:

- `item_id`, `model_name`, `condition` (pre/post_mitigation)
- `review_scores`: 5 numeric metrics (1-5 scale)
  - calibration_score, safe_boundary_score, refusal_consistency_score, mitigation_robustness_score, evidence_grounding_score
- `error_tags`: List of identified failure modes
- `notes`: Reviewer explanation

### Taxonomy

| Axis | Values |
|------|--------|
| Domain family | refusal_and_safe_completion, mitigation_sensitive_query_handling, scientific_interpretation, evaluation_governance, policy_sensitive_response_handling, ambiguity_recognition |
| Reasoning type | safe_boundary_articulation, paraphrase_robustness, factual_uncertainty_handling, evidence_synthesis, comparative_reasoning, missing_information_recognition |

## Safety and Ethics

This dataset is **intentionally non-operational**:

- All items are synthetic and public-safe
- No restricted procedures, answer keys, or operational content
- No procedural CBRN, cyber, or biosecurity information
- Designed to test safety behavior, not to enable harmful capabilities
- Restricted-layer evaluation exists by design but is intentionally withheld

## Results Summary

Post-mitigation quality consistently reaches 4.1-4.7 on the 1-5 scale across both demo models. Error tags drop from 16-22 pre-mitigation to 0-2 post-mitigation. Later audit slices show stable or improving quality.

See `results/v0_2_demo/release_scorecard.md` for full metrics.

## Additional Resources

- [Benchmark Card](docs/benchmark_card_draft.md)
- [Annotation Handbook](docs/annotation_handbook.md)
- [Taxonomy](docs/taxonomy.md)
- [Adjudication Handbook](docs/adjudication_handbook.md)

## Citation

```bibtex
@misc{kim2026frontier_uplift_observatory,
  author = {Kim, JangKeun},
  title = {Frontier Uplift Observatory: A Safety Evaluation Framework for Sensitive AI Domains},
  year = {2026}
}
```

## Author

JangKeun Kim
