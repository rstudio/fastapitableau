from typing import List

from fastapi import FastAPI

app = FastAPI(
    title="A Simple Example for Tableau",
    description="A *very* simple example FastAPITableau app.",
    version="0.1.0",
)


@app.post(
    "/add_5",
    summary="Adds 5 to a list of floating point numbers",
    response_description="A list of concatenated strings",
)
def add_5(input: List[float]) -> List[float]:
    """
    Given a list of floating point numbers, will add 5.0 to each number.

    - **input**: the list of numbers
    """
    return [x + 5.0 for x in input]


@app.post(
    "/add_two_lists",
    summary="Adds 5 to a list of floating point numbers",
    response_description="A list of concatenated strings",
)
def add_two_lists(first: List[float], second: List[float]) -> List[float]:
    """
    Given a list of floating point numbers, will add 5.0 to each number.

    - **first**: the first list of numbers
    - **second**: the second list of numbers
    """
    result = [a + b for a, b in zip(first, second)]
    return result
