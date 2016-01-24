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


.DEFAULT_GOAL = run
program = run.py
dir_name = $${PWD\#\#*/}

runenv = . env/bin/activate
python = $(runenv) && python
pip_install = $(runenv) && pip install
unittest = $(python) -m unittest

gempath = ./gems
gembin = $(gempath)/bin
use_gempath = export GEM_HOME=$(gempath)

csspath = static/css
scsspath = static/scss
sasspaths = $(scsspath):$(csspath)
sasscmd = $(gembin)/sass

bbfoldername = bourbon_files
bbpath = $(scsspath)/$(bbfoldername)

nmodulespath = ./node_modules

bowerpath = ./bower_components
bowercmd = $(nmodulespath)/bower/bin/bower

jspath = static/js
coffeepath = static/coffee
coffeepaths = $(jspath) $(coffeepath)
coffeeoptions = --map --compile --output
coffeecmd = $(nmodulespath)/coffee-script/bin/coffee

sub_target =
sub_make_resources = export coffeecmd="$$(readlink -e $(coffeecmd))" && \
                     export sasscmd="$$(readlink -e $(sasscmd))" && \
                     export GEM_HOME="$$(readlink -e $(gempath))"
make_iterate_over_d = for d in */ ; \
                          do if [ -f "$$d/makefile" ]; then \
                              $(MAKE) -C "$$d" --no-print-directory $(sub_target); \
                          fi \
                      done

VPATH = static $(gembin) $(scsspath) $(nmodulespath) \
        $(jspath) env/lib/python3.4/site-packages \
        make_empty_targets $(csspath)

qrm_path = src/utils/qrmaster
doc_path = doc

green = \033[0;32m
nc = \033[0m

make_empty_targets:
	mkdir make_empty_targets

dependencies: | make_empty_targets
	sudo apt-get update
	sudo apt-get install python3 python3-dev \
	                     build-essential ruby npm curl \
	                     screen nodejs-legacy libjpeg-dev \
						 mongodb
	touch make_empty_targets/dependencies

virtualenv: | dependencies
	url=$$(./get_venv_url.py) && \
	mkdir $@ && \
	curl $$url | tar xvfz - -C $@ --strip-components=1

env: | dependencies virtualenv
	cd virtualenv && \
	python3 virtualenv.py --python=python3 ../env

tornado motor oauth2client qrcode: | env
	$(pip_install) $@

jwt: | env
	$(pip_install) PyJWT

PIL: | env
	$(pip_install) pillow

httplib2: | env
	$(pip_install) git+https://github.com/jcgregorio/httplib2.git

sphinx: | env
	$(pip_install) Sphinx

sass bourbon: | dependencies
	$(use_gempath) && gem install --no-ri --no-rdoc $@

$(bbfoldername): bourbon
	$(use_gempath) && $(gembin)/bourbon install \
	                                    --path=$(scsspath)
	mv $(scsspath)/bourbon $(bbpath)

css: $(scsspath)/*.scss | $(bbfoldername) sass
	$(use_gempath) && $(sasscmd) --update $(sasspaths)

coffee-script bower: | dependencies
	npm install $@

normalize.css: | css bower
	$(bowercmd) install $@
	cd $(csspath) && ln -s ../../$(bowerpath)/normalize-css/$@ $@

tinycolor.js: | bower js
	$(bowercmd) install tinycolor
	cd $(jspath) && ln -s ../../$(bowerpath)/tinycolor/$@ $@

reconnecting-websocket.js: | bower js
	$(bowercmd) install reconnectingWebsocket
	cd $(jspath) && ln -s ../../$(bowerpath)/reconnectingWebsocket/$@ $@

unibabel.js: | bower js
	$(bowercmd) install unibabel
	cd $(jspath) && ln -s ../../$(bowerpath)/unibabel/index.js $@

js: $(coffeepath)/*.coffee | coffee-script
	$(coffeecmd) $(coffeeoptions) $(coffeepaths)

.PHONY: run python srun drun testenv attach csswatch dcsswatch \
	jswatch djswatch clean panels notifications \
	locking_panels qrmaster controls autodoc clean_doc test
	vtest showdocs

run_py_deps = tornado motor jwt httplib2 oauth2client
run: $(run_py_deps) dependencies css js \
     reconnecting-websocket.js tinycolor.js unibabel.js \
	 normalize.css panels notifications locking_panels \
	 controls qrmaster
	$(python) -i $(program)

python: dependencies
	$(python)

srun:
	screen -S $(dir_name) $(MAKE) run

drun:
	screen -d -m -S $(dir_name) $(MAKE) run

qrmaster_py_deps = tornado qrcode PIL
qrmaster: dependencies sass $(bbfoldername) $(qrmaster_py_deps)
	-cd $(qrm_path) && \
	ln -s ../../../$(bbpath) $(bbfoldername)
	$(sub_make_resources) && \
	 cd $(qrm_path) && \
	 $(MAKE)

panels notifications locking_panels controls: coffee-script sass $(bbfoldername)
	@echo "$(green)Executing makefiles in $@ ...$(nc)"
	@$(sub_make_resources) && \
	 cd $@ && \
	 $(make_iterate_over_d)

testenv: env
	$(python) -V

test:
	$(unittest)

vtest:
	$(unittest) -v

attach:
	screen -r $(dir_name)

#Upstream Merge
upsm:
	git pull --no-commit --no-rebase cganterh.net:git/tornadoBoxes.git

csswatch: scss $(bbfoldername) sass
	$(use_gempath) && $(sasscmd) --watch $(sasspaths)

dcsswatch:
	screen -d -m -S $(dir_name)_sass $(MAKE) csswatch

jswatch:
	$(nmodulespath)/coffee-script/bin/coffee --watch $(coffeeoptions) $(coffeepaths)

djswatch:
	screen -d -m -S $(dir_name)_coffee $(MAKE) jswatch

autodoc: $(run_py_deps) $(qrmaster_py_deps) sphinx
	$(runenv) && \
	dir_name=$(dir_name) && \
	cd .. && \
	sphinx-apidoc --separate -f -o $$dir_name/$(doc_path) $$dir_name

	$(runenv) && \
	cd $(doc_path) && \
	export AA_PATH=".." && \
	$(MAKE) html

showdocs: autodoc
	xdg-open doc/_build/html/index.html

clean_doc: | sphinx
	$(runenv) && cd $(doc_path) && $(MAKE) clean
	cd $(doc_path) && \
	find . -maxdepth 1 -type f ! -regex '.*\(index.rst\|todo.rst\|conf.py\|[mM]akefile\)' -delete

clean: sub_target = clean
clean: clean_doc
	rm -rf $(bowerpath) env $(nmodulespath) \
	       __pycache__ $(csspath) $(jspath) $(gempath) \
	       log.log $(bbpath) virtualenv temp
	-cd panels && $(make_iterate_over_d)
	-cd notifications && $(make_iterate_over_d)
	-cd locking_panels && $(make_iterate_over_d)
	-cd controls && $(make_iterate_over_d)
	cd $(qrm_path) && $(MAKE) clean
