watch:
	texfot latexmk -pdf -pvc main.tex | grep -v "Missing character: There is no ; in font nullfont"

book:
	texfot latexmk -pdf main.tex | grep -v "Missing character: There is no ; in font nullfont"

clean:
	texfot latexmk -C
	rm *.bbl

view:
	evince main.pdf &

pretty: # TOFIX: THIS DOESNT WORK ANYMORE
	for file in cap/*.tex ; do \
		python3 beautifier.py $$file ; \
		rm -f cap/*.bak cap/*.bak0 cap/*.log ; \
	done

indexing:
	python3 missing_indexes.py > missing_indices.idx
	# this *.idx file is highly volatile