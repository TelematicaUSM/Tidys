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

VPATH = static $(gembin) $(scsspath) \
        env/lib/python3.4/site-packages make_empty_targets


make_empty_targets:
	mkdir make_empty_targets

dependencies: | make_empty_targets
	sudo apt-get update
	sudo apt-get install python3 python3-dev \
	                     build-essential ruby curl screen
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

css: scss $(bbfoldername) sass
	$(use_gempath) && $(sasscmd) --update $(sasspaths)

.PHONY: run srun drun testenv attach csswatch dcsswatch \
	clean publish

run: dependencies tornado css
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
	rm -rf env __pycache__ $(csspath) $(gempath) \
	       log.log $(bbpath) virtualenv

publish:
	git push $(pub_remote)
