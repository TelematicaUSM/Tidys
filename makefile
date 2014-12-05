runenv = . env/bin/activate
screename = tornadoBolier

env:
	virtualenv --python=/usr/bin/python3 env

install: env
	$(runenv); pip install -r requirements.txt
	touch install

run: install
	$(runenv); python server.py

runs:
	screen -S $(screename) make run

rund:
	screen -d -m -S $(screename) make run

testenv: env
	$(runenv); python -V

attach:
	screen -r $(screename)
