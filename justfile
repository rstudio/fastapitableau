lint:
	pipenv run isort --check --diff fastapitableau/ tests/ examples/
	pipenv run black --check --diff fastapitableau/ tests/ examples/
	pipenv run flake8 fastapitableau/ tests/ examples/
	pipenv run mypy -p fastapitableau

lint-fix:
	pipenv run isort fastapitableau/ tests/ examples/
	pipenv run black fastapitableau/ tests/ examples/

test:
	pipenv run pytest -vv --cov=fastapitableau tests/

serve filename app="app":
	pipenv run uvicorn {{filename}}:{{app}} --app-dir examples --reload

open_command := if os() == "macos" { "open" } else { "xdg-open" }

cov-report:
	pipenv run pytest --cov=fastapitableau --cov-report=html tests/
	{{open_command}} htmlcov/index.html
