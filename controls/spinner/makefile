VPATH = static
.PHONY = install clean
static_path = static
name = spinner

scss_file = $(name).scss
css_file = $(name).css
css_path = $(static_path)/$(css_file)

$(css_file): $(scss_file)
	$(sasscmd) --update $(static_path)/$(scss_file)

clean:
	rm -f $(css_path) $(css_path).map
