watch:
	texfot latexmk -pdf -pvc main.tex

book:
	texfot latexmk -pdf main.tex

clean:
	texfot latexmk -C
	rm *.bbl

view:
	evince main.pdf &

pretty:
	for file in cap/*.tex ; do \
		python3 beautifier.py $$file ; \
		rm -f cap/*.bak cap/*.bak0 cap/*.log ; \
	done
