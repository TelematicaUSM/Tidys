runenv = . env/bin/activate
program = run.py
VPATH = static
.DEFAULT_GOAL = run

env:
	virtualenv --system-site-packages --python=/usr/bin/python3 env

install: env requirements.txt
	$(runenv); pip install -r requirements.txt
	touch install

css: scss
	sass --update static/scss:static/css

.PHONY: run srun drun testenv attach show

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
