from typing import List

from fastapitableau import FastAPITableau

app = FastAPITableau(
    title="A Simple Example for Tableau",
    description="A *very* simple example FastAPITableau app.",
    version="0.1.0",
)


@app.post("/add_5")
def add_5(input: List[float]) -> List[float]:
    return [x + 5 for x in input]


@app.post("/paste")
def paste(first: List[str], second: List[str]) -> List[str]:
    result = [a + " " + b for a, b in zip(first, second)]
    return result


# @app.post("/sum")
# def sum(numbers: List[float]) -> List[float]:
#     summed = sum(numbers)
#     return summed
