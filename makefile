.DEFAULT_GOAL = run
program = run.py
runenv = . env/bin/activate
python = $(runenv) && python
dir_name = $${PWD\#\#*/}

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
        env/lib/python3.4/site-packages


dependencies:
	sudo apt-get update
	sudo apt-get install python3 python3-dev virtualenv \
	                     build-essential ruby
	touch dependencies

env: dependencies
	virtualenv --python=python3 env

sass bourbon: dependencies
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
	       $(gempath) log.log $(bbpath)
