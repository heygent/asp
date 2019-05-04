
out/relazione.pdf: $(wildcard *.md)
	pandoc --data-dir=~/.pandoc --toc -t latex --listings --template ~/.local/share/pandoc/templates/eisvogel.tex -o $@ $^