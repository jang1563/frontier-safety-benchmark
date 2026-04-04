#!/usr/bin/env bash
# Word count analysis for NeurIPS submission (9-page limit)
set -euo pipefail

if ! command -v texcount &>/dev/null; then
    echo "texcount not found. Install with: brew install texcount"
    exit 1
fi

echo "=== Total Word Count ==="
texcount -utf8 -inc -total main.tex
echo ""
echo "=== Breakdown by Section ==="
texcount -utf8 -inc -sub=section main.tex
echo ""
echo "Note: NeurIPS 2026 limit is 9 pages of content (not word count)."
echo "      Typical 9 pages ~ 5,400-6,300 words excluding figures/tables."
