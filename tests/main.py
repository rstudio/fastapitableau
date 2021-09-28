import json
from typing import Dict, List

from fastapi import HTTPException, Request

from fastapitableau import FastAPITableau


def make_data(endpoint: str, data: List) -> str:
    body = {
        "script": endpoint,
        "data": {"_arg" + str(i + 1): elem for i, elem in enumerate(data)},
    }
    return json.dumps(body)


app = FastAPITableau(
    title="Example API",
    description="An API for testing.",
    version="0.1.0",
)


@app.post(
    "/capitalize",
    summary="An endpoint that requires a single argument.",
    # description="Capitalize each item in a list of strings"
)
def capitalize(text: List[str]) -> List[str]:
    capitalized = [t.upper() for t in text]
    return capitalized


@app.post(
    "/paste",
    summary="An endpoint that requires two arguments.",
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


@app.post(
    "/multiply",
    summary="An endpoint that requires a query parameter",
    description="A function that adds a number to a list of numbers. This is intended to test query parameters.",
    response_description="Numbers with added number",
)
def multiply(numbers: List[float], multiplier: float) -> List[float]:
    result = [i * multiplier for i in numbers]
    return result


@app.post(
    "/fail",
    summary="Fails and raises an HTTP Exception",
    # description="Capitalize each item in a list of strings"
)
def fail(text: List[str]) -> None:
    raise HTTPException(status_code=420, detail="This didn't work")


@app.post(
    "/weird_type",
    summary="This endpoint has a Tableau-incompatible type signature.",
    # description="Capitalize each item in a list of strings"
)
def weird_type(text: List[Dict]) -> List[str]:
    raise HTTPException(status_code=420, detail="This didn't work")


@app.post(
    "/variadic",
    summary="Fails and raises an HTTP Exception",
    # description="Capitalize each item in a list of strings"
)
async def variadic(request: Request) -> Dict[str, List[str]]:
    result = await request.json()
    return result
