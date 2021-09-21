from typing import List

from fastapitableau import FastAPITableau

app = FastAPITableau(
    title="Simple Example",
    description="A *simple* example FastAPITableau app.",
    version="0.1.0",
)


@app.post("/capitalize_path")
def capitalize_func(text: List[str]) -> List[str]:
    capitalized = [t.upper() for t in text]
    return capitalized
