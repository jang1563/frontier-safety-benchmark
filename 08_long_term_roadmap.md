# Long-Term Roadmap

Date: 2026-04-01
Project: CBRN-AI 2.0 - Frontier Uplift Observatory
Time horizon: 18-24 months
Scope: Public-facing, safety-oriented evaluation research program

## Executive summary

The long-term goal of CBRN-AI 2.0 is to become a credible, portfolio-quality frontier-safety research program rather than a one-off benchmark. To get there, the project needs to mature across five dimensions at once:

- evaluation methodology
- contamination-aware benchmark operations
- governance and release discipline
- mitigation-audit infrastructure
- external legibility through documentation, reports, and selective public artifacts

The strongest version of this project after 18-24 months is:

- a reusable safety-oriented evaluation framework
- a public benchmark and methods package
- a governed restricted evaluation layer
- a calibration and mitigation audit harness
- a coherent publication and portfolio trail

## 1. Program North Star

### Primary objective

Develop a durable evaluation program for testing whether safeguards and deployment mitigations remain robust on high-risk scientific content under contamination pressure, distribution shift, and withheld-set evaluation.

### Success condition

At the end of the roadmap, you should be able to say:

"CBRN-AI 2.0 is not just a concept. It is a governed, contamination-aware, mitigation-audit evaluation program with public documentation, a benchmark specification, a restricted review process, and a reusable framework for frontier-risk research."

### Anti-goal

The project should not become:

- a static benchmark with no maintenance plan
- a public release of restricted scientific content
- a narrow portfolio artifact that cannot generalize beyond one application

## 2. Strategic design principles

Every phase should preserve these principles:

- public artifacts stay non-operational
- governance is part of the research contribution
- contamination is treated as a validity problem, not an afterthought
- calibration and uncertainty are first-class metrics
- mitigation auditing matters more than raw capability ranking
- benchmark maintenance is part of the scientific design

## 3. Program structure

The roadmap is organized into six phases:

1. Foundation
2. Prototype
3. Internal maturation
4. Public release
5. External validation
6. Platformization

Each phase has:

- a core goal
- specific deliverables
- exit criteria
- key risks

## 4. Phase 0: Foundation

Timeline:

- Weeks 1-4

### Goal

Lock down the project's identity, scope, safety boundaries, and initial operating model.

### Deliverables

- project charter
- benchmark specification
- governance and release policy
- safe prompting and execution guide
- first metadata schema draft

### Key tasks

- define the exact public thesis
- define project non-goals
- define public vs restricted artifact categories
- define naming, versioning, and folder conventions
- define review roles and decision flow

### Exit criteria

- the project can be described in one paragraph without ambiguity
- all future work can be routed through explicit public vs restricted handling rules
- the public artifact is already portfolio-safe

### Key risks

- concept drift back toward unsafe specificity
- unclear line between research methodology and restricted content

## 5. Phase 1: Prototype

Timeline:

- Months 1-3

### Goal

Build the first real research prototype that demonstrates methodological seriousness.

### Deliverables

- public metadata schema v0.1
- item lifecycle workflow
- contamination tracking template
- scoring rubric v0.1
- safe sample dataset
- small calibration and mitigation audit harness

### Key tasks

- implement item schema in JSON or YAML
- define core public labels and score families
- create 20-40 safe sample items
- implement logging for model version, prompt template, and mitigation condition
- create first evaluation notebook or script

### Exit criteria

- you can run a small end-to-end public evaluation
- outputs are versioned and reproducible
- benchmark items can be tracked by provenance and release class

### Portfolio outputs

- repo structure screenshot
- benchmark card draft
- 1-2 figures on calibration or mitigation deltas
- public methods note

### Key risks

- building too much content before the schema is stable
- mixing exploratory notes with release-ready materials

## 6. Phase 2: Internal maturation

Timeline:

- Months 3-6

### Goal

Turn the prototype into a repeatable internal research workflow.

### Deliverables

- schema v1.0
- annotation handbook
- reviewer workflow guide
- restricted audit split policy
- contamination refresh policy
- benchmark card v1

### Key tasks

- formalize annotation and review steps
- create decision logs for release-class assignments
- establish drift / refresh cadence
- add withheld-set logic to the evaluation harness
- create qualitative error taxonomy for overconfidence, false reassurance, and policy inconsistency

### Exit criteria

- new items can be added without ad hoc decisions
- restricted evaluation can be run under defined governance
- benchmark maintenance work is documented, not implicit

### Portfolio outputs

- process diagram
- data model diagram
- methodology memo on contamination-aware design

### Key risks

- governance becoming too vague to be actionable
- public and restricted versions diverging without traceability

## 7. Phase 3: Public release

Timeline:

- Months 6-9

### Goal

Release the first coherent public-facing version that is strong enough for portfolio and application use.

### Deliverables

- public project README
- benchmark card v1 public edition
- safe sample dataset release
- public scoring overview
- public concept note / white paper
- release notes and version history

### Key tasks

- polish public language for broad legibility
- create figures and tables that illustrate methodology without exposing sensitive content
- document contamination policy and release classes clearly
- prepare short and long project summaries

### Exit criteria

- an external reviewer can understand the project from the public docs alone
- the release is methodologically credible without disclosing restricted content
- the project is CV-ready and portfolio-ready

### Portfolio outputs

- polished project page
- one-page project overview PDF
- concise project summary for CV, cover letter, and website

### Key risks

- public materials feeling too abstract to be credible
- over-disclosure pressure during polishing

## 8. Phase 4: External validation

Timeline:

- Months 9-15

### Goal

Stress-test the framework through external-style critique and limited advisory input.

### Deliverables

