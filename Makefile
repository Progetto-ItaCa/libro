p:
	latexmk -pdf -pvc main.tex

t:
	latexmk -pdf main.tex

c:
	latexmk -C
	rm *.bbl

v:
	evince main.pdf &

pretty:
	for file in cap/*.tex ; do \
		python3 beautifier.py $$file ; \
		rm cap/*.bak cap/*.bak0 cap/*.log ; \
	done