from typing import List

from fastapi import FastAPI

app = FastAPI()


@app.post("/capitalize")
def capitalize(text: List[str]) -> List[str]:
    capitalized = [t.upper() for t in text]
    return capitalized


@app.post("/paste")
def paste(first: List[str], second: List[str]) -> List[str]:
    result = [a + " " + b for a, b in zip(first, second)]
    return result


@app.post("/sum")
def sum(numbers: List[float]) -> List[float]:
    summed = sum(numbers)
    return summed
