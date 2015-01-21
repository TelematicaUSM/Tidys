VPATH = static
.PHONY = install clean

install: conn-ind.js conn-ind.css

conn-ind.js: conn-ind.coffee
	$(coffeecmd) --map --compile static/conn-ind.coffee

conn-ind.css: conn-ind.scss
	export GEM_HOME=$(gempath) && $(sasscmd) --update \
	                              static/conn-ind.scss

clean:
	rm -f static/conn-ind.js static/conn-ind.js.map \
	      static/conn-ind.css static/conn-ind.css.map
