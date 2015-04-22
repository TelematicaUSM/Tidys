.DEFAULT_GOAL = run
program = run.py
pub_remote = prod
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

make_empty_targets:
	mkdir make_empty_targets

dependencies: | make_empty_targets
	sudo apt-get update
	sudo apt-get install python3 python3-dev \
	                     build-essential ruby npm curl \
	                     screen nodejs-legacy
	touch make_empty_targets/dependencies

virtualenv: | dependencies
	mkdir virtualenv && \
	curl $$(./get_venv_url.py) | tar xvfz - -C $@ \
	                                 --strip-components=1

env: | dependencies virtualenv
	cd virtualenv && \
	python3 virtualenv.py --python=python3 ../env

tornado: | env
	$(pip_install) $@

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

.PHONY: run srun drun testenv attach csswatch dcsswatch \
	clean

run: dependencies tornado css normalize.css
	$(python) -i $(program)

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

clean:
	rm -rf $(bowerpath) env $(nmodulespath) \
	       __pycache__ $(csspath) $(gempath) \
	       log.log $(bbpath) virtualenv
