# latexmk configuration for NeurIPS 2026 paper
$pdflatex = 'pdflatex -interaction=nonstopmode -synctex=1 -file-line-error %O %S';
$pdf_mode = 1;
$bibtex_use = 2;
@default_files = ('main.tex');
ensure_path('TEXINPUTS', './style//');
@generated_exts = (@generated_exts, 'synctex.gz');