- structured feedback memo from expert reviewers
- benchmark revision log
- revised governance policy
- second public release
- internal report on failure modes of the benchmark itself

### Key tasks

- solicit feedback on the benchmark card and methodology
- test whether public docs are understandable and sufficiently specific
- identify where contamination controls are weakest
- identify metrics that are unstable or easy to game
- refine safe sample items and taxonomy labels

### Exit criteria

- major external criticisms are documented and addressed
- at least one release cycle has included meaningful revision after review
- the project can explain its own limitations clearly

### Portfolio outputs

- lessons-learned report
- revision diff summary
- roadmap update memo

### Key risks

- external feedback pushing toward unsafe specificity
- benchmark credibility suffering if limitations are not communicated clearly

## 9. Phase 5: Platformization

Timeline:

- Months 15-24

### Goal

Convert the project from a document set into a lightweight research platform.

### Deliverables

- stable evaluation harness
- structured benchmark registry
- release audit log
- dashboard or summary report generator
- reusable package for future domain extensions

### Key tasks

- modularize schemas and scoring logic
- build templated report generation
- standardize configuration for public vs restricted runs
- support version comparisons across mitigation conditions
- prepare extension hooks for other frontier-risk domains

### Exit criteria

- the project can support multiple evaluation rounds cleanly
- public and restricted components share a common backbone
- future domain adaptation does not require redesign from scratch

### Portfolio outputs

- architecture diagram
- project demo or screen capture
- technical write-up on framework design

### Key risks

- over-engineering before research questions stabilize
- tool-building crowding out scientific interpretation

## 10. Cross-cutting workstreams

These should run across multiple phases rather than belonging to only one phase.

### Workstream A: Documentation

Maintain:

- benchmark card
- release notes
- roadmap notes
- methodology memos
- portfolio summaries

### Workstream B: Governance

Maintain:

- release class decisions
- reviewer assignments
- redaction logic
- change logs
- misuse response norms

### Workstream C: Evaluation science

Maintain:

- metric validation
- calibration analysis
- mitigation-audit design
- contamination tracking
- qualitative error analysis

### Workstream D: Portfolio and career translation

Maintain:

- CV bullet updates
- project summaries
- interview-ready narratives
- publication ideas

## 11. Success metrics by horizon

### By 3 months

- clear project identity
- working schema
- first safe sample set
- first evaluation run

### By 6 months

- governed item workflow
- benchmark card v1
- reproducible calibration / mitigation harness

### By 9 months

- public release with coherent documentation
- portfolio-ready project page
- strong CV / statement language

### By 15 months

- revised release after feedback
- explicit limitations and lessons learned
- stronger credibility through iteration

### By 24 months

- lightweight evaluation platform
- stable methodology package
- durable research identity around frontier-safety evaluation

## 12. Resource model

### Minimum solo version

What one person can realistically do:

- benchmark design
- schema and documentation
- small public dataset
- lightweight evaluation harness
- governance policy
- limited revision cycles

### Small team version

Ideal roles:

- evaluation lead
- domain reviewer
- safety reviewer
- annotation / ops support

### Stretch support

Helpful additions:

- external advisory reviewer
- design / documentation support
- engineering support for report automation

## 13. Research outputs strategy

The project should produce multiple artifact types rather than aiming at only one paper.

### Public artifact types

- concept note
- benchmark card
- governance memo
- methodology white paper
- project page
- selected figures and result summaries

### Restricted artifact types

- audit protocol
- review logs
- restricted split notes
- adjudication notes

### Publication strategy

Possible publication directions:

- contamination-aware benchmark design for sensitive domains
- public-vs-withheld benchmark architecture
- calibration and mitigation auditing in safety-sensitive evaluation
- governance as a benchmark-design contribution

## 14. Career and portfolio strategy

For your CV and portfolio, the project becomes more valuable when it can tell three stories at once:

### Story 1. Evaluation scientist

- designed a new methodology, not just a dataset

### Story 2. Responsible researcher

- built governance and release discipline into the project from the beginning

### Story 3. Research engineer

- implemented schemas, scoring pipelines, and repeatable evaluation tooling

That combination is stronger than either pure writing or pure tooling alone.

## 15. Review cadence

Use a regular planning loop:

### Monthly

- roadmap review
- schema and metric issues
- artifact status check

### Quarterly

- release readiness review
- governance audit
- portfolio and application refresh

### Major version release

- benchmark card update
- release notes
- limitations statement
- next-version priorities

## 16. Risk register

### Scientific risks

- contamination makes the benchmark less informative over time
- metrics drift away from meaningful safety signals
- public items become too narrow or too sanitized

### Project risks

- too much planning, not enough implementation
- too much implementation, not enough documentation
- scope grows faster than review capacity

### Safety risks

- public artifact accidentally becomes more informative than intended
- restricted content handling becomes inconsistent
- external requests pressure the project toward over-disclosure

### Career risks

- project reads as abstract governance rather than technical research
- project looks incomplete because the public layer is intentionally partial

### Mitigations

- versioned release classes
- clear public thesis
- regular artifact production
- visible tooling and schema work
- clear explanations of why partial release is a feature, not a weakness

## 17. Recommended immediate next steps

To start the roadmap well, do these next:

1. Create the item schemas as actual files.
2. Create a starter `data_public/` directory with a few safe sample items.
3. Create a benchmark card template.
4. Create a release-log template.
5. Build a first evaluation script focused on calibration and mitigation deltas.

## 18. Bottom line

The long-term win is not just "finish a benchmark." The long-term win is to build a small but credible frontier-safety evaluation program that demonstrates methodological rigor, governance maturity, research engineering ability, and strong judgment about how to work on sensitive domains responsibly.
