MAIN   = main
LATEX  = pdflatex
SHELL  = /bin/bash

# LaTeX source dependencies
SECTIONS = $(wildcard sections/*.tex)
FIGURES  = $(wildcard figures/*.png) $(wildcard figures/*.pdf)
DEPS     = $(MAIN).tex references.bib $(SECTIONS) $(FIGURES)

# ── Build ────────────────────────────────────────────────────────────────────

.PHONY: all
all: $(MAIN).pdf

$(MAIN).pdf: $(DEPS)
	latexmk -pdf -dvi- -ps- -halt-on-error $(MAIN)

# ── Live Preview ─────────────────────────────────────────────────────────────

.PHONY: watch
watch:
	latexmk -pdf -dvi- -ps- -interaction=nonstopmode -synctex=1 -pvc $(MAIN)

# ── Word Count ───────────────────────────────────────────────────────────────

.PHONY: wordcount
wordcount:
	@bash scripts/word_count.sh

# ── Pre-Submission Check ─────────────────────────────────────────────────────

.PHONY: check
check:
	@bash scripts/check_submission.sh

# ── arXiv Submission Package ─────────────────────────────────────────────────

.PHONY: arxiv
arxiv: $(MAIN).pdf
	@echo "Packaging for arXiv..."
	@if command -v arxiv_latex_cleaner >/dev/null 2>&1; then \
		arxiv_latex_cleaner . \
			--config cleaner_config.yaml; \
		cd $(MAIN)_arXiv && tar czvf ../arxiv_submission.tar.gz ./*; \
		echo ""; \
		echo "Created: arxiv_submission.tar.gz"; \
		du -h ../arxiv_submission.tar.gz; \
	else \
		echo "arxiv-latex-cleaner not found. Installing..."; \
		pip3 install arxiv-latex-cleaner; \
		$(MAKE) arxiv; \
	fi

# ── Revision Diff ────────────────────────────────────────────────────────────

.PHONY: diff
diff:
	@if command -v git-latexdiff >/dev/null 2>&1; then \
		mkdir -p diff; \
		git latexdiff \
			--main $(MAIN).tex \
			--tmpdirprefix ./diff/ \
			--cleanup keeppdf \
			--whole-tree \
			--latexdiff-flatten \
			--bibtex \
			HEAD~1; \
	else \
		echo "git-latexdiff not found."; \
		echo "  brew install git-latexdiff  (macOS)"; \
		echo "  pip install git-latexdiff   (pip)"; \
	fi

# ── Switch Submission Mode ───────────────────────────────────────────────────

.PHONY: mode-preprint
mode-preprint:
	@sed -i '' 's/^\\\\usepackage\[.*\]{neurips_2026}/\\\\usepackage[preprint,eandd]{neurips_2026}/' $(MAIN).tex
	@echo "Switched to preprint mode (arXiv)"

.PHONY: mode-submission
mode-submission:
	@sed -i '' 's/^\\\\usepackage\[.*\]{neurips_2026}/\\\\usepackage[eandd]{neurips_2026}/' $(MAIN).tex
	@echo "Switched to anonymous submission mode"

.PHONY: mode-final
mode-final:
	@sed -i '' 's/^\\\\usepackage\[.*\]{neurips_2026}/\\\\usepackage[final,eandd]{neurips_2026}/' $(MAIN).tex
	@echo "Switched to camera-ready mode"

# ── Clean ────────────────────────────────────────────────────────────────────

.PHONY: clean
clean:
	latexmk -C $(MAIN)
	rm -f $(MAIN).bbl $(MAIN).run.xml
	rm -rf diff/ *_arXiv/ arxiv_submission.tar.gz

.PHONY: distclean
distclean: clean
	rm -f $(MAIN).pdf
