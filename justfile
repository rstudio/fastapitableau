lint:
	pipenv run isort fastapitableau/ --diff
	pipenv run black --check --diff fastapitableau/
	pipenv run flake8 fastapitableau/
	pipenv run mypy -p fastapitableau

test:
	pipenv run pytest -vv --cov=fastapitableau tests/
