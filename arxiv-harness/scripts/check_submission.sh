#!/usr/bin/env bash
# Pre-submission validation for NeurIPS 2026 / arXiv
set -euo pipefail

PASS=0
FAIL=0
WARN=0

check_pass() { echo "  [PASS] $1"; ((PASS++)); }
check_fail() { echo "  [FAIL] $1"; ((FAIL++)); }
check_warn() { echo "  [WARN] $1"; ((WARN++)); }

echo "======================================"
echo "  Pre-Submission Validation"
echo "======================================"
echo ""

# 1. PDF exists
echo "1. Checking PDF..."
if [ -f main.pdf ] && [ -s main.pdf ]; then
    SIZE=$(du -h main.pdf | cut -f1)
    check_pass "main.pdf exists ($SIZE)"
else
    check_fail "main.pdf not found. Run: make"
fi

# 2. No TODOs
echo "2. Checking for TODOs..."
TODO_COUNT=$(grep -rni 'TODO\|FIXME\|XXX\|HACK' sections/ main.tex 2>/dev/null | wc -l | tr -d ' ')
if [ "$TODO_COUNT" -eq 0 ]; then
    check_pass "No TODO/FIXME markers found"
else
    check_fail "$TODO_COUNT TODO/FIXME markers found:"
    grep -rni 'TODO\|FIXME\|XXX\|HACK' sections/ main.tex 2>/dev/null | head -10 | sed 's/^/         /'
fi

# 3. Undefined references
echo "3. Checking references..."
if [ -f main.log ]; then
    UNDEF_REF=$(grep -c "Reference.*undefined" main.log 2>/dev/null || true)
    if [ "$UNDEF_REF" -eq 0 ]; then
        check_pass "No undefined references"
    else
        check_fail "$UNDEF_REF undefined reference(s)"
        grep "Reference.*undefined" main.log | head -5 | sed 's/^/         /'
    fi
else
    check_warn "No main.log found (compile first)"
fi

# 4. Missing citations
echo "4. Checking citations..."
if [ -f main.log ]; then
    UNDEF_CIT=$(grep -c "Citation.*undefined" main.log 2>/dev/null || true)
    if [ "$UNDEF_CIT" -eq 0 ]; then
        check_pass "No undefined citations"
    else
        check_fail "$UNDEF_CIT undefined citation(s)"
        grep "Citation.*undefined" main.log | head -5 | sed 's/^/         /'
    fi
else
    check_warn "No main.log found (compile first)"
fi

# 5. Word count
echo "5. Checking word count..."
if command -v texcount &>/dev/null; then
    WORDS=$(texcount -utf8 -inc -total -brief main.tex 2>/dev/null | grep -o '[0-9]*' | head -1)
    if [ -n "$WORDS" ]; then
        if [ "$WORDS" -le 6500 ]; then
            check_pass "Word count: $WORDS (within typical 9-page range)"
        else
            check_warn "Word count: $WORDS (may exceed 9 pages)"
        fi
    else
        check_warn "Could not determine word count"
    fi
else
    check_warn "texcount not installed (brew install texcount)"
fi

# 6. Missing figures
echo "6. Checking figure files..."
MISSING_FIGS=0
for fig in $(grep -oh 'includegraphics\[.*\]{[^}]*}' main.tex sections/*.tex 2>/dev/null | grep -oh '{[^}]*}' | tr -d '{}'); do
    # Check in figures/ directory and current directory
    if [ ! -f "figures/$fig" ] && [ ! -f "$fig" ] && [ ! -f "figures/${fig}.png" ] && [ ! -f "figures/${fig}.pdf" ]; then
        check_fail "Missing figure: $fig"
        ((MISSING_FIGS++))
    fi
done
if [ "$MISSING_FIGS" -eq 0 ]; then
    check_pass "All referenced figures exist"
fi

# 7. Anonymization (for submission mode)
echo "7. Checking anonymization..."
ANON_ISSUES=$(grep -rni 'our previous\|my previous\|our earlier\|we previously\|I previously' sections/ 2>/dev/null | wc -l | tr -d ' ')
if [ "$ANON_ISSUES" -eq 0 ]; then
    check_pass "No obvious de-anonymizing language found"
else
    check_warn "$ANON_ISSUES potential de-anonymizing phrase(s)"
    grep -rni 'our previous\|my previous\|our earlier\|we previously' sections/ 2>/dev/null | head -5 | sed 's/^/         /'
fi

# 8. NeurIPS checklist included
echo "8. Checking NeurIPS checklist..."
if grep -q 'checklist' main.tex 2>/dev/null; then
    check_pass "NeurIPS checklist included"
else
    check_fail "NeurIPS checklist not found in main.tex (mandatory)"
fi

# 9. PDF size (arXiv limit: 50MB)
echo "9. Checking PDF size..."
if [ -f main.pdf ]; then
    SIZE_BYTES=$(wc -c < main.pdf | tr -d ' ')
    SIZE_MB=$((SIZE_BYTES / 1048576))
    if [ "$SIZE_MB" -lt 50 ]; then
        check_pass "PDF size: ${SIZE_MB}MB (under 50MB arXiv limit)"
    else
        check_fail "PDF size: ${SIZE_MB}MB (exceeds 50MB arXiv limit)"
    fi
fi

# 10. .bbl file for arXiv
echo "10. Checking .bbl file..."
if [ -f main.bbl ]; then
    check_pass "main.bbl exists (needed for arXiv)"
else
    check_warn "main.bbl not found (generate with: make)"
fi

# Summary
echo ""
echo "======================================"
echo "  Results: $PASS passed, $FAIL failed, $WARN warnings"
echo "======================================"

if [ "$FAIL" -gt 0 ]; then
    exit 1
fi
