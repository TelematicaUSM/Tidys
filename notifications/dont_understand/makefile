# COPYRIGHT (c) 2016 Cristóbal Ganter
#
# GNU AFFERO GENERAL PUBLIC LICENSE
#    Version 3, 19 November 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


VPATH = static
.PHONY = install clean
static_path = static
name = dont_understand

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
