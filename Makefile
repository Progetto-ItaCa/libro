itaca.sty: itaca.ins itaca.dtx
	tex $<

hash:
	echo "\\\\newcommand{\\gHash}{\\\\texttt{`git rev-parse --short HEAD`}}" > gitcommit.tex
# 	$(MAKE) -B main.pdf

itaca.pdf: itaca.dtx
	latexmk -shell-escape -pdf -gg $<

main.pdf: main.tex itaca.sty
	latexmk -shell-escape -pdf main.tex

watch:
	texfot latexmk -shell-escape -pdf -pvc main.tex | grep -v "Missing character: There is no ; in font nullfont"

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