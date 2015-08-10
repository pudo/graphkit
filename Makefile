
test: install
	@env/bin/nosetests --with-coverage --cover-package=graphkit --cover-erase

install: env/bin/python upgrade

env/bin/python:
	virtualenv env

upgrade:
	env/bin/pip install --upgrade pip
	env/bin/pip install -e .
	env/bin/pip install nose coverage unicodecsv python-dateutil

upload:
	env/bin/python setup.py sdist bdist_wheel upload

clean:
	rm -rf env
