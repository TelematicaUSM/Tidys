runenv = . env/bin/activate
program = server.py

env:
	virtualenv --system-site-packages --python=/usr/bin/python3 env

install: env requirements.txt
	$(runenv); pip install -r requirements.txt
	touch install

run: install
	$(runenv); python $(program)

runs:
	screen -S $${PWD##*/} make run

rund:
	screen -d -m -S $${PWD##*/} make run

testenv: env
	$(runenv); python -V

attach:
	screen -r $${PWD##*/}
