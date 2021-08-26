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

We also have pre-commit hooks which check (and if possible fix) formatting and a few other things as you commit, so you don't have to wait for CI to fail to see where your formatting is wrong.

You should be able to get set up with these by running the following command in your Pipenv sub-shell.

```
pre-commit install
```

Maybe this isn't required? I'm not actually sure if the pre-commit hooks get tracked in the repo.
