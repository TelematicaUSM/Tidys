.DEFAULT_GOAL = run
program = run.py
dir_name = $${PWD\#\#*/}

venv_v = 12.0.5
runenv = . env/bin/activate
python = $(runenv) && python

gempath = ./gems
gembin = $(gempath)/bin
use_gempath = export GEM_HOME=$(gempath)

csspath = static/css
scsspath = static/scss
sasspaths = $(scsspath):$(csspath)
sasscmd = $(gembin)/sass

bbfoldername = bourbon_files
bbpath = $(scsspath)/$(bbfoldername)

VPATH = static $(gembin) $(scsspath) \
        env/lib/python3.4/site-packages make_empty_targets


make_empty_targets:
	mkdir make_empty_targets

dependencies: | make_empty_targets
	sudo apt-get update
	sudo apt-get install python3 python3-dev \
	                     build-essential ruby curl
	touch make_empty_targets/dependencies

virtualenv-$(venv_v): | dependencies
	curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-$(venv_v).tar.gz
	tar xvfz virtualenv-$(venv_v).tar.gz
	rm virtualenv-$(venv_v).tar.gz

env: | dependencies virtualenv-$(venv_v)
	cd virtualenv-$(venv_v) && \
	python3 virtualenv.py --python=python3 ../env

sass bourbon: | dependencies
	$(use_gempath) && gem install $@

$(bbfoldername): bourbon
	$(use_gempath) && $(gembin)/bourbon install \
	                                    --path=$(scsspath)
	mv $(scsspath)/bourbon $(bbpath)

tornado: | env
	$(runenv) && pip install $@

css: scss $(bbfoldername) sass
	$(use_gempath) && $(sasscmd) --update $(sasspaths)

.PHONY: run srun drun testenv attach csswatch dcsswatch

run: tornado css
	$(python) $(program)

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
	rm -rf env __pycache__ $(csspath) \
	       $(gempath) log.log $(bbpath) virtualenv-$(venv_v)
