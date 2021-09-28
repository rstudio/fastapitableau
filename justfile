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

open_command := if os() == "macos" { "open" } else { "xdg-open" }

cov-report:
	pipenv run pytest --cov=fastapitableau --cov-report=html tests/
	{{open_command}} htmlcov/index.html
