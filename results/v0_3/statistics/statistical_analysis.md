# Statistical Analysis Summary

- Generated on: 2026-04-12
- Items: 24
- Bootstrap resamples: 10000

## Post-Mitigation Means with 95% Bootstrap CIs

| Model | Metric | Mean | 95% CI | Delta | Delta CI | Wilcoxon p | Cohen's d |
|-------|--------|------|--------|-------|----------|-----------|-----------|
| GPT-4o | Calibration | 3.958 | [3.625, 4.292] | -0.375 | [-0.708, -0.083] | 0.0357 | -0.487 |
| GPT-4o | Safe Boundary | 4.208 | [3.917, 4.458] | -0.167 | [-0.458, +0.125] | 0.3270 | -0.219 |
| GPT-4o | Refusal Consistency | 3.833 | [3.583, 4.083] | -0.125 | [-0.417, +0.167] | 0.4469 | -0.169 |
| GPT-4o | Mitigation Robustness | 4.542 | [4.292, 4.750] | +0.708 | [+0.458, +1.000] | 0.0010 | 1.026 |
| GPT-4o | Evidence Grounding | 3.958 | [3.667, 4.250] | +0.042 | [-0.333, +0.417] | 0.7794 | 0.042 |
| DeepSeek-V3 | Calibration | 4.167 | [3.875, 4.458] | -0.167 | [-0.500, +0.125] | 0.3329 | -0.204 |
| DeepSeek-V3 | Safe Boundary | 4.458 | [4.208, 4.667] | +0.125 | [-0.250, +0.583] | 0.7897 | 0.116 |
| DeepSeek-V3 | Refusal Consistency | 4.042 | [3.792, 4.292] | +0.042 | [-0.333, +0.458] | 0.8590 | 0.040 |
| DeepSeek-V3 | Mitigation Robustness | 4.750 | [4.583, 4.917] | +0.708 | [+0.292, +1.125] | 0.0086 | 0.654 |
| DeepSeek-V3 | Evidence Grounding | 4.167 | [3.833, 4.458] | +0.125 | [-0.083, +0.375] | 0.3454 | 0.204 |
| Llama-3.3-70B | Calibration | 4.292 | [3.958, 4.583] | +0.167 | [-0.083, +0.417] | 0.2367 | 0.262 |
| Llama-3.3-70B | Safe Boundary | 4.417 | [4.208, 4.625] | +0.250 | [-0.042, +0.583] | 0.1282 | 0.315 |
| Llama-3.3-70B | Refusal Consistency | 4.083 | [3.917, 4.250] | +0.292 | [+0.042, +0.583] | 0.0747 | 0.389 |
| Llama-3.3-70B | Mitigation Robustness | 4.750 | [4.583, 4.917] | +1.000 | [+0.667, +1.292] | 0.0004 | 1.199 |
| Llama-3.3-70B | Evidence Grounding | 4.083 | [3.792, 4.333] | +0.333 | [+0.000, +0.708] | 0.1282 | 0.364 |
| Qwen3-32B | Calibration | 4.292 | [4.042, 4.542] | -0.042 | [-0.333, +0.250] | 0.7989 | -0.056 |
| Qwen3-32B | Safe Boundary | 4.583 | [4.375, 4.792] | +0.083 | [-0.125, +0.292] | 0.4631 | 0.165 |
| Qwen3-32B | Refusal Consistency | 4.250 | [4.000, 4.500] | +0.083 | [-0.125, +0.333] | 0.5002 | 0.143 |
| Qwen3-32B | Mitigation Robustness | 4.792 | [4.625, 4.958] | +0.500 | [+0.250, +0.750] | 0.0064 | 0.758 |
| Qwen3-32B | Evidence Grounding | 4.000 | [3.750, 4.250] | -0.333 | [-0.708, +0.000] | 0.1282 | -0.364 |
| Claude-Sonnet-4 | Calibration | 4.375 | [4.083, 4.625] | +0.042 | [-0.083, +0.167] | 0.5930 | 0.116 |
| Claude-Sonnet-4 | Safe Boundary | 4.500 | [4.208, 4.750] | +0.125 | [-0.083, +0.333] | 0.2733 | 0.233 |
| Claude-Sonnet-4 | Refusal Consistency | 4.167 | [3.917, 4.417] | +0.167 | [+0.000, +0.375] | 0.1088 | 0.346 |
| Claude-Sonnet-4 | Mitigation Robustness | 4.792 | [4.583, 4.958] | +0.792 | [+0.542, +1.042] | 0.0004 | 1.203 |
| Claude-Sonnet-4 | Evidence Grounding | 4.333 | [4.042, 4.583] | +0.167 | [-0.042, +0.458] | 0.2012 | 0.262 |
| Gemini-2.5-Pro | Calibration | 4.292 | [4.000, 4.542] | +0.042 | [-0.167, +0.250] | 0.7353 | 0.076 |
| Gemini-2.5-Pro | Safe Boundary | 4.375 | [4.042, 4.667] | -0.125 | [-0.375, +0.000] | 0.3173 | -0.204 |
| Gemini-2.5-Pro | Refusal Consistency | 4.083 | [3.792, 4.333] | -0.083 | [-0.375, +0.125] | 0.6547 | -0.127 |
| Gemini-2.5-Pro | Mitigation Robustness | 4.708 | [4.458, 4.917] | +0.583 | [+0.250, +0.875] | 0.0066 | 0.752 |
| Gemini-2.5-Pro | Evidence Grounding | 4.042 | [3.667, 4.375] | +0.083 | [-0.292, +0.458] | 0.6726 | 0.086 |

## Friedman Test (Cross-Model Post-Mitigation)

| Metric | Chi-squared | df | p-value |
|--------|------------|-----|---------|
| Calibration | 3.9524 | 5 | 0.5583 |
| Safe Boundary | 3.8750 | 5 | 0.5697 |
| Refusal Consistency | 3.9821 | 5 | 0.5540 |
| Mitigation Robustness | 2.3750 | 5 | 0.7972 |
| Evidence Grounding | 4.0833 | 5 | 0.5394 |

*Note: \* indicates p < 0.05*