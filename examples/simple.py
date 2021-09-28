from typing import List

from fastapitableau import FastAPITableau

app = FastAPITableau(
    title="Simple FastAPI Tableau Extension",
    description="A very example FastAPITableau app.",
    version="0.1.0",
)


@app.post("/capitalize")
def capitalize(text: List[str]) -> List[str]:
    capitalized = [t.upper() for t in text]
    return capitalized


@app.post("/paste")
def paste(first: List[str], second: List[str]) -> List[str]:
    result = [a + " " + b for a, b in zip(first, second)]
    return result


@app.post("/multiply")
def multiply(numbers: List[float], multiplier: float) -> List[float]:
    result = [i * multiplier for i in numbers]
    return result
