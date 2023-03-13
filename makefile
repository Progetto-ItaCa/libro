p:
	latexmk -pdf -pvc main.tex

t:
	latexmk -pdf main.tex

c:
	latexmk -C
	rm *.bbl

v:
	evince main.pdf &
