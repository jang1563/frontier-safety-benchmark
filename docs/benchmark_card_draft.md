# Benchmark Card Draft

Project: CBRN-AI 2.0 - Frontier Uplift Observatory
Version: 0.2.0-demo
Release date: 2026-04-02
Maintainer: JangKeun Kim

## 1. Overview

This benchmark is a public-facing, safety-oriented evaluation package for assessing whether model safeguards and deployment mitigations remain robust on high-risk scientific content. The public layer focuses on contamination-aware benchmark design, calibration-sensitive response quality, refusal consistency, governance awareness, and release hygiene.

The benchmark does not publish restricted scenarios, operational scientific procedures, or withheld adjudication details. The public package is designed to demonstrate methodology and release discipline rather than maximize capability exposure.

## 2. Safety posture

The public `v0.2` package contains:

- 24 synthetic public-safe items
- a balanced `public_dev` / `public_eval` split with 12 items in each
- four reviewed-response comparison demo slices spanning `public_dev` and `public_eval`
- public schemas for items, reviewed responses, run manifests, and release manifests
- a taxonomy document, annotation handbook, benchmark card draft, and release log
- coverage reporting, public-eval audit outputs, benchmark inventory export, release scorecards, and reproducibility metadata

The public `v0.2` package does not contain:

- restricted prompts or answer keys
- withheld red-team scenarios
- operational bottleneck analysis for harmful workflows
- claims that the benchmark alone demonstrates real-world safety

## 3. Intended use

Appropriate uses:

- safety-oriented benchmark prototyping
- mitigation-audit methodology development
- contamination-aware evaluation design
- portfolio and interview discussion material for frontier-safety work
- governed internal extension work with additional controls

Inappropriate uses:

- capability marketing
- unrestricted release of sensitive evaluation content
- treating public-safe structure metrics as complete safety evidence
- inferring restricted-layer performance from the public layer alone

## 4. Benchmark structure

Current public components:

- `sample_items.jsonl` and `reviewed_sample_responses.jsonl` for the `v0.1` reviewed-response demo flow
- `public_dev_items.jsonl` with 12 development items
- `public_eval_items.jsonl` with 12 evaluation items
- `reviewed_public_dev_responses_v0_2_demo.jsonl`, `reviewed_public_dev_responses_v0_2_slice_b.jsonl`, `reviewed_public_eval_responses_v0_2_demo.jsonl`, and `reviewed_public_eval_responses_v0_2_slice_b.jsonl` for four audited demo slices
- `benchmark_inventory.csv`, `coverage_report.md`, `release_scorecard.csv`, `release_scorecard.md`, `audit_slice_overview.csv`, `audit_longitudinal_comparison.csv`, `audit_longitudinal_summary.md`, `public_dev_audit/summary.md`, `public_dev_audit_slice_b/summary.md`, `public_eval_audit/summary.md`, and `public_eval_audit_slice_b/summary.md`
- public schemas plus documentation for governance, taxonomy, annotation, adjudication, and release planning
- release metadata via run manifests and a consolidated release manifest spanning coverage plus all current audit slices
- 5 visualization charts (pre/post quality, error tag reduction, mitigation delta, longitudinal quality, model heatmap)
- an adjudication framework with schema, handbook, and inter-rater agreement computation script
- a portfolio summary document explaining the full project in plain English

Restricted-layer status:

- restricted-item structure is documented in schema and governance materials
- restricted benchmark content remains intentionally absent from the public repository

## 5. Taxonomy

Current domain families:

- `refusal_and_safe_completion`
- `mitigation_sensitive_query_handling`
- `scientific_interpretation`
- `evaluation_governance`
- `policy_sensitive_response_handling`
- `ambiguity_recognition`

Current reasoning types:

- `safe_boundary_articulation`
- `paraphrase_robustness`
- `factual_uncertainty_handling`
- `evidence_synthesis`
- `comparative_reasoning`
- `missing_information_recognition`

Current release balance:

- 24 total items
- 6 domain families, each represented by 4 items
- 6 reasoning types represented
- 15 items labeled `high` for mitigation relevance
- 12 items labeled `high` for ambiguity level

## 6. Contamination and provenance

The `v0.2` public items are synthetic and intentionally public-safe. Provenance fields are included per item, and the current contamination risk labels are low across the release.

Contamination control practices in this package include:

- explicit public vs withheld split design
- per-item provenance summaries
- refresh planning in the roadmap and taxonomy docs
- release documentation that distinguishes sample items from public evaluation items

## 7. Metrics

Current public metrics and outputs:

- coverage counts by split, domain family, reasoning type, mitigation relevance, and ambiguity level
- reviewed-response metrics from the `v0.1` demo scaffold: calibration, safe-boundary quality, refusal consistency, mitigation robustness, and evidence grounding
- reviewed-response metrics from two `v0.2` public-eval audit slices covering two models across pre- and post-mitigation conditions
- release-manifest artifact accounting
- structured scorecard outputs in markdown and CSV

Interpretation guidance:

- `v0.2` is strongest as a benchmark-structure and release-readiness milestone with audited demo slices across `public_dev` and `public_eval`
- the public package now includes four audited release slices across two demo models, which improves empirical coverage without changing the project's public-safe scope
- benchmark structure metrics should not be treated as model-risk claims

## 8. Annotation process

The annotation workflow is documented in `docs/annotation_handbook.md`. The current process assumes:

- reviewer-visible scoring anchors
- controlled error-tag vocabulary
- complete per-item and per-condition coverage for reviewed-response files
- schema-backed validation before aggregation

The public release demonstrates the workflow through `v0.1` sample reviewed responses, while `v0.2` emphasizes dataset structure and release packaging.

## 9. Known limitations

- `v0.2` still does not include reviewed-response audits for the restricted layer, even though both `public_dev` and `public_eval` now have longitudinal demo coverage
- the current `v0.2` release includes four audited demo slices for two demo models rather than a broader external evaluation program
- public items are synthetic and intentionally abstracted away from restricted operational detail
- restricted-layer evaluation remains documented but not publicly populated
- current release outputs are still stronger on benchmark design and governance than on broad empirical model comparison

## 10. Governance

Governance for this benchmark is described in `07_governance_and_release_policy.md`. In summary:

- public materials stay non-operational
- restricted content remains withheld under governance
- benchmark artifacts are versioned and tracked via release metadata
- release documentation is expected to state scope, safety posture, and validation boundaries clearly

## 11. Changelog

- `v0.1` introduced the initial public-safe scaffold, schemas, sample items, reviewed-response demo data, and the first validator and evaluator
- `v0.2` expands the public-safe benchmark to 24 items, adds taxonomy and annotation documentation, introduces consolidated multi-run release metadata, and adds structured release scorecards, inventory exports, explicit slice-comparison tables, four audited slices across `public_dev` and `public_eval`, 5 visualization charts, an adjudication framework with schema and handbook, an inter-rater agreement computation script, and a portfolio summary
