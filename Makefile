p:
	texfot latexmk -pdf -pvc main.tex

t:
	texfot latexmk -pdf main.tex

c:
	texfot latexmk -C
	rm *.bbl

v:
	evince main.pdf &

pretty:
	for file in cap/*.tex ; do \
		python3 beautifier.py $$file ; \
		rm -f cap/*.bak cap/*.bak0 cap/*.log ; \
	done
