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

VPATH = static $(gembin) $(scsspath) $(nmodulespath) \
        env/lib/python3.4/site-packages \
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

bower: | dependencies
	npm install $@

normalize.css: | css bower
	$(bowercmd) install $@
	cd $(csspath) && ln -s ../../$(bowerpath)/$@/$@ $@

.PHONY: run python srun drun testenv attach csswatch dcsswatch \
	clean autodoc clean_doc

run_py_deps = tornado
run: $(run_py_deps) dependencies css normalize.css
	$(python) -i $(program)

python: dependencies
	$(python)

srun:
	screen -S $(dir_name) $(MAKE) run

drun:
	screen -d -m -S $(dir_name) $(MAKE) run

testenv: env
	$(python) -V

attach:
	screen -r $(dir_name)

csswatch: scss $(bbfoldername) sass
	$(use_gempath) && $(sasscmd) --watch $(sasspaths)

dcsswatch:
	screen -d -m -S $(dir_name)_sass $(MAKE) csswatch

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
	       __pycache__ $(csspath) $(gempath) \
	       log.log $(bbpath) virtualenv temp
