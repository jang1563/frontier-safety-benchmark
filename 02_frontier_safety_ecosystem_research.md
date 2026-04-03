# Frontier Safety Ecosystem Research

Date: 2026-04-01
Method: current web research using primary or near-primary sources where possible

## Executive summary

The strongest evidence from current sources is that frontier safety teams are looking for technical staff who can:

- identify new risk pathways
- design new measurements for pre-mitigation and post-mitigation risk
- reason across multiple risk domains
- prioritize evaluations based on value of information
- build evidence that can support mitigation and deployment decisions

The evaluation ecosystem has converged on threshold-triggered safeguards tied to Critical Capability Levels (CCLs), early warning evaluations, and mitigation-audit methodology, not just static benchmarks.

## 1. DeepMind's evaluation stack

### 1.1 Dangerous capabilities research program

Primary source:

- [Evaluating Frontier Models for Dangerous Capabilities](https://deepmind.google/research/publications/evaluating-frontier-models-for-dangerous-capabilities/) (March 2024)

Why it matters:

- This paper is the clearest public map of the team's evaluation philosophy.
- The paper covers persuasion and deception, cyber-security, self-proliferation, self-reasoning / self-modification, and biological / nuclear risk.
- It distinguishes dangerous-capability detection from simple benchmark scoring.

### 1.2 Frontier Safety Framework (initial version)

Primary source:

- [Introducing the Frontier Safety Framework](https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/) (2024)

What it established:

- Critical Capability Levels (CCLs)
- early warning evaluations
- mitigation triggers when models approach or cross thresholds
- initial domains: autonomy, biosecurity, cybersecurity, and ML R&D

Important detail:

- The framework is explicitly about identifying the minimal capability level at which severe harm becomes plausible and then testing early enough to avoid surprises.
- The key design principle is early warning measurement against plausible harm pathways, not just benchmark creation.

### 1.3 FSF v3.0 and harmful manipulation

Primary source:

- [Strengthening our Frontier Safety Framework](https://deepmind.google/discover/blog/strengthening-our-frontier-safety-framework/) (September 22, 2025)

Key updates:

- introduced a harmful manipulation CCL
- expanded protocols for ML R&D-related CCLs
- treated some advanced ML R&D capability levels as risky even for large-scale internal deployments
- emphasized safety case reviews before launches when relevant CCLs are reached

### 1.4 Cyber evaluations

Primary source:

- [Evaluating potential cybersecurity threats of advanced AI](https://deepmind.google/discover/blog/evaluating-potential-cybersecurity-threats-of-advanced-ai/) (April 2, 2025)

Key details:

- DeepMind analyzed more than 12,000 real-world attempts to use AI in cyberattacks across 20 countries.
- They created seven archetypal attack categories and a 50-challenge benchmark spanning the attack chain.
- The framing is explicitly bottleneck-based: focus evaluation on where AI can make attacks faster, cheaper, or easier.

Research implication:

- This is the closest public example of how capability decomposition works in practice: attack chain, bottlenecks, actor models, and measured uplift.

### 1.5 Harmful manipulation toolkit

Primary source:

- [Protecting people from harmful manipulation](https://deepmind.google/blog/protecting-people-from-harmful-manipulation/) (March 26, 2026)

Key details:

- Described as the first empirically validated toolkit for measuring harmful manipulation in the real world.
- The studies involved more than 10,000 participants across the UK, US, and India.
- The framework measures both efficacy and propensity, not just whether the model can say persuasive things.

Research implication:

- This signals that the field increasingly values human-subject and sociotechnical evaluation, not just static prompt-response benchmarks.

## 2. DeepMind's currently public frontier-safety results

Primary sources:

- [Gemini 3.1 Pro model card](https://deepmind.google/models/model-cards/gemini-3-1-pro) (published February 19, 2026)
- [Gemini model cards index](https://deepmind.google/models/model-cards/)

Key publicly stated results:

- DeepMind's frontier safety assessments cover five domains: CBRN, cyber, harmful manipulation, machine learning R&D, and misalignment.
- Gemini 3.1 Pro remained below the CCLs in all five domains.
- Cyber had already reached the alert threshold in prior models, so DeepMind ran extra testing there.
- Harmful manipulation: DeepMind reports a maximum odds ratio of 3.6x versus a non-AI baseline, but not enough to reach the alert threshold.
- ML R&D: Gemini 3.1 Pro scored a human-normalized average of 1.27 on RE-Bench versus Gemini 3 Pro's 1.04, but still remained below the relevant CCLs.
- Misalignment exploratory evals included stealth and situational awareness tasks; the model was strong on some tasks but did not reach the alert threshold.

## 3. Adjacent governance frameworks and evaluators

### 3.1 Anthropic Responsible Scaling Policy

Primary sources:

- [Responsible Scaling Policy updates](https://www.anthropic.com/rsp-updates)
- [Activating AI Safety Level 3 protections](https://www.anthropic.com/news/activating-asl3-protections) (May 22, 2025)
- [Responsible Scaling Policy Version 3.0](https://www.anthropic.com/news/responsible-scaling-policy-v3)

Important points:

- Anthropic's March 31, 2025 RSP 2.1 update added a CBRN development threshold and split AI R&D capability thresholds more finely.
- Anthropic activated ASL-3 deployment and security protections on May 22, 2025 for Claude Opus 4 as a precautionary step tied to CBRN misuse risk.
- The ecosystem has converged on threshold-triggered safeguards, not generic safety language.

### 3.2 OpenAI Preparedness Framework v2

Primary sources:

- [Preparedness Framework v2 PDF](https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf) (last updated April 15, 2025)
- [OpenAI o3 and o4-mini System Card](https://openai.com/index/o3-o4-mini-system-card/) (April 16, 2025)

Important points:

- OpenAI's preparedness work tracks biological / chemical capability, cybersecurity, and AI self-improvement.
- Their system cards increasingly combine benchmark evidence with external reviews and deployment thresholds.

### 3.3 METR and benchmark-to-reality skepticism

Primary sources:

- [Five lessons from having helped run an AI-Biology RCT](https://metr.org/blog/2026-02-19-five-lessons-from-ai-biology-rct/) (February 19, 2026)
- [Task-Completion Time Horizons of Frontier AI Models](https://metr.org/time-horizons/) (last updated March 3, 2026)
- [Research Update: Algorithmic vs. Holistic Evaluation](https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons/) (August 13, 2025)

Important points:

- The AI-biology RCT involved 153 novices over 8 weeks.
- METR reports that AI was helpful on individual steps but did not produce a significant effect on end-to-end success across the three core tasks together.
- METR's later work repeatedly warns that algorithmically scored benchmarks can overestimate real-world usefulness.

Research implication:

- This is a strong reason not to oversell benchmark results and to include human studies or expert red teaming in evaluation design.

Note on the "1.4x uplift" claim:

- This was not independently verified from a primary source during this pass.
- The safer primary-source claim is that the RCT did not show a significant end-to-end improvement across the core tasks, despite some step-level usefulness.

### 3.4 WMDP

Primary or near-primary sources:

- [WMDP ICML poster page](https://icml.cc/virtual/2024/poster/32695)
- [CAIS WMDP dataset card](https://huggingface.co/datasets/cais/wmdp)

Key details:

- WMDP is a multiple-choice benchmark for hazardous knowledge.
- The original paper is often cited as having 4,157 questions; the current public Hugging Face dataset exposes 3,668 across bio, cyber, and chem subsets after later curation.
- The dataset card itself notes that some WMDP-Bio questions were removed after feedback from Google DeepMind and OpenAI.

Research implication:

- WMDP is useful but not sufficient. Its own associated materials point toward limitations of multiple-choice format, training contamination, and missing end-to-end misuse dynamics.

### 3.5 VCT / SecureBio

Primary or near-primary sources:

- [Virology Capabilities Test site](https://www.virologytest.ai/)
- [VCT paper page](https://huggingface.co/papers/2504.16137)
- [VCT PDF](https://www.virologytest.ai/vct_paper.pdf)

Key details:

- VCT contains 322 multimodal virology troubleshooting questions.
- Expert virologists with internet access averaged 22.1% in their areas of expertise.
- OpenAI o3 reached 43.8%, outperforming 94% of expert virologists on matched subsets.

Research implication:

- This is a much more serious bio-capability signal than simple MCQ biology benchmarks. It points directly toward tacit wet-lab knowledge as an evaluation frontier.

### 3.6 UK AI Security Institute

Primary source:

- [AI Security Institute - Frontier AI Trends report factsheet](https://www.gov.uk/government/publications/ai-security-institute-frontier-ai-trends-report-factsheet) (December 18, 2025)

Research implication:

- Frontier evaluations are now institutionalized beyond labs themselves, involving government bodies and the broader public-interest evaluation ecosystem.

## 4. Sources

- Dangerous capabilities paper page: https://deepmind.google/research/publications/evaluating-frontier-models-for-dangerous-capabilities/
- FSF introduction: https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/
- FSF v3.0 update: https://deepmind.google/discover/blog/strengthening-our-frontier-safety-framework/
- Cyber evaluation framework: https://deepmind.google/discover/blog/evaluating-potential-cybersecurity-threats-of-advanced-ai/
- Harmful manipulation toolkit: https://deepmind.google/blog/protecting-people-from-harmful-manipulation/
- Gemini 3.1 Pro model card: https://deepmind.google/models/model-cards/gemini-3-1-pro
- Anthropic RSP updates: https://www.anthropic.com/rsp-updates
- Anthropic ASL-3 activation: https://www.anthropic.com/news/activating-asl3-protections
- Anthropic RSP v3.0: https://www.anthropic.com/news/responsible-scaling-policy-v3
- OpenAI Preparedness Framework v2: https://cdn.openai.com/pdf/18a02b5d-6b67-4cec-ab64-68cdfbddebcd/preparedness-framework-v2.pdf
- OpenAI o3 / o4-mini system card: https://openai.com/index/o3-o4-mini-system-card/
- METR AI-biology RCT note: https://metr.org/blog/2026-02-19-five-lessons-from-ai-biology-rct/
- METR time horizons: https://metr.org/time-horizons/
- METR algorithmic vs holistic note: https://metr.org/blog/2025-08-12-research-update-towards-reconciling-slowdown-with-time-horizons/
- WMDP dataset card: https://huggingface.co/datasets/cais/wmdp
- WMDP ICML page: https://icml.cc/virtual/2024/poster/32695
- VCT site: https://www.virologytest.ai/
- VCT paper page: https://huggingface.co/papers/2504.16137
- VCT PDF: https://www.virologytest.ai/vct_paper.pdf
- UK AISI factsheet: https://www.gov.uk/government/publications/ai-security-institute-frontier-ai-trends-report-factsheet
