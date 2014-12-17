runenv = . env/bin/activate
program = run.py
.DEFAULT_GOAL = run
VPATH = static

scssin = static/scss
cssout = static/css

env:
	virtualenv --system-site-packages --python=/usr/bin/python3 env

install: env requirements.txt
	$(runenv); pip install -r requirements.txt
	touch install

css: scss
	sass --update $(scssin):$(cssout)

.PHONY: run srun drun testenv attach

run: install css
	$(runenv); python $(program)

srun:
	screen -S $${PWD##*/} $(MAKE) run

drun:
	screen -d -m -S $${PWD##*/} $(MAKE) run

testenv: env
	$(runenv); python -V

attach:
	screen -r $${PWD##*/}

#Upstream Merge
upsm:
	git pull --no-commit cganterh.net:git/tornadoBoiler.git
