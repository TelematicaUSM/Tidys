VPATH = static
.PHONY = install clean
static_path = static
name = loading

coffee_file = $(name).coffee
js_file = $(name).js
js_path = $(static_path)/$(js_file)

scss_file = $(name).scss
css_file = $(name).css
css_path = $(static_path)/$(css_file)


install: $(js_file) $(css_file)

$(js_file): $(coffee_file)
	$(coffeecmd) --map --compile \
	    $(static_path)/$(coffee_file)

$(css_file): $(scss_file)
	$(sasscmd) --update $(static_path)/$(scss_file)

clean:
	rm -f $(js_path)  $(js_path).map \
	      $(css_path) $(css_path).map
