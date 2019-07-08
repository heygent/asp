OUT_DIR = out
GEN_DIR = gen

$(OUT_DIR)/relazione.pdf: $(wildcard *.md) $(GEN_DIR)/99-output.md | $(OUT_DIR)
	pandoc -t latex --toc --listings --template $(CURDIR)/eisvogel.tex -o $@ $^

$(OUT_DIR) $(GEN_DIR):
	mkdir -p $@

$(GEN_DIR)/99-output.md: | $(GEN_DIR)
	../calendario.py --solve 1 --cell-data materia,aula,docente > $@

clean:
	rm -rf $(OUT_DIR) $(GEN_DIR)
