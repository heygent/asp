
out/relazione.pdf: $(wildcard *.md)
	pandoc -t latex --toc --template $(CURDIR)/eisvogel.tex -o $@ $^