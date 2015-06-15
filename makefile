.DEFAULT_GOAL = run
program = run.py
dir_name = $${PWD\#\#*/}

runenv = . env/bin/activate
python = $(runenv) && python
pip_install = $(runenv) && pip install

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
coffeepaths = $(jspath) static/coffee
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
clean: sub_target = clean

VPATH = static $(gembin) $(scsspath) $(nmodulespath) \
        $(jspath) env/lib/python3.4/site-packages \
        make_empty_targets $(csspath)

doc_path = doc

green = \033[0;32m
nc = \033[0m

make_empty_targets:
	mkdir make_empty_targets

dependencies: | make_empty_targets
	sudo apt-get update
	sudo apt-get install python3 python3-dev \
	                     build-essential ruby npm curl \
	                     screen nodejs-legacy
	touch make_empty_targets/dependencies

virtualenv: | dependencies
	url=$$(./get_venv_url.py) && \
	mkdir $@ && \
	curl $$url | tar xvfz - -C $@ --strip-components=1

env: | dependencies virtualenv
	cd virtualenv && \
	python3 virtualenv.py --python=python3 ../env

tornado: | env
	$(pip_install) $@

sphinx: | env
	$(pip_install) Sphinx

sass bourbon: | dependencies
	$(use_gempath) && gem install --no-ri --no-rdoc $@

$(bbfoldername): bourbon
	$(use_gempath) && $(gembin)/bourbon install \
	                                    --path=$(scsspath)
	mv $(scsspath)/bourbon $(bbpath)

css: scss | $(bbfoldername) sass
	$(use_gempath) && $(sasscmd) --update $(sasspaths)

coffee-script bower: | dependencies
	npm install $@

normalize.css: | css bower
	$(bowercmd) install $@
	cd $(csspath) && ln -s ../../$(bowerpath)/$@/$@ $@

reconnecting-websocket.js: | bower js
	$(bowercmd) install reconnectingWebsocket
	cd $(jspath) && ln -s ../../$(bowerpath)/reconnectingWebsocket/$@ $@

js: coffee | coffee-script
	$(coffeecmd) $(coffeeoptions) $(coffeepaths)

.PHONY: run python srun drun testenv attach csswatch dcsswatch \
	jswatch djswatch clean panels notifications locking_panels \
        autodoc clean_doc

run_py_deps = tornado
run: $(run_py_deps) dependencies css normalize.css js reconnecting-websocket.js panels notifications locking_panels
	$(python) -i $(program)

python: dependencies
	$(python)

srun:
	screen -S $(dir_name) $(MAKE) run

drun:
	screen -d -m -S $(dir_name) $(MAKE) run

panels notifications locking_panels: coffee-script sass
	@echo "Executing makefiles in $@ ..."
	@$(sub_make_resources) && \
	 cd $@ && \
	 $(make_iterate_over_d)

testenv: env
	$(python) -V

attach:
	screen -r $(dir_name)

#Upstream Merge
upsm:
	git pull --no-commit --no-rebase cganterh.net:git/tornadoBoiler.git

csswatch: scss $(bbfoldername) sass
	$(use_gempath) && $(sasscmd) --watch $(sasspaths)

dcsswatch:
	screen -d -m -S $(dir_name)_sass $(MAKE) csswatch

jswatch:
	$(nmodulespath)/coffee-script/bin/coffee --watch $(coffeeoptions) $(coffeepaths)

djswatch:
	screen -d -m -S $(dir_name)_coffee $(MAKE) jswatch


autodoc: $(run_py_deps) sphinx
	$(runenv) && \
	dir_name=$(dir_name) && \
	cd .. && \
	sphinx-apidoc --separate -f -o $$dir_name/$(doc_path) $$dir_name

	$(runenv) && \
	cd $(doc_path) && \
	$(MAKE) html

clean_doc: sphinx
	$(runenv) && cd $(doc_path) && $(MAKE) clean
	cd $(doc_path) && \
	find . -maxdepth 1 -type f ! -regex '.*\(index.rst\|conf.py\|[mM]akefile\)' -delete

clean: clean_doc
	rm -rf $(bowerpath) env $(nmodulespath) \
	       __pycache__ $(csspath) $(jspath) $(gempath) \
	       log.log $(bbpath) virtualenv temp
	-cd panels && $(make_iterate_over_d)
	-cd notifications && $(make_iterate_over_d)
	-cd locking_panels && $(make_iterate_over_d)
