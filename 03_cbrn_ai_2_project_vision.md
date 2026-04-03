# CBRN-AI 2.0 Project Vision

Date: 2026-04-01
Working title: CBRN-AI 2.0 - Frontier Uplift Observatory
Status: Public-facing, safety-oriented concept note

## Public thesis

CBRN-AI 2.0 is a frontier-safety evaluation framework for assessing whether model safeguards and deployment mitigations remain robust on high-risk scientific content. The public component focuses on contamination-aware benchmark design, high-level threat taxonomy, calibration, governance, and pre-/post-mitigation evaluation methodology, while sensitive scenario details and restricted test items remain withheld under structured review.

## Why this version is the right one

The original project direction risked sliding into dual-use territory because it centered too directly on measuring harmful capability in operational terms. The stronger public-facing version keeps the scientifically serious part of the idea while making the project's purpose clearly defensive:

- evaluate safeguards, not harmful workflows
- study benchmark validity, not operational misuse enablement
- measure calibration and overconfidence, not task execution guidance
- define governance and release controls, not capability ladders for dangerous use

This is also the version that is most reusable for a CV, portfolio, statement of research interests, or interview discussion.

## Core research objective

Develop a rigorous methodology for testing whether frontier-model mitigations generalize beyond known examples on sensitive scientific material, without publishing procedural content that could increase real-world misuse capability.

## Public research questions

1. How should public evaluations of high-risk scientific content be designed so they remain contamination-aware and informative even when sensitive items cannot be fully released?
2. How can we measure whether mitigations improve safety without simply overfitting to known prompts or known benchmark artifacts?
3. How should public and withheld benchmark components be separated to support both transparency and responsible access control?
4. Which metrics best capture safety-relevant model behavior in sensitive domains: calibration, uncertainty expression, refusal quality, harmful specificity suppression, or robustness to paraphrase and prompt variation?
5. How can a single evaluation methodology support multiple frontier-risk domains at a high level while remaining strongest in CBRN-relevant scientific contexts?

## Project scope

### In scope

- public benchmark methodology
- high-level threat taxonomy
- contamination-aware split design
- public vs withheld benchmark architecture
- pre-/post-mitigation evaluation design
- calibration and confidence analysis
- refusal and safe-completion analysis
- governance, access control, and release policy
- expert review and ethics process

### Out of scope

- procedural instructions for hazardous workflows
- bottleneck analysis for real-world harmful operations
- scenario design that meaningfully increases misuse capability
- publication of sensitive prompts, items, or answers
- assistance with bypassing platform safety controls

## Conceptual contribution

The distinctive contribution of CBRN-AI 2.0 is not that it creates a more dangerous benchmark. It is that it provides a safer evaluation architecture for studying high-risk domains where:

- public release must be partial
- contamination is a serious concern
- benchmark scores can be misleading
- calibration matters as much as raw capability
- mitigations must be evaluated without disclosing sensitive content

## Project architecture

### Pillar 1. High-level threat taxonomy

Build a public taxonomy that groups risky scientific interactions into broad categories without operational detail. The taxonomy should be abstract enough to be safe, but concrete enough to support systematic evaluation.

Examples of public taxonomy dimensions:

- information sensitivity level
- domain family
- reasoning type
- uncertainty level
- mitigation relevance
- public-release eligibility

This lets the project discuss coverage, blind spots, and governance without exposing restricted content.

### Pillar 2. Contamination-aware benchmark design

This should be one of the project's signature strengths.

Key design features:

- use post-cutoff or recently curated public materials when possible
- separate public development items from restricted evaluation items
- maintain release logs and provenance for each item
- track possible training-data exposure and benchmark leakage
- include red-team style paraphrase variants in withheld form rather than public release

The point is to measure whether the benchmark is still informative after widespread model exposure to public scientific corpora.

### Pillar 3. Public vs withheld benchmark structure

The project should explicitly define two layers:

#### Public layer

- methodology paper
- safe sample items
- abstracted taxonomy
- scoring rubric families
- benchmark cards and documentation
- calibration and mitigation metrics

#### Withheld layer

- restricted scenario bank
- sensitive evaluation items
- paraphrase and generalization stress tests
- internal adjudication notes
- restricted scorer details where needed

This split is one of the cleanest ways to make the project both serious and responsible.

