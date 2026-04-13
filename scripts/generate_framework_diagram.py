#!/usr/bin/env python3
"""Generate framework architecture diagram as PNG using matplotlib.

Produces a publication-quality diagram showing the three-layer architecture:
1. Taxonomy & Item Design (public/restricted split)
2. Scoring & Auditing (pre/post mitigation, 5 metrics)
3. Release Governance (versioning, integrity, provenance)
"""

import plistlib
import subprocess
import sys


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
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

def draw_rounded_box(ax, xy, width, height, text, facecolor, edgecolor="black",
                     fontsize=9, fontweight="normal", alpha=0.9, lw=1.5, text_color="black"):
    """Draw a rounded box with centered text."""
    x, y = xy
    box = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.1",
                          facecolor=facecolor, edgecolor=edgecolor, alpha=alpha, lw=lw)
    ax.add_patch(box)
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center",
            fontsize=fontsize, fontweight=fontweight, color=text_color,
            linespacing=1.3)


def draw_arrow(ax, start, end, color="black", style="-", lw=1.5):
    """Draw an arrow from start to end."""
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="->", color=color, lw=lw,
                               linestyle=style))


def main():
    fig, ax = plt.subplots(1, 1, figsize=(11, 8))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)
    ax.axis("off")

    # Colors
    pub_color = "#81C784"    # Green for public
    res_color = "#EF9A9A"    # Red for restricted
    score_color = "#90CAF9"  # Blue for scoring
    gov_color = "#FFB74D"    # Orange for governance
    bg_light = "#F5F5F5"
    bg_mid = "#EEEEEE"

    # =========================================================================
    # Layer 1: Taxonomy & Item Design
    # =========================================================================
    layer1_bg = FancyBboxPatch((0.3, 5.8), 10.4, 2.4, boxstyle="round,pad=0.15",
                                facecolor=bg_light, edgecolor="#888888", lw=1.5, linestyle="--")
    ax.add_patch(layer1_bg)
    ax.text(0.7, 8.0, "Layer 1: Taxonomy & Item Design", fontsize=11,
            fontweight="bold", color="#555555")

    # Public items box
    draw_rounded_box(ax, (1.0, 6.6), 3.5, 1.0,
                     "Public Items\n(24 items, 6 domains × 6 types)",
                     pub_color, fontsize=9, fontweight="bold")

    # Restricted items box
    draw_rounded_box(ax, (6.5, 6.6), 3.5, 1.0,
                     "Restricted Items\n(governed access only)",
                     res_color, fontsize=9, fontweight="bold")

    # Sub-labels
    ax.text(2.75, 6.25, "Public-safe, non-operational", ha="center", fontsize=7,
            color="#388E3C", style="italic")
    ax.text(8.25, 6.25, "Operationally sensitive (withheld)", ha="center", fontsize=7,
            color="#C62828", style="italic")

    # =========================================================================
    # Layer 2: Scoring & Auditing
    # =========================================================================
    layer2_bg = FancyBboxPatch((0.3, 2.6), 10.4, 2.9, boxstyle="round,pad=0.15",
                                facecolor=bg_mid, edgecolor="#888888", lw=1.5, linestyle="--")
    ax.add_patch(layer2_bg)
    ax.text(0.7, 5.25, "Layer 2: Scoring & Auditing", fontsize=11,
            fontweight="bold", color="#555555")

    # Models box
    draw_rounded_box(ax, (0.5, 3.8), 2.0, 1.2,
                     "6 Models\nGPT-4o\nClaude\nGemini\nDeepSeek\nLlama\nQwen",
                     "#E0E0E0", fontsize=7, edgecolor="#757575")

    # Pre-mitigation
    draw_rounded_box(ax, (3.0, 4.2), 2.5, 0.8,
                     "Pre-Mitigation\n(no system prompt)",
                     "#BBDEFB", fontsize=8, fontweight="bold")

    # Post-mitigation
    draw_rounded_box(ax, (6.0, 4.2), 2.5, 0.8,
                     "Post-Mitigation\n(safety system prompt)",
                     "#BBDEFB", fontsize=8, fontweight="bold")

    # LLM judge
    draw_rounded_box(ax, (9.0, 4.2), 1.5, 0.8,
                     "LLM-as-\nJudge",
                     "#CE93D8", fontsize=8, fontweight="bold")

    # Scoring metrics box
    draw_rounded_box(ax, (2.5, 3.0), 6.5, 0.8,
                     "5 Metrics (Calibration · Safe Boundary · Refusal · Mitigation Robustness · Evidence)"
                     "\n6 Error Tags  ·  Δₘ = s̄ᵖᵒˢᵗ − s̄ᵖʳᵉ  (mitigation delta)",
                     score_color, fontsize=8, fontweight="bold")

    # =========================================================================
    # Layer 3: Release Governance
    # =========================================================================
    layer3_bg = FancyBboxPatch((0.3, 0.3), 10.4, 1.9, boxstyle="round,pad=0.15",
                                facecolor=bg_light, edgecolor="#888888", lw=1.5, linestyle="--")
    ax.add_patch(layer3_bg)
    ax.text(0.7, 2.0, "Layer 3: Release Governance", fontsize=11,
            fontweight="bold", color="#555555")

    # Versioned packaging
    draw_rounded_box(ax, (1.0, 0.6), 2.5, 0.9,
                     "Versioned\nPackaging\n(v0.1 → v0.3)",
                     gov_color, fontsize=8, fontweight="bold")

    # SHA-256 manifests
    draw_rounded_box(ax, (4.25, 0.6), 2.5, 0.9,
                     "SHA-256\nIntegrity\nManifests",
                     gov_color, fontsize=8, fontweight="bold")

    # Provenance tracking
    draw_rounded_box(ax, (7.5, 0.6), 2.5, 0.9,
                     "Provenance\nTracking\n(run manifests)",
                     gov_color, fontsize=8, fontweight="bold")

    # =========================================================================
    # Arrows
    # =========================================================================

    # Public items → pre/post mitigation
    draw_arrow(ax, (2.75, 6.6), (4.25, 5.0), color="#388E3C", lw=1.8)
    draw_arrow(ax, (2.75, 6.6), (7.25, 5.0), color="#388E3C", lw=1.8)

    # Restricted items → governed access (dashed)
    draw_arrow(ax, (8.25, 6.6), (8.25, 5.0), color="#C62828", style="--", lw=1.5)
    ax.text(8.8, 5.8, "governed\naccess", fontsize=7, color="#C62828", style="italic")

    # Models → conditions
    draw_arrow(ax, (2.5, 4.4), (3.0, 4.6), color="#757575", lw=1.2)

    # Pre/post → scoring
    draw_arrow(ax, (4.25, 4.2), (4.25, 3.8), color="#1565C0", lw=1.5)
    draw_arrow(ax, (7.25, 4.2), (7.25, 3.8), color="#1565C0", lw=1.5)

    # LLM judge → scoring
    draw_arrow(ax, (9.75, 4.2), (8.5, 3.8), color="#7B1FA2", lw=1.5)

    # Scoring → governance
    draw_arrow(ax, (4.5, 3.0), (2.25, 1.5), color="#E65100", lw=1.5)
    draw_arrow(ax, (5.75, 3.0), (5.5, 1.5), color="#E65100", lw=1.5)
    draw_arrow(ax, (7.0, 3.0), (8.75, 1.5), color="#E65100", lw=1.5)

    # Title
    ax.text(5.5, 8.35, "Frontier Uplift Observatory — Framework Architecture",
            ha="center", fontsize=13, fontweight="bold", color="#333333")

    plt.tight_layout()

    # Save
    from pathlib import Path
    ROOT = Path(__file__).resolve().parents[1]
    out_path = ROOT / "arxiv-harness" / "figures" / "framework_architecture.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"Wrote {out_path}")

    # Also save to paper/figures
    paper_path = ROOT / "paper" / "figures"
    paper_path.mkdir(parents=True, exist_ok=True)
    import shutil
    shutil.copy(out_path, paper_path / "framework_architecture.png")
    print(f"Copied to {paper_path / 'framework_architecture.png'}")


if __name__ == "__main__":
    main()
