
out/relazione.pdf: $(wildcard *.md)
	pandoc --data-dir=~/.pandoc --toc -t latex --template ~/.local/share/pandoc/templates/eisvogel.tex -o $@ $^