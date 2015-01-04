runenv = . env/bin/activate
program = run.py
.DEFAULT_GOAL = run

dir_name = $${PWD\#\#*/}

gempath = ./gems
gembin = $(gempath)/bin
use_gempath = export GEM_HOME=$(gempath)

csspath = static/css
scsspath = static/scss
sasspaths = $(scsspath):$(csspath)
sasscmd = sass

bbfoldername = bourbon_files
bbpath = $(scsspath)/$(bbfoldername)

VPATH = static $(gembin) make_empty_targets $(scsspath)

make_empty_targets:
	mkdir make_empty_targets

dependencies: make_empty_targets
	sudo apt-get update && sudo apt-get install python3 python3-dev virtualenv build-essential ruby
	touch make_empty_targets/dependencies

env: dependencies
	virtualenv --system-site-packages --python=/usr/bin/python3 env

sass: dependencies
	$(use_gempath); gem install sass

bourbon: dependencies
	$(use_gempath); gem install bourbon

$(bbfoldername): bourbon
	$(use_gempath); $(gembin)/bourbon install --path=$(scsspath)
	mv $(scsspath)/bourbon $(bbpath)

pypackgs: env requirements.txt make_empty_targets
	$(runenv); pip install -r requirements.txt
	touch make_empty_targets/pypackgs

css: scss $(bbfoldername) sass
	$(use_gempath); $(gembin)/sass --update $(sasspaths)

.PHONY: run srun drun testenv attach csswatch dcsswatch

run: pypackgs css
	-$(runenv); python $(program)

srun:
	screen -S $(dir_name) $(MAKE) run

drun:
	screen -d -m -S $(dir_name) $(MAKE) run

testenv: env
	$(runenv); python -V

attach:
	screen -r $(dir_name)

csswatch: scss $(bbfoldername) sass
	$(use_gempath); $(gembin)/sass --watch $(sasspaths)

dcsswatch:
	screen -d -m -S $(dir_name)_sass $(MAKE) csswatch

clean:
	rm -rf env __pycache__ make_empty_targets $(csspath) $(gempath) log.log $(bbpath)
