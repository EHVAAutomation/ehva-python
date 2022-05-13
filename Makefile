
install:
	pip install -r requirements.txt --upgrade
	pip install -r requirements_dev.txt --upgrade
	pip install -e .
	pre-commit install

test:
	pytest

cov:
	pytest --cov= ehva

mypy:
	mypy . --ignore-missing-imports

lint:
	flake8

pylint:
	pylint ehva

lintd2:
	flake8 --select RST

lintd:
	pydocstyle ehva

doc8:
	doc8 docs/

update:
	pur

update-pre:
	pre-commit autoupdate --bleeding-edge
