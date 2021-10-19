# Contributing

## The setup

### Manage your dev Python environment with Pipenv

This project uses [Pipenv](https://pipenv.pypa.io/en/latest/).

You can run the following to install Pipenv and set up this project's dependencies.

```
pip install pipenv
pipenv install --dev
```

I *think* this'll install all the packages *and* dev packages listed in the Pipfile. We aren't committing Pipfile.lock because we want to be able to use this environment with different version of Python. You can create a virtualenv with a specific version with a command like `pipenv --python 3.7`.

Pipenv will create a virtual environment, which you can start in a sub-shell by running `pipenv shell`.

### Check code with pre-commit hooks

We run linting and testing in CI (only on pull requests to `main` and pushes to `main` or tagged branches, not with every commit.)

To avoid getting unpleasant errors in CI *after* you've committed stuff, we also have pre-commit hooks which check (and if possible fix) formatting and a few other things as you commit, so you don't have to wait for CI to fail.

You need to run the following in your terminal to add the pre-commit hooks to your repo.

```
pipenv shell
pre-commit install
```

Once this is set up, `git commit` will take longer, because `isort`, `black`, `flake8`, `mypy`, and `pytest` will run and must succeed before the commit happens.

If they fail, they'll include the reason why in the output. You'll need to fix it, `git add` the fix, and try your commit again. Note: if they are able to parse the offending files, `isort` and `black` will automatically fix any issues. You'll almost always be able to `git add` their changes and run your commit again.

You can skip pre-commit hooks by running running `git commit` with the `no-verify` or `-n` option. Beware, the same checks are run in CI, so you might run into issues down the road.

There are issues where something might fail in CI, even if it passes these checks. This is because CI runs across all supported Python versions, and these checks only run in your Pipenv virtualenv.

Within the Pipenv virtualenv, you can run `pre-commit run` to run the checks ahead of time on staged files, or `pre-commit run --all` to run everything. If your Pipenv shell isn't active, you can also type `just pre-commit [--all]`. Which brings me to…

### Run common commands with `just`

This project uses [`just`](https://github.com/casey/just) to run commands. Check the list of available recipes by running `just -l` or `just --list`.

The default recipe, which runs when you type `just`, runs the pre-commit hooks on staged files.

#### Serving FastAPI Tableau content locally

Use `just serve [module]` to start up a Uvicorn server running FastAPI Tableau content from another directory.

- The `module` argument is required. It's the name of the Python file containing your app, minus the `.py` suffix.
- If the file's app object is named something other than `app`, you need to pass a second argument giving its name.
- Your content must be in a different directory, and you can specify it in a few ways.
    - By default, `just` will look in the directory specified by the environment variable `APP_DIR`.
    - If there's no environment variable defined, it'll look in a file named `.env` file, which might contain something like `APP_DIR=../fastapitableau-apps`. (This is a [`just` feature](https://github.com/casey/just#dotenv-integration). I like this "set it and forget it" option.)
    - If you want to serve something from a different directory, you can pass its path as third positional argument.

So you could run `just serve simple`, or `just serve complicated server_object /path/to/app/dir`.
