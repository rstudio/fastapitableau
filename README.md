# FastAPITableau

FastAPITableau lets you call external Python code from Tableau workbooks via [Tableau Analytics
Extensions](https://tableau.github.io/analytics-extensions-api/). To do this, you write an API using [FastAPI](https://fastapi.tiangolo.com), with some minor modifications. If you aren't already familiar with FastAPI, we suggest you start with their [tutorial](https://fastapi.tiangolo.com/tutorial/). 

The main change required for your API to be callable from Tableau is to replace the `FastAPI` app class with `FastAPITableau`. Where a FastAPI file might start with the 

```python
-from fastapi import FastAPI
+from fastapitableau import FastAPITableau

-app = FastAPI()
+app = FastAPITableau()
``` 

