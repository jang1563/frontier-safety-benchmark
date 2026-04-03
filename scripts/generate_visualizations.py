#!/usr/bin/env python3
"""Generate visualizations from v0.2 audit CSV data.

Reads audit_slice_overview.csv and audit_longitudinal_comparison.csv
and produces publication-ready charts for the portfolio and release package.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------

COLORS = {
    "demo-model-v0.2": "#2196F3",
    "strict-model-v0.2": "#FF9800",
}
PRE_COLOR = "#E57373"
POST_COLOR = "#66BB6A"
DELTA_COLOR = "#7E57C2"


def model_color(model_name: str) -> str:
    return COLORS.get(model_name, "#9E9E9E")


# ---------------------------------------------------------------------------
# Chart 1: Pre vs Post Mitigation Quality by Model and Slice
# ---------------------------------------------------------------------------

def chart_pre_post_quality(rows: list[dict[str, str]], output_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(12, 5))

    labels = []
    pre_vals = []
    post_vals = []
    for row in rows:
        label = f"{row['model_name'].replace('-v0.2', '')}\n{row['slice_label'].replace('public_', '').replace('_audit', '')}"
        labels.append(label)
        pre_vals.append(float(row["pre_metric_average"]))
        post_vals.append(float(row["post_metric_average"]))

    x = np.arange(len(labels))
    width = 0.35

    bars_pre = ax.bar(x - width / 2, pre_vals, width, label="Pre-mitigation", color=PRE_COLOR, edgecolor="white", linewidth=0.5)
    bars_post = ax.bar(x + width / 2, post_vals, width, label="Post-mitigation", color=POST_COLOR, edgecolor="white", linewidth=0.5)

    ax.set_ylabel("Average Metric Score (1-5)", fontsize=11)
    ax.set_title("Pre- vs Post-Mitigation Quality Across Audit Slices", fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0, 5.5)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.legend(loc="upper left", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar in bars_pre:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.08,
                f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=7, color="#555")
    for bar in bars_post:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.08,
                f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=7, color="#555")

    plt.tight_layout()
    out = output_dir / "chart_pre_post_quality.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# Chart 2: Error Tag Reduction
# ---------------------------------------------------------------------------

def chart_error_tag_reduction(rows: list[dict[str, str]], output_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(12, 5))

    labels = []
    pre_tags = []
    post_tags = []
    for row in rows:
        label = f"{row['model_name'].replace('-v0.2', '')}\n{row['slice_label'].replace('public_', '').replace('_audit', '')}"
        labels.append(label)
        pre_tags.append(int(row["pre_error_tag_total"]))
        post_tags.append(int(row["post_error_tag_total"]))

    x = np.arange(len(labels))
    width = 0.35

    ax.bar(x - width / 2, pre_tags, width, label="Pre-mitigation", color=PRE_COLOR, edgecolor="white", linewidth=0.5)
    ax.bar(x + width / 2, post_tags, width, label="Post-mitigation", color=POST_COLOR, edgecolor="white", linewidth=0.5)

    ax.set_ylabel("Total Error Tags", fontsize=11)
    ax.set_title("Error Tag Counts: Pre- vs Post-Mitigation", fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.legend(loc="upper right", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for i, (pre, post) in enumerate(zip(pre_tags, post_tags)):
        ax.text(x[i] - width / 2, pre + 0.3, str(pre), ha="center", va="bottom", fontsize=8, color="#555")
        ax.text(x[i] + width / 2, post + 0.3, str(post), ha="center", va="bottom", fontsize=8, color="#555")

    plt.tight_layout()
    out = output_dir / "chart_error_tag_reduction.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# Chart 3: Mitigation Delta by Model
# ---------------------------------------------------------------------------

def chart_mitigation_delta(rows: list[dict[str, str]], output_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(10, 5))

    labels = []
    deltas = []
    colors = []
    for row in rows:
        label = f"{row['model_name'].replace('-v0.2', '')}\n{row['slice_label'].replace('public_', '').replace('_audit', '')}"
        labels.append(label)
        deltas.append(float(row["overall_delta_average"]))
        colors.append(model_color(row["model_name"]))

    x = np.arange(len(labels))
    bars = ax.bar(x, deltas, 0.6, color=colors, edgecolor="white", linewidth=0.5)

    ax.set_ylabel("Average Delta (Post - Pre)", fontsize=11)
    ax.set_title("Mitigation Improvement Delta by Model and Slice", fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.axhline(0, color="#999", linewidth=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar, delta in zip(bars, deltas):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.03,
                f"{delta:+.3f}", ha="center", va="bottom", fontsize=8, color="#333")

    # Manual legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, label=m) for m, c in COLORS.items()]
    ax.legend(handles=legend_elements, loc="upper right", fontsize=9)

    plt.tight_layout()
    out = output_dir / "chart_mitigation_delta.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# Chart 4: Longitudinal Post-Mitigation Quality
# ---------------------------------------------------------------------------

def chart_longitudinal_quality(long_rows: list[dict[str, str]], output_dir: Path) -> Path:
    fig, ax = plt.subplots(figsize=(10, 5))

    grouped: dict[str, list[dict[str, str]]] = {}
    for row in long_rows:
        key = f"{row['scope']} / {row['model_name']}"
        grouped.setdefault(key, []).append(row)

    bar_labels = []
    bar_from = []
    bar_to = []
    bar_colors = []

    for key, entries in sorted(grouped.items()):
        for entry in entries:
            short_scope = entry["scope"].replace("public_", "")
            short_model = entry["model_name"].replace("-v0.2", "")
            bar_labels.append(f"{short_model}\n{short_scope}")
            bar_from.append(float(entry["from_post_metric_average"]))
            bar_to.append(float(entry["to_post_metric_average"]))
            bar_colors.append(model_color(entry["model_name"]))

    x = np.arange(len(bar_labels))
    width = 0.35

    ax.bar(x - width / 2, bar_from, width, label="Slice A (earlier)", color="#BBDEFB", edgecolor="white", linewidth=0.5)
    ax.bar(x + width / 2, bar_to, width, label="Slice B (later)", color="#1565C0", edgecolor="white", linewidth=0.5)

    ax.set_ylabel("Post-Mitigation Average (1-5)", fontsize=11)
    ax.set_title("Longitudinal Post-Mitigation Quality: Slice A vs Slice B", fontsize=13, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(bar_labels, fontsize=9)
    ax.set_ylim(3.5, 5.2)
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax.legend(loc="lower right", fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for i, (f, t) in enumerate(zip(bar_from, bar_to)):
        ax.text(x[i] - width / 2, f + 0.03, f"{f:.3f}", ha="center", va="bottom", fontsize=7, color="#555")
        ax.text(x[i] + width / 2, t + 0.03, f"{t:.3f}", ha="center", va="bottom", fontsize=7, color="#555")

    plt.tight_layout()
    out = output_dir / "chart_longitudinal_quality.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# Chart 5: Cross-Model Radar / Summary Heatmap
# ---------------------------------------------------------------------------

def chart_model_comparison_heatmap(rows: list[dict[str, str]], output_dir: Path) -> Path:
    """Simple heatmap: rows = (model, slice), columns = key metrics."""
    import matplotlib.colors as mcolors

    metric_cols = ["pre_metric_average", "post_metric_average", "overall_delta_average"]
    col_labels = ["Pre Avg", "Post Avg", "Delta Avg"]
    row_labels = []
    data = []

    for row in rows:
        short = f"{row['model_name'].replace('-v0.2', '')} | {row['slice_label'].replace('public_', '').replace('_audit', '')}"
        row_labels.append(short)
        data.append([float(row[c]) for c in metric_cols])

    data_arr = np.array(data)
    fig, ax = plt.subplots(figsize=(7, max(4, len(row_labels) * 0.6 + 1)))

    cmap = plt.cm.RdYlGn
    norm = mcolors.Normalize(vmin=0, vmax=5)
    im = ax.imshow(data_arr, cmap=cmap, norm=norm, aspect="auto")

    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_xticklabels(col_labels, fontsize=10)
    ax.set_yticks(np.arange(len(row_labels)))
    ax.set_yticklabels(row_labels, fontsize=9)

    for i in range(len(row_labels)):
        for j in range(len(col_labels)):
            val = data_arr[i, j]
            text_color = "white" if val < 2 else "black"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=10, color=text_color)

    ax.set_title("Model Performance Heatmap", fontsize=13, fontweight="bold")
    fig.colorbar(im, ax=ax, label="Score (0-5)", shrink=0.8)

    plt.tight_layout()
    out = output_dir / "chart_model_heatmap.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--slice-overview",
        type=Path,
        required=True,
        help="Path to audit_slice_overview.csv",
    )
    parser.add_argument(
        "--longitudinal",
        type=Path,
        required=True,
        help="Path to audit_longitudinal_comparison.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for chart output files.",
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    overview_rows = read_csv(args.slice_overview)
    long_rows = read_csv(args.longitudinal)

    paths = []
    paths.append(chart_pre_post_quality(overview_rows, args.output_dir))
    paths.append(chart_error_tag_reduction(overview_rows, args.output_dir))
    paths.append(chart_mitigation_delta(overview_rows, args.output_dir))
    paths.append(chart_longitudinal_quality(long_rows, args.output_dir))
    paths.append(chart_model_comparison_heatmap(overview_rows, args.output_dir))

    for p in paths:
        print(f"Wrote {p}")


if __name__ == "__main__":
    main()
