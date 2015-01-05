.DEFAULT_GOAL = run
runenv = . env/bin/activate
program = run.py

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

VPATH = static $(gembin) make_empty_targets $(scsspath) $(nmodulesfolder) $(jspath)

make_empty_targets:
	mkdir make_empty_targets

dependencies: make_empty_targets
	sudo apt-get update
	sudo apt-get install python3 python3-dev virtualenv build-essential ruby npm
	-sudo ln -s /usr/bin/nodejs /usr/bin/env/node
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

pypkgs: env requirements.txt make_empty_targets
	$(runenv); pip install -r requirements.txt
	touch make_empty_targets/pypkgs

css: scss $(bbfoldername) sass
	$(use_gempath); $(sasscmd) --update $(sasspaths)

coffee-script:
	npm install coffee-script

bower:
	npm install bower

reconnecting-websocket.js: bower
	$(nmodulespath)/bower/bin/bower install reconnectingWebsocket
	-mkdir $(jspath)
	cd $(jspath) && ln -s ../../$(bowerfolder)/reconnectingWebsocket/reconnecting-websocket.js reconnecting-websocket.js

js: coffee-script coffee
	$(nmodulespath)/coffee-script/bin/coffee $(coffeeoptions) $(coffeepaths)

panels: make_empty_targets
	-export coffeecmd="$$(readlink -e $(coffeecmd))"; export sasscmd="$$(readlink -e $(sasscmd))"; export GEM_HOME="$$(readlink -e $(gempath))"; cd panels && for d in */ ; do $(MAKE) -C "$$d"; done
	touch make_empty_targets/panels

.PHONY: run srun drun testenv attach csswatch dcsswatch \
	jswatch djswatch clean

run: pypkgs css js reconnecting-websocket.js panels
	-$(runenv) && python $(program)

srun:
	screen -S $(dir_name) $(MAKE) run

drun:
	screen -d -m -S $(dir_name) $(MAKE) run

testenv: env
	$(runenv) && python -V

attach:
	screen -r $(dir_name)

#Upstream Merge
upsm:
	git pull --no-commit cganterh.net:git/tornadoBoiler.git

csswatch: scss $(bbfoldername) sass
	$(use_gempath); $(gembin)/sass --watch $(sasspaths)

dcsswatch:
	screen -d -m -S $(dir_name)_sass $(MAKE) csswatch

jswatch:
	$(nmodulespath)/coffee-script/bin/coffee --watch $(coffeeoptions) $(coffeepaths)

djswatch:
	screen -d -m -S $(dir_name)_coffee $(MAKE) jswatch

clean:
	rm -rf make_empty_targets $(bowerfolder) env $(nmodulesfolder) __pycache__ $(csspath) $(jspath) $(gempath) log.log $(bbpath)
