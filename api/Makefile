lint:
	flake8 . --exclude migrations/
	black -l 100 --check .
	pydocstyle --convention=numpy --add-ignore=D100,D101,D102,D103,D104,D105,D202 --match-dir=src
format:
	black -l 100 .
test:
	py.test -v -W ignore::DeprecationWarning tests/
update_deps:
	pip-compile --generate-hashes
