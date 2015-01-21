VPATH = static
.PHONY = install clean

install: script.js style.css

script.js: script.coffee
	$(coffeecmd) --map --compile static/script.coffee

style.css: style.scss
	export GEM_HOME=$(gempath) && $(sasscmd) --update \
	                              static/style.scss

clean:
	rm -f static/script.js static/script.js.map \
	    static/style.css static/style.css.map
