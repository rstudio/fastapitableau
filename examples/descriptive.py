from typing import List

from fastapitableau import FastAPITableau

app = FastAPITableau(
    title="Fancier FastAPI Tableau Extension",
    description="A *fancier* example FastAPITableau app, with more descriptive metadata",
    version="0.1.0",
)


@app.post(
    "/capitalize",
    summary="Capitalize a list of strings",
    description="Capitalize each item in a list of strings",
)
def capitalize(text: List[str]) -> List[str]:
    capitalized = [t.upper() for t in text]
    return capitalized


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


@app.post(
    "/multiply",
    summary="Multiply some data by a number",
    description="A function that multiplies a list of data by a number. The multiplier is provided as a query parameter.",
    response_description="Multiplied numbers",
)
def multiply(numbers: List[float], multiplier: float) -> List[float]:
    result = [i * multiplier for i in numbers]
    return result
