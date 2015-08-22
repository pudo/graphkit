
test: install
	# @rm -f graphkit/**/*.pyc
	@pyenv/bin/nosetests --with-coverage --cover-package=graphkit --cover-erase

install: pyenv/bin/python

pyenv/bin/python:
	virtualenv pyenv
	pyenv/bin/pip install --upgrade pip
	pyenv/bin/pip install nose coverage unicodecsv python-dateutil
	pyenv/bin/pip install git+https://github.com/pudo/jsonmapping
	pyenv/bin/pip install git+https://github.com/pudo/jsongraph
	pyenv/bin/pip install -e .

upload:
	pyenv/bin/python setup.py sdist bdist_wheel upload

clean:
	rm -rf pyenv
