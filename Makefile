itaca.sty: itaca.ins itaca.dtx
	tex $<

# -----------------------------------------------------------------------------
# Local dev build helpers (Task A)
# -----------------------------------------------------------------------------
#
# CI can keep doing full builds; locally we optimize the edit->compile loop.

ITACA_DEV_OPTS ?= fast

# TeX injected before main.tex is read (keeps local builds fast).
# - disable index + bibliography output (still OK for drafting)
# - avoid rendering list of todos
DEV_PRETEX = \
  \\PassOptionsToPackage{$(ITACA_DEV_OPTS)}{itaca}\\relax\
  \\AtBeginDocument{\
    \\let\\printindex\\relax\
    \\renewcommand{\\bibliography}[1]{}\
    \\renewcommand{\\bibliographystyle}[1]{}\
    \\let\\listoftodos\\relax\
  }\\relax

LATEXMK_FULL = latexmk -shell-escape -pdf
# Disable bibtex; makeindex is replaced by a no-op for speed.
LATEXMK_DEV  = latexmk -pdf -bibtex- -e '$$makeindex = q/true/;'

hash:
	echo "\\\\newcommand{\\gHash}{\\\\texttt{`git rev-parse --short HEAD`}}" > gitcommit.tex
# 	$(MAKE) -B main.pdf

itaca.pdf: itaca.dtx
	latexmk -shell-escape -pdf -gg $<

main.pdf: main.tex itaca.sty
	latexmk -shell-escape -pdf main.tex

dev: main.tex itaca.sty
	texfot $(LATEXMK_DEV) -pretex="$(DEV_PRETEX)" main.tex

# Compile a single chapter by editing main.tex's \includeonly list.
# Usage: make chap CH=cap/02-limiti   (with or without .tex)
chap: main.tex itaca.sty
	@test -n "$(CH)" || (echo "Usage: make chap CH=cap/02-limiti"; exit 2)
	python3 select_includeonly.py "$(CH)"
	texfot $(LATEXMK_DEV) -pretex="$(DEV_PRETEX)" main.tex

watch:
	texfot latexmk -shell-escape -pdf -pvc main.tex | grep -v "Missing character: There is no ; in font nullfont"

watch-dev:
	texfot $(LATEXMK_DEV) -pvc -pretex="$(DEV_PRETEX)" main.tex

watch-chap:
	@test -n "$(CH)" || (echo "Usage: make watch-chap CH=cap/02-limiti"; exit 2)
	python3 select_includeonly.py "$(CH)"
	texfot $(LATEXMK_DEV) -pvc -pretex="$(DEV_PRETEX)" main.tex

book:
	for f in cap/*.tex; do touch "${f%.tex}.aux"; done
	for f in cap/01/*.tex; do touch "${f%.tex}.aux"; done
	texfot latexmk -shell-escape -pdf main.tex | grep -v "Missing character: There is no ; in font nullfont"

clean:
	texfot latexmk -C main.tex
	texfot latexmk -C itaca.dtx
	rm -rf *.bbl *.tdo

view:
	evince main.pdf &

pretty:
	find cap/ -type f -name "*.tex" -exec python3 beautifier.py {} \;
	find cap/ -type f \( -name "*.bak" -o -name "*.bak0" -o -name "*.log" \) -delete

indexing:
	python3 missing_indexes.py > missing_indices.idx
	code missing_indices.idx
	# this *.idx file is highly volatile

look_index:
	@cd cap/01/sec && \
	grep -i -r --color=auto "index.*$(word)" .

work: 
	git pull
	$(MAKE) book	
	$(MAKE) view 
	$(MAKE) watch

board:
	evince whiteboard.pdf &
	texfot latexmk -pvc -pdf whiteboard.tex

addnix:
	nix develop 
	latexmk -C
	$(MAKE) work