### Pillar 4. Pre-/post-mitigation evaluation

The project should measure safety behavior before and after mitigation changes, but only in ways that remain non-operational in public materials.

Public evaluation goals:

- assess whether mitigations reduce unsafe specificity
- assess whether mitigations preserve appropriate uncertainty expression
- assess whether mitigations avoid collapsing into unhelpful or inconsistent refusals
- assess whether safety behavior generalizes to novel but high-level paraphrases
- assess whether mitigation gains hold on withheld items, not only public items

This is much more defensible than publishing a capability leaderboard.

### Pillar 5. Calibration and confidence auditing

This is a natural bridge from your prior work.

Public safety questions:

- Does the model express appropriate uncertainty on ambiguous or sensitive scientific queries?
- Does it become overconfident after mitigation?
- Does it provide safe, bounded, uncertainty-aware responses rather than false reassurance?
- Can calibration metrics identify regressions that raw refusal rates miss?

This is an especially strong angle because it is scientifically meaningful, clearly safety-oriented, and much less likely to trigger content restrictions.

### Pillar 6. Governance and responsible release

The project should include a governance section from the beginning rather than as an afterthought.

Recommended governance components:

- dual-use review gate for new benchmark items
- explicit criteria for what is public versus withheld
- named review roles for domain expert, safety reviewer, and release approver
- logging of access decisions for restricted items
- versioned release notes documenting benchmark changes and withholding decisions
- a written misuse review policy for external sharing

This makes the project look mature and institutionally legible.

## Methodology blueprint

### Public evaluation metrics

Recommended metrics for the public-facing part:

- calibration error
- confidence on ambiguous or restricted queries
- refusal consistency
- safe-completion quality
- harmful-specificity suppression
- paraphrase robustness
- pre-/post-mitigation delta
- withheld-set generalization gap

### Annotation strategy

Use a tiered labeling plan:

- policy / safety label
- scientific ambiguity label
- mitigation-relevance label
- public-release label
- confidence / calibration label

This makes the dataset useful without exposing sensitive content.

### Study design options

Safe study designs include:

- model-only evaluation on safe public items
- blinded reviewer scoring of response quality and uncertainty handling
- comparison across model versions before and after mitigation changes
- withheld-set internal audits under governance
- qualitative error analysis focused on calibration, refusal quality, and policy consistency

## Concrete deliverables

### Short-term

- public concept note
- benchmark design memo
- taxonomy schema
- governance policy draft
- rubric draft

### Mid-term

- public benchmark card
- contamination and provenance tracking template
- calibration / mitigation evaluation harness
- safe sample dataset

### Longer-term

- public methods paper
- internal or restricted evaluation protocol
- portfolio-ready project page
- reusable evaluation framework adaptable to other frontier-risk domains

## Why this is still a strong DeepMind-facing project

This version still signals the right things:

- frontier-safety orientation
- evaluation methodology depth
- mitigation auditing
- benchmark skepticism
- governance maturity
- cross-domain transferability

It just does so without drifting into operationally risky territory.

## CV and portfolio framing

### CV-ready one-liner

"Designed CBRN-AI 2.0, a safety-oriented frontier-evaluation framework for contamination-aware benchmark design, governance, calibration auditing, and pre-/post-mitigation assessment on high-risk scientific content with public and withheld benchmark components."

### Slightly longer portfolio summary

"CBRN-AI 2.0 is a public-facing research program on how to evaluate frontier-model safeguards in sensitive scientific domains without publishing misuse-enabling content. The project emphasizes contamination-aware benchmark design, governance, calibration, and withheld-set mitigation auditing rather than operational capability measurement."

## What makes the project novel

- It treats benchmark release itself as a safety problem.
- It treats contamination as a central scientific validity problem.
- It centers calibration and uncertainty rather than only capability.
- It formalizes public vs withheld benchmark architecture.
- It is designed to be extended across other frontier-risk domains.

## Recommended next documents

The next useful files for this project are:

- a public benchmark specification
- a governance and release policy
- a schema for public and withheld items
- a mitigation audit plan
- a prompt template library for safe project drafting

## Bottom line

Yes, the project can go ahead. The right way forward is not to push past safety boundaries, but to make the boundary itself part of the research design. That turns the constraint into one of the project's strongest intellectual contributions.
