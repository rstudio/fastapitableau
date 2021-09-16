# Contributing

## Getting set up

### Pipenv

This project uses [Pipenv](https://pipenv.pypa.io/en/latest/).

You can run the following to install Pipenv and set up this project's dependencies.

```
pip install pipenv
pipenv install
```

I *think* this'll install all the packages *and* dev packages listed in the Pipfile. We aren't committing Pipfile.lock because we want to be able to use this environment with different version of Python. You can create a virtualenv with a specific version with a command like `pipenv --python 3.7`.

Pipenv will create a virtual environment, which you can start in a sub-shell by running `pipenv shell`.

### Pre-commit hooks

This project runs a linter and tests in CI. To avoid getting unpleasant errors *after* you've committed stuff, we also have pre-commit hooks which check (and if possible fix) formatting and a few other things as you commit, so you don't have to wait for CI to fail.

I'm not sure if these will be active when you first clone the repo. If they aren't, you can set them up by running the following command in your Pipenv sub-shell.

```
pre-commit install
```

If you get an error from `black` or `isort`, the offending file will be modified, so you can just stage the newly-modified file and try the commit again.

You can skip pre-commit hooks by running running `git commit` with the `no-verify` or `-n` option. Beware, the same things are checked in CI, so you might run into issues down the road.