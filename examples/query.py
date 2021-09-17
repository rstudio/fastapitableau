from typing import List

from fastapitableau import FastAPITableau

app = FastAPITableau(
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
    "/add_n",
    summary="Adds a number, specified in a query parameter, to a list of floating point numbers",
    response_description="A list of concatenated strings",
)
def add_n(input: List[float], n: float = 0) -> List[float]:
    """
    Given a list of floating point numbers, will add something to each number.

    - **input**: the list of numbers
    - **n** (query parameter): added to each number in input
    """
    return [x + n for x in input]


@app.post(
    "/combine",
)
def combine(
    input1: List[float], input2: List[float], offset: float = 0, scale: float = 0
) -> List[float]:
    added = [a + b for a, b in zip(input1, input2)]
    return [(i * scale) + offset for i in added]
