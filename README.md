# FastAPITableau

FastAPITableau lets you call external Python code from Tableau workbooks via [Tableau Analytics
Extensions](https://tableau.github.io/analytics-extensions-api/). To do this, you write an API using [FastAPI](https://fastapi.tiangolo.com), with some minor modifications. If you aren't already familiar with FastAPI, we suggest you start with their [tutorial](https://fastapi.tiangolo.com/tutorial/). 

The main change required for your API to be callable from Tableau is to replace the `FastAPI` app class with `FastAPITableau`.

```diff
-from fastapi import FastAPI
+from fastapitableau import FastAPITableau

-app = FastAPI()
+app = FastAPITableau()
``` 

When you do this, FastAPITableau will correctly route and transform requests from Tableau, which arrive at the `/evaluate` endpoint, to endpoints you define in your app. It will also show documentation for Tableau users at the root of your API, with copy-and-paste code samples for Tableau calls.

## A simple FastAPITableau extension

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

You can add additional metadata to endpoints as you would with a regular Tableau extension, in the endpoint decorator and the docstring.

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

## Deploying to RStudio Connect.

You can deploy FastAPITableau extensions to RStudio Connect with `rsconnect-python`. Detailed documentation can be found [over there](https://github.com/rstudio/rsconnect-python#deploying-python-content-to-rstudio-connect).

rsconnect-python assumes that your API is the only Python in its directory. For best results, specify your API's dependencies in a `requirements.txt` file in the same directory. See more information [here](https://github.com/rstudio/rsconnect-python#package-dependencies-1).

rsconnect deploy fastapi \
    --server https://connect.example.org:3939 \
    --api-key my-api-key \
    my_api_directory/
