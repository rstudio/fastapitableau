set dotenv-load := true

pre-commit *args:
	@echo "Use 'just -l' to see all available recipes."
	pipenv run pre-commit run {{args}}

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

serve module app="app" app_dir=env_var_or_default("APP_DIR", ""):
	#!/usr/bin/env sh
	if [ -z {{app_dir}} ]; then
		echo "No app directory specified. You can pass it as the second argument to this command or set an environment variable named APP_DIR (perhaps in a .env file at the root of this repo)."
	else
		pipenv run uvicorn {{module}}:{{app}} --app-dir {{app_dir}} --reload
	fi

open_command := if os() == "macos" { "open" } else { "xdg-open" }

cov-report:
	pipenv run pytest --cov=fastapitableau --cov-report=html tests/
	{{open_command}} htmlcov/index.html

clean-dist:
	rm -r dist

build clean="true":
	#!/usr/bin/env sh
	if [ {{clean}} = "true" ]; then
		just clean-dist
	fi
	pipenv run python -m build

testpypi-upload:
	pipenv run python -m twine upload --repository testpypi dist/* --username __token__ --password $TESTPYPI_TOKEN

pypi-upload:
	#!/usr/bin/env sh
	read -p "Are you really ready to publish to PyPI? [y/N] " choice
	case "$choice" in 
	  [Yy]* ) pipenv run python -m twine upload dist/* --username __token__ --password $PYPI_TOKEN;;
	esac

docs-serve:
	pipenv run mkdocs serve

docs-publish:
	#!/usr/bin/env sh
	read -p "Are you sure you want to update the docs on GitHub? [y/N] " choice
	case "$choice" in 
	  [Yy]* ) pipenv run mkdocs gh-deploy;;
	esac
