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

nmodulesfolder = node_modules
bowerfolder = bower_components
nmodulespath = ./$(nmodulesfolder)

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

VPATH = static $(gembin) $(scsspath) $(nmodulesfolder) \
        $(jspath) env/lib/python3.4/site-packages \
        make_empty_targets

make_empty_targets:
	mkdir make_empty_targets

dependencies: | make_empty_targets
	sudo apt-get update
	sudo apt-get install python3 python3-dev \
	                     build-essential ruby npm curl \
	                     screen mongodb
	-sudo ln -s /usr/bin/nodejs /usr/bin/node
	touch make_empty_targets/dependencies

virtualenv: | dependencies
	mkdir virtualenv && \
	curl $$(./get_venv_url.py) | tar xvfz - -C $@ \
	                                 --strip-components=1

env: | dependencies virtualenv
	cd virtualenv && \
	python3 virtualenv.py --python=python3 ../env

tornado motor oauth2client: | env
	$(pip_install) $@

jwt: | env
	$(pip_install) PyJWT

httplib2: | env
	$(pip_install) git+https://github.com/jcgregorio/httplib2.git

sass bourbon: | dependencies
	$(use_gempath) && gem install --no-ri --no-rdoc $@

$(bbfoldername): bourbon
	$(use_gempath) && $(gembin)/bourbon install \
	                                    --path=$(scsspath)
	mv $(scsspath)/bourbon $(bbpath)

css: scss $(bbfoldername) sass
	$(use_gempath) && $(sasscmd) --update $(sasspaths)

coffee-script bower: dependencies
	npm install $@

reconnecting-websocket.js: bower | js
	$(nmodulespath)/bower/bin/bower install reconnectingWebsocket
	cd $(jspath) && ln -s ../../$(bowerfolder)/reconnectingWebsocket/reconnecting-websocket.js \
	                      reconnecting-websocket.js

js: coffee-script coffee
	$(nmodulespath)/coffee-script/bin/coffee $(coffeeoptions) $(coffeepaths)

.PHONY: run srun drun testenv attach csswatch dcsswatch \
	jswatch djswatch clean publish panels notifications locking_panels

run: dependencies tornado motor jwt httplib2 oauth2client css js reconnecting-websocket.js panels notifications locking_panels
	$(python) -i $(program)

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
	git pull --no-commit cganterh.net:git/tornadoBoxes.git

csswatch: scss $(bbfoldername) sass
	$(use_gempath) && $(sasscmd) --watch $(sasspaths)

dcsswatch:
	screen -d -m -S $(dir_name)_sass $(MAKE) csswatch

jswatch:
	$(nmodulespath)/coffee-script/bin/coffee --watch $(coffeeoptions) $(coffeepaths)

djswatch:
	screen -d -m -S $(dir_name)_coffee $(MAKE) jswatch

clean:
	rm -rf $(bowerfolder) env $(nmodulesfolder) \
	       __pycache__ $(csspath) $(jspath) $(gempath) \
	       log.log $(bbpath) virtualenv
	-cd panels && $(make_iterate_over_d)
	-cd notifications && $(make_iterate_over_d)
	-cd locking_panels && $(make_iterate_over_d)

publish:
	git push $(pub_remote)
