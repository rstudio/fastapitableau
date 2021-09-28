# FastAPI Tableau

[![codecov](https://codecov.io/gh/rstudio/fastapitableau/branch/main/graph/badge.svg?token=E206DENI3A)](https://codecov.io/gh/rstudio/fastapitableau)

FastAPI Tableau lets you call external Python code from Tableau workbooks via [Tableau Analytics
Extensions](https://tableau.github.io/analytics-extensions-api/). To do this, you write an API using [FastAPI](https://fastapi.tiangolo.com), with some minor modifications. If you aren't already familiar with FastAPI, we suggest you start with their [tutorial](https://fastapi.tiangolo.com/tutorial/). 

The main change required for your API to be callable from Tableau is to replace the `FastAPI` app class with `FastAPITableau`.

```python
# Base FastAPI
from fastapi import FastAPI
app = FastAPI()

# FastAPI Tableau
from fastapitableau import FastAPITableau
app = FastAPITableau()
``` 

When you do this, FastAPI Tableau will reroute and transform requests from Tableau, which arrive at the `/evaluate` endpoint, to the endpoints you define in your app. It will also show documentation for Tableau users at the root of your API, with copy-and-paste code samples for Tableau calls.

**Before you write an extension with FastAPI Tableau, you should be familiar with [FastAPI](https://fastapi.tiangolo.com). The [Tutorial](https://fastapi.tiangolo.com/tutorial/) is a great place to start.** You should also take a look at the limitations of FastAPI Tableau extensions, described [below](#tableau-fastapi-supports-a-subset-of-fastapis-features).

## A simple FastAPI Tableau extension

```python
from typing import List

from fastapitableau import FastAPITableau

app = FastAPITableau(
    title="Simple Example",
    description="A *simple* example FastAPITableau app.",
    version="0.1.0",
)


@app.post("/capitalize")
def capitalize(text: List[str]) -> List[str]:
    capitalized = [t.upper() for t in text]
    return capitalized
```

If you put this code in a file named `simple.py` in your terminal's working directory, you can serve it locally using [Uvicorn](https://www.uvicorn.org), by invoking `uvicorn simple:app --reload`.

### Tableau FastAPI extensions support a limited set of data model features

FastAPI Tableau extensions have a few constraints compared to standard FastAPI apps. Some of these are due to the ways that Tableau sends data. We'll describe known limitations here, and how to work within them.

**You cannot use Pydantic models to describe your endpoints' input parameters. Put the arguments in the function definition directly instead.** FastAPI Tableau currently only supports declaring inputs in a function definition, as shown in the examples on this page. We plan to support Pydantic models in the near future. However, these will be subject to the same type and complexity limitations as function arguments, described below.

**All parameters that receive data from Tableau must be [list fields](https://fastapi.tiangolo.com/tutorial/body-nested-models/?h=list#list-fields-with-type-parameter).** Tableau sends its data in JSON lists in the request body, which FastAPI converts to equivalent Python types. Compatible types are `List[str]`, `List[float]`, `List[int]`, and `List[bool]`.

**For compatibility with Tableau, your endpoints should also return one of these compatible list types.** Tableau expects to get back data of the same length as the input data it sent.

**You can add query parameters to your functions by declaring singular (non-`List`) arguments.** FastAPI assumes that any `bool`, `float`, `int`, or `str` variables are query parameters. You can use these in the `script` argument when calling the API from Tableau.

Putting this all together, you can have as many list and singular parameters as you want, declared in the function definition. List parameters will come from Tableau data objects, and singular parameters can be set in the Tableau calculation.

For example, if you wanted an endpoint to multiply data by a user-provided number, you could define it like this:

```python
@app.post("/multiply")
def multiply(numbers: List[float], multiplier: float) -> List[float]:
    result = [i * multiplier for i in numbers]
    return result
```

FastAPI Tableau will automatically generated Tableau usage examples for your endpoints, using your type annotations, so providing complete type annotations will make it easier to use your APIs from Tableau.

### Additional descriptive metadata for endpoints

You can add additional metadata to endpoints as you would with a regular FastAPI app, in the endpoint decorator and the docstring.

```python
@app.post(
    "/paste",
    summary="Parallel concatenation on two lists of strings",
    response_description="A list of concatenated strings",
)
def paste(first: List[str], second: List[str]) -> List[str]:
    """
    Given two lists of strings, iterate over them, concatenating parallel items.

    - **first**: the first list of strings
    - **second**: the second list of strings
    """
    result = [a + " " + b for a, b in zip(first, second)]
    return result
```

This metadata will appear in the documentation for Tableau users.

## Deploying extensions to RStudio Connect.

You can deploy FastAPI Tableau extensions to RStudio Connect with `rsconnect-python`. Detailed documentation can be found [over there](https://github.com/rstudio/rsconnect-python#deploying-python-content-to-rstudio-connect).

```bash
rsconnect deploy fastapi \
    --server https://connect.example.org:3939 \
    --api-key my-api-key \
    my_api_directory/
```

rsconnect-python assumes that your API is the only Python in its directory. For best results, specify your API's dependencies in a `requirements.txt` file in the same directory. See more information [here](https://github.com/rstudio/rsconnect-python#package-dependencies-1).

## Calling an extension endpoint in Tableau

You can copy and paste the usage example (the `SCRIPT_*` command) into a calculated field in Tableau (it generates the correct URL), and replace the argument placeholders with actual values from the Tableau workbook.

### Working with Tableau data

We've found that a few practices in Tableau ensure that the data you pass to a plumbertableau extension is sent correctly.

- You must turn off "Aggregate Measures" under the "Analysis" menu for Tableau to pass the correct values to the extension. If this setting is on, Tableau will send aggregated data to the extension, which may cause inaccuracies in computations.
- With this value off, calculated fields don't allow you to pass raw values directly to an extension. Those values must be wrapped in an aggregating function. Since we've turned "Aggregate Measures" off, these functions won't actually aggregate the data. We've had success using `ATTR([VALUE_NAME])`.
