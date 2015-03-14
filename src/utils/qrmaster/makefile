css_name = style
scss_file = $(css_name).scss
css_file = $(css_name).css

.DEFAULT_GOAL = $(css_file)

$(css_file): $(scss_file)
	$(sasscmd) --update $(scss_file)

clean:
	rm -f $(css_file) $(css_file).map bourbon_files
