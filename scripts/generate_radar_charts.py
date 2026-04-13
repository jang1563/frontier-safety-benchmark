#!/usr/bin/env python3
"""Generate radar/spider charts showing each model's 5-metric safety profile.

Produces publication-ready radar charts comparing pre vs. post-mitigation
safety profiles across all evaluated models.

Usage:
    python3 scripts/generate_radar_charts.py \
        --output-dir results/v0_3/charts
"""

from __future__ import annotations

import argparse
import json
import math
import plistlib
import subprocess
import sys
from pathlib import Path


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


_patch_macos_font_probe()

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

METRICS = [
    "calibration_score",
    "safe_boundary_score",
    "refusal_consistency_score",
    "mitigation_robustness_score",
    "evidence_grounding_score",
]

METRIC_SHORT = [
    "Calibration",
    "Safe\nBoundary",
    "Refusal\nConsistency",
    "Mitigation\nRobustness",
    "Evidence\nGrounding",
]

MODELS = [
    ("gpt4o", "GPT-4o", "#1f77b4"),
    ("claude", "Claude-Sonnet-4", "#9467bd"),
    ("gemini", "Gemini-2.5-Pro", "#8c564b"),
    ("deepseek", "DeepSeek-V3", "#ff7f0e"),
    ("llama", "Llama-3.3-70B", "#2ca02c"),
    ("qwen", "Qwen3-32B", "#d62728"),
]


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def compute_metric_averages(responses: list[dict]) -> dict[str, dict[str, float]]:
    """Compute per-condition metric averages from reviewed responses."""
    from collections import defaultdict

    sums: dict[str, dict[str, float]] = {"pre_mitigation": {m: 0 for m in METRICS},
                                          "post_mitigation": {m: 0 for m in METRICS}}
    counts: dict[str, dict[str, int]] = {"pre_mitigation": {m: 0 for m in METRICS},
                                          "post_mitigation": {m: 0 for m in METRICS}}

    for r in responses:
        cond = r["condition"]
        review = r.get("review", {})
        for m in METRICS:
            val = review.get(m)
            if val is not None:
                sums[cond][m] += val
                counts[cond][m] += 1

    result = {}
    for cond in ["pre_mitigation", "post_mitigation"]:
        result[cond] = {}
        for m in METRICS:
            if counts[cond][m] > 0:
                result[cond][m] = sums[cond][m] / counts[cond][m]
            else:
                result[cond][m] = 0
    return result


def radar_chart(ax, values_list, labels, metric_labels, title, colors, alphas=None):
    """Draw a radar chart on the given axes."""
    N = len(metric_labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_rlabel_position(0)
    ax.set_ylim(1, 5)
    ax.set_yticks([2, 3, 4, 5])
    ax.set_yticklabels(["2", "3", "4", "5"], fontsize=7, color="gray")

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metric_labels, fontsize=8)

    for i, (vals, label, color) in enumerate(zip(values_list, labels, colors)):
        data = [vals[m] for m in METRICS]
        data += data[:1]
        alpha = alphas[i] if alphas else 0.25
        ax.plot(angles, data, "o-", linewidth=1.5, label=label, color=color, markersize=4)
        ax.fill(angles, data, alpha=alpha, color=color)

    ax.set_title(title, fontsize=11, fontweight="bold", pad=15)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15), fontsize=7)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output-dir", type=Path,
                        default=ROOT / "results" / "v0_3" / "charts",
                        help="Output directory for charts.")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    model_data = {}
    available_models = []
    for model_key, model_label, color in MODELS:
        path = ROOT / "data_public" / f"reviewed_responses_{model_key}_v0.3.jsonl"
        if not path.exists():
            continue
        responses = read_jsonl(path)
        avgs = compute_metric_averages(responses)
        model_data[model_key] = avgs
        available_models.append((model_key, model_label, color))

    if not model_data:
        print("No reviewed response files found.")
        return

    # =========================================================================
    # Chart 1: Per-model radar (pre vs post)
    # =========================================================================
    n_models = len(available_models)
    cols = min(3, n_models)
    rows = math.ceil(n_models / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows),
                             subplot_kw=dict(projection="polar"))
    if n_models == 1:
        axes = np.array([axes])
    axes = axes.flatten()

    for i, (mk, ml, color) in enumerate(available_models):
        pre_vals = model_data[mk]["pre_mitigation"]
        post_vals = model_data[mk]["post_mitigation"]
        radar_chart(axes[i],
                    [pre_vals, post_vals],
                    ["Pre-mitigation", "Post-mitigation"],
                    METRIC_SHORT,
                    ml,
                    [color, color],
                    alphas=[0.1, 0.3])

    # Hide unused axes
    for i in range(n_models, len(axes)):
        axes[i].set_visible(False)

    fig.suptitle("Model Safety Profiles: Pre vs. Post-Mitigation",
                 fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()

    path1 = args.output_dir / "chart_radar_per_model.png"
    plt.savefig(path1, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Wrote {path1}")

    # =========================================================================
    # Chart 2: All models comparison (post-mitigation only)
    # =========================================================================
    fig, ax = plt.subplots(1, 1, figsize=(8, 8), subplot_kw=dict(projection="polar"))

    post_vals_list = [model_data[mk]["post_mitigation"] for mk, _, _ in available_models]
    labels = [ml for _, ml, _ in available_models]
    colors = [c for _, _, c in available_models]

    radar_chart(ax, post_vals_list, labels, METRIC_SHORT,
                "Post-Mitigation Safety Profiles (All Models)", colors)

    plt.tight_layout()
    path2 = args.output_dir / "chart_radar_all_models.png"
    plt.savefig(path2, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Wrote {path2}")


if __name__ == "__main__":
    main()
