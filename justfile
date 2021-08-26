lint:
	pipenv run isort --check --diff fastapitableau/
	pipenv run black --check --diff fastapitableau/
	pipenv run flake8 fastapitableau/
	pipenv run mypy -p fastapitableau

lint-fix:
	pipenv run isort fastapitableau/
	pipenv run black fastapitableau/

test:
	pipenv run pytest -vv --cov=fastapitableau tests/

serve filename app="app":
	pipenv run uvicorn {{filename}}:{{app}} --app-dir examples --reload