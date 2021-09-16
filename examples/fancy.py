from typing import List

from fastapitableau import FastAPITableau

app = FastAPITableau(
    title="Fancy Example",
    description="A *fancier* example FastAPITableau app.",
    version="0.1.0",
)


@app.post(
    "/capitalize",
    summary="Capitalize a list of strings",
    # description="Capitalize each item in a list of strings"
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
    "Given two lists of strings, iterate over them, concatenating parallel items."

    - **first**: the first list of strings
    - **second**: the second list of strings
    """
    result = [a + " " + b for a, b in zip(first, second)]
    return result


# @app.post(
#     "/add",
#     summary="Add a number to a list of numbers",
#     description="A function that adds a number to a list of numbers. This is intended to test query parameters.",
#     response_description="Numbers with added number"
# )
# def sum(numbers: List[float], to_add: float) -> List[float]:
#     result = [i + to_add for i in numbers]
#     return result
