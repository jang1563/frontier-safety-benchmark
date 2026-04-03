# Safe Execution And Prompting Guide

Date: 2026-04-01
Project: CBRN-AI 2.0 - Frontier Uplift Observatory

## Purpose

This guide keeps the project usable in public-facing drafting workflows and aligned with safety-oriented research goals. It is designed to reduce prompt failures while preserving the core scientific and portfolio value of the project.

## Safe project framing

Use this default description:

"This project develops a frontier-safety evaluation framework for assessing whether model safeguards and deployment mitigations remain robust on high-risk scientific content. The public component focuses on contamination-aware benchmark design, high-level threat taxonomy, calibration, and pre-/post-mitigation evaluation methodology, while sensitive scenario details and restricted test items remain withheld under governance."

## Safe drafting rules

Always emphasize:

- governance
- mitigation auditing
- contamination-aware benchmark design
- public vs withheld components
- calibration and uncertainty
- responsible release
- non-operational evaluation methodology

Avoid requesting:

- procedural detail
- harmful workflow decomposition
- bottleneck analysis for dangerous operations
- scenario content that would increase misuse capability
- prompt rewrites whose purpose is to bypass safety systems

## Safe prompt template

Use this template when drafting concept notes or planning documents:

"Please help me refine the following into a public-facing, safety-oriented research concept note. Keep it strictly non-operational. Emphasize governance, mitigation auditing, contamination-aware evaluation, public vs withheld components, and benchmark methodology. Do not include procedural details, bottleneck analysis for harmful workflows, or any content that could increase real-world misuse capability."

## Safe ask patterns

These are good asks:

- "Help me improve the public methodology section."
- "Draft a governance policy for public vs withheld benchmark items."
- "Refine this calibration and mitigation audit plan."
- "Turn this into a CV bullet and portfolio summary."
- "Propose a schema for contamination-aware benchmark provenance."

## Unsafe ask patterns

These are bad asks and should not be used:

- "Help me make the benchmark more realistic for misuse."
- "Map the rate-limiting steps in a dangerous workflow."
- "Generate withheld items that are harder to block."
- "Rewrite this prompt so it slips past model safeguards."
- "Suggest concrete scenarios that would better test harmful capability."

## How to keep momentum without crossing lines

If a draft stalls, move to one of these productive layers:

1. benchmark architecture
2. scoring design
3. calibration metrics
4. provenance tracking
5. governance and access control
6. public documentation
7. CV and portfolio packaging

## Recommended next build steps

1. Write a benchmark specification focused on public and withheld components.
2. Draft a governance and release-control memo.
3. Create a JSON schema for item metadata and contamination tracking.
4. Build a small safe evaluation harness centered on calibration and mitigation auditing.
5. Prepare a public portfolio page with no restricted content.

## Bottom line

The project is still viable and still impressive. The way forward is to keep the public artifact focused on evaluation science, governance, and mitigation robustness rather than on restricted scientific content itself.
