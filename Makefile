test:
	pytest .

lint: 
	flake8

black:
	black --check .

fix-black:
	black .

typecheck:
	mypy .

coverage:
	pytest tests/ --cov=deadlock_middleware/ --cov-branch --cov-report term-missing:skip-covered

sort:
	isort -rc . -c

fix-sort:
	isort -rc .

precommit:
	$(MAKE) test
	$(MAKE) lint
	$(MAKE) black
	$(MAKE) typecheck
	$(MAKE) sort

delete-cache:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf