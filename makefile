VIRTUALENV = $(shell which virtualenv)

clean: shutdown
	rm -fr dynamic_hosts.egg-info
	rm -fr venv

venv:
	$(VIRTUALENV) -p /usr/bin/python3.7 venv

install: clean venv
	. venv/bin/activate; python setup.py install
	. venv/bin/activate; python setup.py develop
