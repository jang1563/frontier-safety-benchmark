# Governance And Release Policy

Date: 2026-04-01
Project: CBRN-AI 2.0 - Frontier Uplift Observatory
Scope: Public-facing governance framework for benchmark and evaluation release

## Purpose

This document defines a governance model for building and releasing a safety-oriented evaluation framework in a high-risk scientific domain while minimizing misuse risk.

## Core principle

The benchmark is not only about evaluating model behavior. It is also about evaluating what should and should not be published. Release decisions are therefore part of the scientific method for this project.

## Governance objectives

- prevent misuse-enabling release
- preserve scientific usefulness
- document release decisions clearly
- support internal restricted evaluation where needed
- make public artifacts legible to external reviewers

## Governance roles

### Domain reviewer

Responsibilities:

- assess scientific content sensitivity
- identify dual-use concerns
- advise on whether an item is suitable for public release

### Safety reviewer

Responsibilities:

- assess misuse risk
- review prompt and reference content for operational sensitivity
- recommend withholding, abstraction, or redaction

### Evaluation lead

Responsibilities:

- maintain benchmark quality
- document scoring rules
- ensure contamination and provenance tracking

### Release approver

Responsibilities:

- make the final public vs withheld decision
- sign off on benchmark version releases
- ensure release notes document major changes

## Release classes

Use four release classes:

### Class A: Public

- safe to publish fully
- may appear in documentation and sample materials

### Class B: Public metadata only

- item existence and taxonomy can be described
- prompt content remains withheld

### Class C: Restricted internal use

- used only for governed evaluation
- not published externally

### Class D: Do not retain

- too sensitive to use safely
- not included in the benchmark

This prevents the false choice between "publish everything" and "publish nothing."

## Review workflow

1. Draft item is created with metadata only.
2. Domain reviewer assesses scientific sensitivity.
3. Safety reviewer assesses release risk.
4. Evaluation lead assigns provisional release class.
5. Release approver confirms or modifies the decision.
6. Decision is logged in versioned release notes.

## Decision criteria

The following questions should guide each release decision:

- Does publication materially increase real-world misuse capability?
- Can the scientific point be preserved through abstraction or metadata-only release?
- Is the item needed publicly for credibility, or is documentation enough?
- Would public release increase benchmark contamination more than it increases transparency?
- Is the item replaceable by a safer proxy for public-facing purposes?

## Redaction strategy

When an item is too sensitive for full release but still valuable methodologically, redact by:

- publishing taxonomy rather than content
- summarizing scoring categories rather than the exact prompt
- releasing provenance metadata without revealing the item body
- abstracting response expectations at a higher level

## Versioning policy

Every benchmark release should include:

- version number
- summary of added and removed items
- changes in release classes
- contamination updates
- metric changes
- documentation of any new withholding rules

## Access control for restricted items

Restricted materials should only be accessible to approved reviewers under documented conditions.

Minimum controls:

- named access list
- purpose-limited access
- access logging
- local handling guidance
- no casual redistribution

## External communication policy

When describing the project publicly:

- emphasize methodology, governance, and mitigation auditing
- avoid examples that create operational intuition for misuse
- describe withheld components at an abstract level only
- do not claim comprehensiveness where content was intentionally withheld

## Misuse response policy

If external requests seek:

- restricted prompts
- benchmark answers
- harmful scenario elaboration
- bypass guidance for safety systems

the response should be:

- decline release
- restate the project's safety-oriented purpose
- redirect discussion toward public methodology or governance artifacts

## Ethics and oversight extensions

As the project grows, consider adding:

- periodic external advisory review
- documented conflict-resolution process for release disputes
- annual governance audit
- explicit retirement process for outdated or newly risky public materials

## Why this matters for your portfolio

This governance layer strengthens the project because it shows:

- mature judgment
- institutional thinking
- understanding that benchmark design is itself a safety problem
- ability to work on frontier-risk evaluation without drifting into unsafe disclosure

## Bottom line

For this project, governance is not a wrapper around the research. Governance is part of the research contribution.
