# Portfolio Summary: CBRN-AI 2.0 - Frontier Uplift Observatory

Author: JangKeun Kim
Version: 0.2.0-demo
Date: 2026-04-02

## What this project is

This is a safety evaluation project. It is not a tool for doing CBRN work.

The goal is to design, build, and demonstrate a contamination-aware benchmark framework for testing whether AI models behave safely on sensitive scientific topics. The project covers the full lifecycle: benchmark design, taxonomy, scoring, validation, release packaging, and longitudinal comparison.

## Why it matters

Frontier AI labs need structured ways to test whether their safety mitigations actually work. The standard approach is to build evaluation benchmarks, but doing this well for sensitive domains like CBRN, cyber, and biosecurity is harder than for general-purpose tasks because:

- the test items themselves can be dangerous if released carelessly
- benchmark contamination can silently erode evaluation value
- pre- and post-mitigation comparisons require careful experimental design
- public and restricted layers must be governed separately

This project addresses all four problems within a single, working package.

## What has been built

### Benchmark items (24 public-safe items)

The current benchmark contains 24 synthetic items organized into a balanced `public_dev` / `public_eval` split. Each item tests a specific safety behavior: refusal quality, uncertainty handling, paraphrase robustness, policy consistency, evidence grounding, or governance awareness.

All items are intentionally non-operational. They test model behavior on safety-relevant topics without including any restricted procedures or real-world enablement detail.

### Taxonomy and annotation infrastructure

The benchmark uses a structured taxonomy with 6 domain families, 6 reasoning types, 3 risk sensitivity tiers, 3 ambiguity levels, and 2 mitigation relevance levels. Each item is labeled across all axes.

A 420-line annotation handbook defines the review workflow, scoring anchors (1-5 scale), error-tag vocabulary, borderline resolution rules, and reviewer consistency checks.

### Scoring pipeline (5 metrics, 6 error tags)

Each model response is scored on five numeric metrics:
- **Calibration**: does the model express appropriate certainty?
- **Safe boundary**: does it maintain limits on sensitive content?
- **Refusal consistency**: does it stay stable under pressure or paraphrase?
- **Mitigation robustness**: does the safety mitigation hold?
- **Evidence grounding**: is the reasoning anchored in evidence?

Plus six controlled error tags: overconfidence, false reassurance, inconsistent refusal, unsupported certainty, policy inconsistency, incomplete safe alternative.

### Audited release slices (4 slices, 2 models, 192 scored responses)

The package includes four audited comparison slices across two demo models (`demo-model-v0.2` and `strict-model-v0.2`), each evaluated under pre-mitigation and post-mitigation conditions. This creates a longitudinal comparison layer showing how model behavior changes across audit runs.

Key findings from the demo audits:
- Post-mitigation quality is consistently strong (averages 4.1-4.7 on the 1-5 scale)
- Error tags drop from 16-22 pre-mitigation to 0-2 post-mitigation
- Later slices show stable or improving post-mitigation quality with stronger pre-mitigation baselines
- Both models clear residual error tags to zero by the final slice

### Validation and reproducibility infrastructure

The package includes:
- JSON schemas for items, responses, run manifests, and release manifests
- A scaffold validator with duplicate detection, cross-condition coverage checks, and SHA-256 integrity verification
- Run manifests tracking which scripts produced which artifacts
- A consolidated release manifest spanning all data, documentation, and result artifacts

### Release documentation

The package ships with:
- A benchmark card (model-card-style documentation)
- Release logs for both v0.1 and v0.2
- A release scorecard with structural metrics, audit summaries, and cross-model/cross-slice comparisons
- CSV exports for the benchmark inventory, scorecard, slice overview, and longitudinal comparison
- A taxonomy document and annotation handbook

## What this demonstrates

This project demonstrates five research-engineering competencies:

1. **Benchmark design**: creating evaluation items that test safety behavior without introducing risk
2. **Contamination awareness**: separating public from restricted content, tracking provenance, and planning refresh cycles
3. **Evaluation methodology**: pre/post-mitigation comparison, multi-model auditing, longitudinal tracking
4. **Release governance**: versioned manifests, SHA-256 integrity hashes, explicit safety posture documentation
5. **Research communication**: structured outputs that are readable by reviewers, interviewers, and collaborators

## How it connects to frontier safety work

The Frontier Safety Framework at labs like DeepMind organizes risk around Critical Capability Levels (CCLs) across five domains: CBRN, cyber, ML R&D, loss of control, and harmful manipulation.

This project is directly aligned with that framework because it addresses the question: **how do you evaluate whether mitigations actually work, without the evaluation itself becoming a risk?**

The CBRN domain is the entry point, but the methodology (contamination-aware benchmarking, governed public/restricted splits, mitigation auditing, calibration-sensitive scoring) applies to any sensitive evaluation domain.

## Current limitations

- The current audits use synthetic demo models, not real frontier or open-source models
- The restricted layer is designed but not publicly populated
- The benchmark is small (24 items) and would need scaling for a full empirical study
- No external reviewer or inter-rater reliability component yet

## What comes next

The strongest next steps to move this from "strong scaffold" to "serious standout":

1. **Visualization layer**: charts showing pre/post-mitigation quality, cross-model comparisons, and longitudinal trends
2. **Expert adjudication framework**: inter-rater agreement tracking and adjudication workflow for disputed scores
3. **Real model evaluation**: running the benchmark against actual frontier or open-source models
4. **Scaling**: expanding item coverage and adding drift-refresh items for contamination monitoring

## How to explore the package

Start with the release scorecard for the numbers, then the benchmark card for the methodology, then the taxonomy and annotation handbook for the design principles:

1. `results/v0_2_demo/release_scorecard.md` - the main results summary
2. `docs/benchmark_card_draft.md` - what the benchmark is and how it works
3. `docs/taxonomy.md` - how items are organized
4. `docs/annotation_handbook.md` - how responses are scored
5. `results/v0_2_demo/audit_longitudinal_summary.md` - how models change across slices

## One-sentence summary

A working, contamination-aware frontier-safety benchmark package with 24 public-safe items, 192 scored responses across 4 audited slices, structured validation, and governed release infrastructure, demonstrating the full evaluation lifecycle for sensitive AI safety domains.
