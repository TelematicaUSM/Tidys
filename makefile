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

nmodulesfolder = node_modules
bowerfolder = bower_components
nmodulespath = ./$(nmodulesfolder)

jspath = static/js
coffeepaths = $(jspath) static/coffee
coffeeoptions = --map --compile --output
coffeecmd = $(nmodulespath)/coffee-script/bin/coffee

VPATH = static $(gembin) $(scsspath) $(nmodulesfolder) $(jspath) env/lib/python3.4/site-packages

make_empty_targets:
	mkdir make_empty_targets

dependencies: | make_empty_targets
	sudo apt-get update
	sudo apt-get install python3 python3-dev virtualenv \
	                     build-essential ruby npm
	-sudo ln -s /usr/bin/nodejs /usr/bin/env/node
	touch make_empty_targets/dependencies

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

coffee-script bower: dependencies
	npm install $@

reconnecting-websocket.js: bower | js
	$(nmodulespath)/bower/bin/bower install reconnectingWebsocket
	cd $(jspath) && ln -s ../../$(bowerfolder)/reconnectingWebsocket/reconnecting-websocket.js reconnecting-websocket.js

js: coffee-script coffee
	$(nmodulespath)/coffee-script/bin/coffee $(coffeeoptions) $(coffeepaths)

panels: | make_empty_targets
	-export coffeecmd="$$(readlink -e $(coffeecmd))"; export sasscmd="$$(readlink -e $(sasscmd))"; export GEM_HOME="$$(readlink -e $(gempath))"; cd panels && for d in */ ; do $(MAKE) -C "$$d"; done
	touch make_empty_targets/panels

.PHONY: run srun drun testenv attach csswatch dcsswatch \
	jswatch djswatch clean

run: tornado css js reconnecting-websocket.js panels dependencies
	$(python) $(program)

srun:
	screen -S $(dir_name) $(MAKE) run

drun:
	screen -d -m -S $(dir_name) $(MAKE) run

testenv: env
	$(python) -V

attach:
	screen -r $(dir_name)

#Upstream Merge
upsm:
	git pull --no-commit cganterh.net:git/tornadoBoiler.git

csswatch: scss $(bbfoldername) sass
	$(use_gempath) && $(sasscmd) --watch $(sasspaths)

dcsswatch:
	screen -d -m -S $(dir_name)_sass $(MAKE) csswatch

jswatch:
	$(nmodulespath)/coffee-script/bin/coffee --watch $(coffeeoptions) $(coffeepaths)

djswatch:
	screen -d -m -S $(dir_name)_coffee $(MAKE) jswatch

clean:
	rm -rf $(bowerfolder) env $(nmodulesfolder) __pycache__ $(csspath) $(jspath) $(gempath) log.log $(bbpath)
