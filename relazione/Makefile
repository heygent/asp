
out/relazione.pdf: $(wildcard *.md)
	pandoc -t latex --toc --listings --template $(CURDIR)/eisvogel.tex -o $@ $^