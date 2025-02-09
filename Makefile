watch:
	texfot latexmk -pdf -pvc main.tex | grep -v "Missing character: There is no ; in font nullfont"

book:
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