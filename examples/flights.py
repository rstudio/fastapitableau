from typing import List

from fastapi import Request

from fastapitableau import FastAPITableau

app = FastAPITableau(
    title="Simple Example",
    description="A *simple* example FastAPITableau app.",
    version="0.1.0",
)


@app.post("/flights")
def flights(
    year: List[str],
    month: List[str],
    day: List[str],
    dep_time: List[str],
    sched_dep_time: List[str],
) -> List[str]:
    return ["Yes"]


@app.post("/paste")
def paste(first: List[str], second: List[str]) -> List[str]:
    result = [a + " " + b for a, b in zip(first, second)]
    return result


@app.post("/capitalize")
def capitalize(text: List[str]) -> List[str]:
    capitalized = [t.upper() for t in text]
    return capitalized


@app.post("/test")
async def test(req: Request):
    return await req.json()
