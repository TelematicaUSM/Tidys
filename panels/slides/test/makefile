presentation.html: presentation.md
	pandoc -t html5 -s --mathjax --section-divs \
		-c style.css -o $@ $^
