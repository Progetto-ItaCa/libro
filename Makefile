itaca.sty: itaca.ins itaca.dtx
	tex $<

itaca.pdf: itaca.dtx
	latexmk -pdf -gg $<

main.pdf: main.tex itaca.sty
	latexmk \
		-gg -interaction=nonstopmode -pdf \
		-pretex="\pdftrailerid{}\relax" -usepretex  \
	$<

watch:
	texfot latexmk -pdf -pvc main.tex | grep -v "Missing character: There is no ; in font nullfont"

book:
	for f in cap/*.tex; do touch "${f%.tex}.aux"; done
	for f in cap/01/*.tex; do touch "${f%.tex}.aux"; done
	texfot latexmk -pdf main.tex | grep -v "Missing character: There is no ; in font nullfont"

clean:
	texfot latexmk -C
	rm *.bbl

view:
	evince main.pdf &

pretty:
	find cap/ -type f -name "*.tex" -exec python3 beautifier.py {} \;
	find cap/ -type f \( -name "*.bak" -o -name "*.bak0" -o -name "*.log" \) -delete

indexing:
	python3 missing_indexes.py > missing_indices.idx
	# this *.idx file is highly volatile

look_index:
	@cd cap/01/sec && \
	grep -i -r --color=auto "index.*$(word)" .

work: book	view watch

board:
	evince whiteboard.pdf &
	texfot latexmk -pvc -pdf whiteboard.tex