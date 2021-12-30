%.pdf: %.dot
				circo -Tpdf $< > $@

%.dot: %.blocks
				python -m brs $< $@
