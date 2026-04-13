#!/usr/bin/env python3
"""Statistical analysis of benchmark results with bootstrap CIs and significance tests.

Produces:
- Bootstrap 95% confidence intervals for all means and deltas
- Wilcoxon signed-rank tests for pre vs. post mitigation (per model)
- Friedman test across models on post-mitigation scores
- Effect sizes (rank-biserial correlation)

Usage:
    python3 scripts/statistical_analysis.py \
        --output-dir results/v0_3/statistics
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

METRICS = [
    "calibration_score",
    "safe_boundary_score",
    "refusal_consistency_score",
    "mitigation_robustness_score",
    "evidence_grounding_score",
]

MODELS = [
    ("gpt4o", "GPT-4o"),
    ("deepseek", "DeepSeek-V3"),
    ("llama", "Llama-3.3-70B"),
    ("qwen", "Qwen3-32B"),
    ("claude", "Claude-Sonnet-4"),
    ("gemini", "Gemini-2.5-Pro"),
]


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def bootstrap_ci(values: list[float], n_boot: int = 10000, ci: float = 0.95,
                 seed: int = 42) -> tuple[float, float, float]:
    """Compute bootstrap mean and CI."""
    rng = random.Random(seed)
    n = len(values)
    if n == 0:
        return 0.0, 0.0, 0.0
    means = []
    for _ in range(n_boot):
        sample = [rng.choice(values) for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    alpha = (1 - ci) / 2
    lo = means[int(alpha * n_boot)]
    hi = means[int((1 - alpha) * n_boot)]
    point = sum(values) / n
    return point, lo, hi


def wilcoxon_signed_rank(pre: list[float], post: list[float]) -> dict:
    """Wilcoxon signed-rank test (two-sided) without scipy.

    Returns W statistic, approximate z-score, and p-value.
    Uses normal approximation for n >= 10.
    """
    import math

    diffs = [(post[i] - pre[i]) for i in range(len(pre))]
    # Remove zeros
    nonzero = [(abs(d), 1 if d > 0 else -1, d) for d in diffs if d != 0]
    n = len(nonzero)

    if n == 0:
        return {"W": 0, "z": 0.0, "p_value": 1.0, "n_nonzero": 0}

    # Rank by absolute value
    nonzero.sort(key=lambda x: x[0])

    # Assign ranks with tied-rank averaging
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j < n and nonzero[j][0] == nonzero[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0  # 1-indexed average
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j

    # Sum of positive ranks
    W_plus = sum(ranks[k] for k in range(n) if nonzero[k][1] > 0)
    W_minus = sum(ranks[k] for k in range(n) if nonzero[k][1] < 0)
    W = min(W_plus, W_minus)

    # Normal approximation
    mu = n * (n + 1) / 4.0
    sigma = math.sqrt(n * (n + 1) * (2 * n + 1) / 24.0)

    if sigma == 0:
        return {"W": W, "z": 0.0, "p_value": 1.0, "n_nonzero": n,
                "W_plus": W_plus, "W_minus": W_minus}

    z = (W - mu) / sigma
    # Two-sided p-value using normal approximation
    p_value = 2 * (1 - _norm_cdf(abs(z)))

    return {
        "W": W,
        "W_plus": W_plus,
        "W_minus": W_minus,
        "z": round(z, 4),
        "p_value": round(p_value, 6),
        "n_nonzero": n,
    }


def _norm_cdf(x: float) -> float:
    """Standard normal CDF approximation (Abramowitz & Stegun)."""
    import math
    if x < 0:
        return 1.0 - _norm_cdf(-x)
    t = 1.0 / (1.0 + 0.2316419 * x)
    d = 0.3989422804014327  # 1/sqrt(2*pi)
    poly = ((((1.330274429 * t - 1.821255978) * t + 1.781477937) * t
             - 0.356563782) * t + 0.319381530) * t
    return 1.0 - d * math.exp(-0.5 * x * x) * poly


def friedman_test(data: dict[str, list[float]]) -> dict:
    """Friedman test across models for repeated measures.

    data: {model_label: [scores per item]} — all lists must have same length.
    """
    import math

    model_names = list(data.keys())
    k = len(model_names)
    n = len(data[model_names[0]])

    if k < 2 or n < 2:
        return {"chi2": 0.0, "p_value": 1.0, "k": k, "n": n}

    # Rank within each item (row)
    rank_sums = {m: 0.0 for m in model_names}
    for i in range(n):
        row = [(data[m][i], m) for m in model_names]
        row.sort(key=lambda x: x[0])
        # Assign ranks with tie averaging
        j = 0
        while j < k:
            jj = j
            while jj < k and row[jj][0] == row[j][0]:
                jj += 1
            avg_rank = (j + 1 + jj) / 2.0
            for kk in range(j, jj):
                rank_sums[row[kk][1]] += avg_rank
            j = jj

    # Friedman statistic
    total = sum(rs ** 2 for rs in rank_sums.values())
    chi2 = (12.0 / (n * k * (k + 1))) * total - 3 * n * (k + 1)

    # Chi-squared p-value approximation (df = k-1)
    df = k - 1
    p_value = _chi2_survival(chi2, df)

    return {
        "chi2": round(chi2, 4),
        "df": df,
        "p_value": round(p_value, 6),
        "k": k,
        "n": n,
        "rank_sums": {m: round(v, 2) for m, v in rank_sums.items()},
    }


def _chi2_survival(x: float, df: int) -> float:
    """Approximate chi-squared survival function using Wilson-Hilferty."""
    import math
    if x <= 0:
        return 1.0
    if df <= 0:
        return 0.0
    # Wilson-Hilferty approximation
    z = ((x / df) ** (1.0 / 3.0) - (1.0 - 2.0 / (9.0 * df))) / math.sqrt(2.0 / (9.0 * df))
    return 1.0 - _norm_cdf(z)


def rank_biserial(pre: list[float], post: list[float]) -> float:
    """Rank-biserial correlation as effect size for Wilcoxon test."""
    diffs = [post[i] - pre[i] for i in range(len(pre))]
    nonzero = [d for d in diffs if d != 0]
    n = len(nonzero)
    if n == 0:
        return 0.0
    pos = sum(1 for d in nonzero if d > 0)
    neg = sum(1 for d in nonzero if d < 0)
    return (pos - neg) / n


def cohens_d(pre: list[float], post: list[float]) -> float:
    """Cohen's d for paired samples."""
    import math
    diffs = [post[i] - pre[i] for i in range(len(pre))]
    n = len(diffs)
    if n < 2:
        return 0.0
    mean_d = sum(diffs) / n
    var_d = sum((d - mean_d) ** 2 for d in diffs) / (n - 1)
    sd_d = math.sqrt(var_d) if var_d > 0 else 1e-10
    return mean_d / sd_d


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "results" / "v0_3" / "statistics",
                        help="Directory for statistical output files.")
    parser.add_argument("--n-boot", type=int, default=10000,
                        help="Number of bootstrap resamples.")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Load all reviewed responses
    all_data: dict[str, dict[str, dict[str, list[float]]]] = {}
    # Structure: all_data[model_key][condition][metric] = [scores per item]

    item_ids = None

    for model_key, model_label in MODELS:
        reviewed_path = ROOT / "data_public" / f"reviewed_responses_{model_key}_v0.3.jsonl"
        if not reviewed_path.exists():
            print(f"Skipping {model_key}: not found.")
            continue

        responses = read_jsonl(reviewed_path)

        # Index by condition and item
        pre_by_item: dict[str, dict] = {}
        post_by_item: dict[str, dict] = {}

        for r in responses:
            review = r.get("review", {})
            if r["condition"] == "pre_mitigation":
                pre_by_item[r["item_id"]] = review
            else:
                post_by_item[r["item_id"]] = review

        # Get consistent item ordering
        if item_ids is None:
            item_ids = sorted(set(pre_by_item.keys()) & set(post_by_item.keys()))

        all_data[model_key] = {
            "pre_mitigation": {},
            "post_mitigation": {},
        }
        for metric in METRICS:
            all_data[model_key]["pre_mitigation"][metric] = [
                pre_by_item[iid].get(metric, 0) for iid in item_ids
            ]
            all_data[model_key]["post_mitigation"][metric] = [
                post_by_item[iid].get(metric, 0) for iid in item_ids
            ]

    if not all_data:
        print("No data found.")
        sys.exit(1)

    results = {
        "generated_on": __import__("datetime").date.today().isoformat(),
        "n_items": len(item_ids),
        "n_bootstrap": args.n_boot,
        "models": {},
    }

    # =========================================================================
    # Per-model analysis
    # =========================================================================

    print("=" * 70)
    print("STATISTICAL ANALYSIS OF BENCHMARK RESULTS")
    print("=" * 70)

    for model_key, model_label in MODELS:
        if model_key not in all_data:
            continue

        print(f"\n--- {model_label} ---")
        model_result = {
            "model_label": model_label,
            "bootstrap_ci": {},
            "wilcoxon": {},
            "effect_sizes": {},
        }

        for metric in METRICS:
            pre_vals = all_data[model_key]["pre_mitigation"][metric]
            post_vals = all_data[model_key]["post_mitigation"][metric]
            delta_vals = [post_vals[i] - pre_vals[i] for i in range(len(item_ids))]

            # Bootstrap CIs
            pre_mean, pre_lo, pre_hi = bootstrap_ci(pre_vals, args.n_boot)
            post_mean, post_lo, post_hi = bootstrap_ci(post_vals, args.n_boot)
            delta_mean, delta_lo, delta_hi = bootstrap_ci(delta_vals, args.n_boot)

            model_result["bootstrap_ci"][metric] = {
                "pre": {"mean": round(pre_mean, 3), "ci_lo": round(pre_lo, 3), "ci_hi": round(pre_hi, 3)},
                "post": {"mean": round(post_mean, 3), "ci_lo": round(post_lo, 3), "ci_hi": round(post_hi, 3)},
                "delta": {"mean": round(delta_mean, 3), "ci_lo": round(delta_lo, 3), "ci_hi": round(delta_hi, 3)},
            }

            # Wilcoxon
            wtest = wilcoxon_signed_rank(pre_vals, post_vals)
            model_result["wilcoxon"][metric] = wtest

            # Effect sizes
            d = cohens_d(pre_vals, post_vals)
            rb = rank_biserial(pre_vals, post_vals)
            model_result["effect_sizes"][metric] = {
                "cohens_d": round(d, 3),
                "rank_biserial": round(rb, 3),
            }

            sig = "*" if wtest["p_value"] < 0.05 else ""
            print(f"  {metric}:")
            print(f"    Post-mit: {post_mean:.3f} [{post_lo:.3f}, {post_hi:.3f}]")
            print(f"    Delta:    {delta_mean:+.3f} [{delta_lo:+.3f}, {delta_hi:+.3f}]")
            print(f"    Wilcoxon: W={wtest['W']}, z={wtest['z']}, p={wtest['p_value']}{sig}")
            print(f"    Cohen's d={d:.3f}, rank-biserial={rb:.3f}")

        # Overall delta
        overall_pre = []
        overall_post = []
        for metric in METRICS:
            overall_pre.extend(all_data[model_key]["pre_mitigation"][metric])
            overall_post.extend(all_data[model_key]["post_mitigation"][metric])
        overall_delta = [overall_post[i] - overall_pre[i] for i in range(len(overall_pre))]
        _, d_lo, d_hi = bootstrap_ci(overall_delta, args.n_boot)
        d_mean = sum(overall_delta) / len(overall_delta)
        model_result["overall_delta_ci"] = {
            "mean": round(d_mean, 3), "ci_lo": round(d_lo, 3), "ci_hi": round(d_hi, 3)
        }
        print(f"  Overall delta: {d_mean:+.3f} [{d_lo:+.3f}, {d_hi:+.3f}]")

        results["models"][model_key] = model_result

    # =========================================================================
    # Cross-model Friedman test
    # =========================================================================

    print(f"\n--- Cross-Model Friedman Test ---")
    friedman_results = {}
    for metric in METRICS:
        data_for_friedman = {}
        for model_key, model_label in MODELS:
            if model_key in all_data:
                data_for_friedman[model_label] = all_data[model_key]["post_mitigation"][metric]

        if len(data_for_friedman) >= 2:
            ftest = friedman_test(data_for_friedman)
            friedman_results[metric] = ftest
            sig = "*" if ftest["p_value"] < 0.05 else ""
            print(f"  {metric}: chi2={ftest['chi2']}, df={ftest['df']}, p={ftest['p_value']}{sig}")
        else:
            friedman_results[metric] = {"chi2": 0, "p_value": 1.0}

    results["friedman_tests"] = friedman_results

    # =========================================================================
    # Save results
    # =========================================================================

    json_path = args.output_dir / "statistical_analysis.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {json_path}")

    # Generate markdown summary
    md_path = args.output_dir / "statistical_analysis.md"
    lines = [
        "# Statistical Analysis Summary",
        "",
        f"- Generated on: {results['generated_on']}",
        f"- Items: {results['n_items']}",
        f"- Bootstrap resamples: {results['n_bootstrap']}",
        "",
    ]

    # Summary table
    lines.append("## Post-Mitigation Means with 95% Bootstrap CIs")
    lines.append("")
    lines.append("| Model | Metric | Mean | 95% CI | Delta | Delta CI | Wilcoxon p | Cohen's d |")
    lines.append("|-------|--------|------|--------|-------|----------|-----------|-----------|")

    for model_key, model_label in MODELS:
        if model_key not in results["models"]:
            continue
        mr = results["models"][model_key]
        for metric in METRICS:
            bc = mr["bootstrap_ci"][metric]
            wt = mr["wilcoxon"][metric]
            es = mr["effect_sizes"][metric]
            short_metric = metric.replace("_score", "").replace("_", " ").title()
            lines.append(
                f"| {model_label} | {short_metric} | "
                f"{bc['post']['mean']:.3f} | [{bc['post']['ci_lo']:.3f}, {bc['post']['ci_hi']:.3f}] | "
                f"{bc['delta']['mean']:+.3f} | [{bc['delta']['ci_lo']:+.3f}, {bc['delta']['ci_hi']:+.3f}] | "
                f"{wt['p_value']:.4f} | {es['cohens_d']:.3f} |"
            )

    lines.append("")
    lines.append("## Friedman Test (Cross-Model Post-Mitigation)")
    lines.append("")
    lines.append("| Metric | Chi-squared | df | p-value |")
    lines.append("|--------|------------|-----|---------|")
    for metric in METRICS:
        ft = friedman_results.get(metric, {})
        short_metric = metric.replace("_score", "").replace("_", " ").title()
        lines.append(f"| {short_metric} | {ft.get('chi2', 0):.4f} | {ft.get('df', 0)} | {ft.get('p_value', 1):.4f} |")

    lines.append("")
    lines.append("*Note: \\* indicates p < 0.05*")

    with md_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {md_path}")

    # Generate LaTeX table fragment for the paper
    tex_path = args.output_dir / "results_table_with_ci.tex"
    tex_lines = [
        "% Auto-generated table with bootstrap CIs",
        "\\begin{table}[t]",
        "\\centering",
        "\\caption{Post-mitigation metric averages with 95\\% bootstrap confidence intervals and mitigation deltas across models. $\\uparrow$ indicates higher is better. Significance from Wilcoxon signed-rank tests: * $p<0.05$, ** $p<0.01$.}",
        "\\label{tab:main_results_ci}",
        "\\small",
        "\\begin{tabular}{@{}lccccccc@{}}",
        "\\toprule",
        "\\textbf{Model} & \\textbf{Cal.}$\\uparrow$ & \\textbf{Safe}$\\uparrow$ & \\textbf{Ref.}$\\uparrow$ & \\textbf{Mit.}$\\uparrow$ & \\textbf{Evid.}$\\uparrow$ & \\textbf{Avg.}$\\uparrow$ & $\\boldsymbol{\\Delta}$ \\\\",
        "\\midrule",
    ]

    for model_key, model_label in MODELS:
        if model_key not in results["models"]:
            continue
        mr = results["models"][model_key]
        cells = []
        for metric in METRICS:
            bc = mr["bootstrap_ci"][metric]
            wt = mr["wilcoxon"][metric]
            sig = ""
            if wt["p_value"] < 0.01:
                sig = "**"
            elif wt["p_value"] < 0.05:
                sig = "*"
            cells.append(f"{bc['post']['mean']:.2f}{sig}")

        # Overall avg and delta
        post_avg = sum(mr["bootstrap_ci"][m]["post"]["mean"] for m in METRICS) / len(METRICS)
        delta_avg = mr["overall_delta_ci"]["mean"]
        delta_ci = f"[{mr['overall_delta_ci']['ci_lo']:+.2f}, {mr['overall_delta_ci']['ci_hi']:+.2f}]"

        row = f"{model_label} & {' & '.join(cells)} & {post_avg:.2f} & {delta_avg:+.2f} \\\\"
        tex_lines.append(row)

    tex_lines.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table}",
    ])

    with tex_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(tex_lines))
    print(f"Wrote {tex_path}")


if __name__ == "__main__":
    main()
