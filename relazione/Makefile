out/relazione.pdf: $(wildcard *.md) | out
	pandoc -t latex --toc --listings --template $(CURDIR)/eisvogel.tex -o $@ $^

out:
	mkdir out