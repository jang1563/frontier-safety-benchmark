#!/usr/bin/env python3
"""Domain-family breakdown analysis of benchmark results.

Produces:
- Per-domain-family mean scores (pre/post) and deltas for each model
- Domain-family x model heatmap visualization
- Item-level difficulty and discrimination analysis
- Per-domain mitigation effectiveness comparison

Usage:
    python3 scripts/domain_analysis.py \
        --output-dir results/v0_3/domain_analysis
"""

from __future__ import annotations

import argparse
import csv
import json
import plistlib
import subprocess
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


def _patch_macos_font_probe() -> None:
    """Work around matplotlib font discovery failures on some macOS setups."""
    if sys.platform != "darwin":
        return

    original_check_output = subprocess.check_output
    empty_font_plist = plistlib.dumps([{"_items": []}])

    def safe_check_output(cmd, *args, **kwargs):
        if isinstance(cmd, (list, tuple)) and list(cmd[:3]) == ["system_profiler", "-xml", "SPFontsDataType"]:
            return empty_font_plist
        return original_check_output(cmd, *args, **kwargs)

    subprocess.check_output = safe_check_output


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "results" / "v0_3" / "domain_analysis",
                        help="Output directory.")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Load items
    items = read_jsonl(ROOT / "data_public" / "all_public_items.jsonl")
    item_index = {item["item_id"]: item for item in items}

    # Load all reviewed responses
    # Structure: model -> item_id -> condition -> review dict
    all_reviews: dict[str, dict[str, dict[str, dict]]] = {}

    for model_key, model_label in MODELS:
        path = ROOT / "data_public" / f"reviewed_responses_{model_key}_v0.3.jsonl"
        if not path.exists():
            continue
        all_reviews[model_key] = {}
        for r in read_jsonl(path):
            iid = r["item_id"]
            cond = r["condition"]
            if iid not in all_reviews[model_key]:
                all_reviews[model_key][iid] = {}
            all_reviews[model_key][iid][cond] = r.get("review", {})

    # =========================================================================
    # Domain-family analysis
    # =========================================================================

    domain_families = sorted(set(item["domain_family"] for item in items))
    domain_items = defaultdict(list)
    for item in items:
        domain_items[item["domain_family"]].append(item["item_id"])

    print("=" * 70)
    print("DOMAIN-FAMILY BREAKDOWN ANALYSIS")
    print("=" * 70)

    # Compute per-domain, per-model averages
    # Structure: domain_results[domain][model_key] = {pre_avg, post_avg, delta, per_metric}
    domain_results = {}

    for domain in domain_families:
        domain_results[domain] = {}
        iids = domain_items[domain]

        for model_key, model_label in MODELS:
            if model_key not in all_reviews:
                continue

            pre_scores = defaultdict(list)
            post_scores = defaultdict(list)

            for iid in iids:
                if iid in all_reviews[model_key]:
                    reviews = all_reviews[model_key][iid]
                    pre = reviews.get("pre_mitigation", {})
                    post = reviews.get("post_mitigation", {})
                    for metric in METRICS:
                        if metric in pre:
                            pre_scores[metric].append(pre[metric])
                        if metric in post:
                            post_scores[metric].append(post[metric])

            per_metric = {}
            for metric in METRICS:
                pre_avg = sum(pre_scores[metric]) / len(pre_scores[metric]) if pre_scores[metric] else 0
                post_avg = sum(post_scores[metric]) / len(post_scores[metric]) if post_scores[metric] else 0
                per_metric[metric] = {
                    "pre": round(pre_avg, 3),
                    "post": round(post_avg, 3),
                    "delta": round(post_avg - pre_avg, 3),
                }

            all_pre = [v for metric in METRICS for v in pre_scores[metric]]
            all_post = [v for metric in METRICS for v in post_scores[metric]]
            pre_avg = sum(all_pre) / len(all_pre) if all_pre else 0
            post_avg = sum(all_post) / len(all_post) if all_post else 0

            domain_results[domain][model_key] = {
                "pre_avg": round(pre_avg, 3),
                "post_avg": round(post_avg, 3),
                "delta": round(post_avg - pre_avg, 3),
                "per_metric": per_metric,
                "n_items": len(iids),
            }

    # Print domain results
    for domain in domain_families:
        print(f"\n--- {domain} ({len(domain_items[domain])} items) ---")
        for model_key, model_label in MODELS:
            if model_key in domain_results[domain]:
                dr = domain_results[domain][model_key]
                print(f"  {model_label}: pre={dr['pre_avg']:.3f} post={dr['post_avg']:.3f} delta={dr['delta']:+.3f}")

    # =========================================================================
    # Item difficulty and discrimination
    # =========================================================================

    print(f"\n{'='*70}")
    print("ITEM DIFFICULTY AND DISCRIMINATION")
    print("=" * 70)

    item_stats = []
    for item in items:
        iid = item["item_id"]
        all_pre_scores = []
        all_post_scores = []

        for model_key, _ in MODELS:
            if model_key not in all_reviews or iid not in all_reviews[model_key]:
                continue
            reviews = all_reviews[model_key][iid]
            pre = reviews.get("pre_mitigation", {})
            post = reviews.get("post_mitigation", {})
            for metric in METRICS:
                if metric in pre:
                    all_pre_scores.append(pre[metric])
                if metric in post:
                    all_post_scores.append(post[metric])

        if not all_pre_scores:
            continue

        pre_mean = sum(all_pre_scores) / len(all_pre_scores)
        post_mean = sum(all_post_scores) / len(all_post_scores) if all_post_scores else 0

        # Discrimination = variance across models (higher = more discriminating)
        model_avgs = []
        for model_key, _ in MODELS:
            if model_key not in all_reviews or iid not in all_reviews[model_key]:
                continue
            reviews = all_reviews[model_key][iid]
            post = reviews.get("post_mitigation", {})
            scores = [post.get(m, 0) for m in METRICS if m in post]
            if scores:
                model_avgs.append(sum(scores) / len(scores))

        if len(model_avgs) >= 2:
            mean_avg = sum(model_avgs) / len(model_avgs)
            variance = sum((x - mean_avg) ** 2 for x in model_avgs) / (len(model_avgs) - 1)
        else:
            variance = 0

        item_stats.append({
            "item_id": iid,
            "title": item.get("title", ""),
            "domain_family": item.get("domain_family", ""),
            "reasoning_type": item.get("reasoning_type", ""),
            "difficulty": round(pre_mean, 3),  # Lower pre-mitigation = harder
            "post_mean": round(post_mean, 3),
            "delta": round(post_mean - pre_mean, 3),
            "discrimination": round(variance, 3),  # Higher = more discriminating
        })

    # Sort by difficulty (ascending = hardest first)
    item_stats.sort(key=lambda x: x["difficulty"])

    print(f"\n{'Item ID':<10} {'Difficulty':<12} {'Post-Mit':<10} {'Delta':<8} {'Discrim':<10} {'Domain'}")
    print("-" * 80)
    for ist in item_stats:
        print(f"{ist['item_id']:<10} {ist['difficulty']:<12.3f} {ist['post_mean']:<10.3f} "
              f"{ist['delta']:+<8.3f} {ist['discrimination']:<10.3f} {ist['domain_family']}")

    # =========================================================================
    # Save outputs
    # =========================================================================

    # JSON results
    output = {
        "generated_on": __import__("datetime").date.today().isoformat(),
        "domain_results": domain_results,
        "item_stats": item_stats,
    }
    json_path = args.output_dir / "domain_analysis.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"\nWrote {json_path}")

    # CSV: domain x model table
    csv_path = args.output_dir / "domain_model_table.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        header = ["domain_family", "n_items"]
        for _, model_label in MODELS:
            header.extend([f"{model_label}_pre", f"{model_label}_post", f"{model_label}_delta"])
        writer.writerow(header)
        for domain in domain_families:
            row = [domain, len(domain_items[domain])]
            for model_key, _ in MODELS:
                dr = domain_results[domain].get(model_key, {})
                row.extend([dr.get("pre_avg", ""), dr.get("post_avg", ""), dr.get("delta", "")])
            writer.writerow(row)
    print(f"Wrote {csv_path}")

    # CSV: item difficulty
    item_csv_path = args.output_dir / "item_difficulty.csv"
    with item_csv_path.open("w", encoding="utf-8", newline="") as f:
        fieldnames = ["item_id", "title", "domain_family", "reasoning_type",
                      "difficulty", "post_mean", "delta", "discrimination"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(item_stats)
    print(f"Wrote {item_csv_path}")

    # Markdown summary
    md_path = args.output_dir / "domain_analysis.md"
    lines = [
        "# Domain-Family Breakdown Analysis",
        "",
        f"- Generated on: {output['generated_on']}",
        "",
        "## Mitigation Delta by Domain Family and Model",
        "",
        "| Domain Family | Items |",
    ]

    # Dynamic header
    header = "| Domain Family | Items |"
    sep = "|---------------|-------|"
    for _, model_label in MODELS:
        header += f" {model_label} Delta |"
        sep += "------------|"
    lines = [
        "# Domain-Family Breakdown Analysis",
        "",
        f"- Generated on: {output['generated_on']}",
        "",
        "## Mitigation Delta by Domain Family and Model",
        "",
        header,
        sep,
    ]
    for domain in domain_families:
        short_domain = domain.replace("_", " ").title()
        row = f"| {short_domain} | {len(domain_items[domain])} |"
        for model_key, _ in MODELS:
            dr = domain_results[domain].get(model_key, {})
            delta = dr.get("delta", 0)
            row += f" {delta:+.3f} |"
        lines.append(row)

    lines.extend([
        "",
        "## Hardest Items (lowest pre-mitigation scores)",
        "",
        "| Rank | Item ID | Difficulty | Domain | Reasoning Type |",
        "|------|---------|-----------|--------|----------------|",
    ])
    for i, ist in enumerate(item_stats[:5], 1):
        lines.append(f"| {i} | {ist['item_id']} | {ist['difficulty']:.3f} | "
                     f"{ist['domain_family']} | {ist['reasoning_type']} |")

    lines.extend([
        "",
        "## Most Discriminating Items (highest cross-model variance)",
        "",
        "| Rank | Item ID | Discrimination | Domain | Reasoning Type |",
        "|------|---------|---------------|--------|----------------|",
    ])
    disc_sorted = sorted(item_stats, key=lambda x: x["discrimination"], reverse=True)
    for i, ist in enumerate(disc_sorted[:5], 1):
        lines.append(f"| {i} | {ist['item_id']} | {ist['discrimination']:.3f} | "
                     f"{ist['domain_family']} | {ist['reasoning_type']} |")

    with md_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {md_path}")

    # =========================================================================
    # Generate visualization (domain x model delta heatmap)
    # =========================================================================
    try:
        _patch_macos_font_probe()

        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np

        fig, ax = plt.subplots(figsize=(10, 6))

        model_labels = [ml for _, ml in MODELS if _ in all_reviews]
        model_keys = [mk for mk, _ in MODELS if mk in all_reviews]
        short_domains = [d.replace("_", "\n") for d in domain_families]

        data = []
        for domain in domain_families:
            row = []
            for mk in model_keys:
                dr = domain_results[domain].get(mk, {})
                row.append(dr.get("delta", 0))
            data.append(row)

        data_arr = np.array(data)
        im = ax.imshow(data_arr, cmap="RdYlGn", aspect="auto", vmin=-0.5, vmax=1.0)

        ax.set_xticks(range(len(model_labels)))
        ax.set_xticklabels(model_labels, fontsize=10)
        ax.set_yticks(range(len(domain_families)))
        ax.set_yticklabels(short_domains, fontsize=9)

        # Add text annotations
        for i in range(len(domain_families)):
            for j in range(len(model_labels)):
                val = data_arr[i, j]
                color = "white" if abs(val) > 0.3 else "black"
                ax.text(j, i, f"{val:+.2f}", ha="center", va="center", fontsize=9, color=color)

        plt.colorbar(im, ax=ax, label="Mitigation Delta")
        ax.set_title("Mitigation Delta by Domain Family and Model", fontsize=13, fontweight="bold")
        plt.tight_layout()

        chart_path = args.output_dir / "chart_domain_delta_heatmap.png"
        plt.savefig(chart_path, dpi=200, bbox_inches="tight")
        plt.close()
        print(f"Wrote {chart_path}")

        # Item difficulty bar chart
        fig, ax = plt.subplots(figsize=(12, 5))
        sorted_items = sorted(item_stats, key=lambda x: x["difficulty"])
        ids = [s["item_id"] for s in sorted_items]
        difficulties = [s["difficulty"] for s in sorted_items]
        colors_map = {}
        palette = plt.cm.Set2(range(8))
        for i, d in enumerate(domain_families):
            colors_map[d] = palette[i % 8]
        colors = [colors_map.get(s["domain_family"], "gray") for s in sorted_items]

        bars = ax.bar(range(len(ids)), difficulties, color=colors)
        ax.set_xticks(range(len(ids)))
        ax.set_xticklabels(ids, rotation=45, ha="right", fontsize=8)
        ax.set_ylabel("Difficulty (mean pre-mitigation score)")
        ax.set_title("Item Difficulty Ranking (lower = harder)", fontsize=13, fontweight="bold")
        ax.axhline(y=sum(difficulties) / len(difficulties), color="gray", linestyle="--", alpha=0.7)

        # Legend
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor=colors_map[d], label=d.replace("_", " "))
                          for d in domain_families if d in colors_map]
        ax.legend(handles=legend_elements, fontsize=7, loc="lower right")
        plt.tight_layout()

        chart_path2 = args.output_dir / "chart_item_difficulty.png"
        plt.savefig(chart_path2, dpi=200, bbox_inches="tight")
        plt.close()
        print(f"Wrote {chart_path2}")

    except ImportError:
        print("matplotlib not available; skipping visualizations.")


if __name__ == "__main__":
    main()
