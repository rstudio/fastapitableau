from typing import List

from fastapi import Body
from pydantic import BaseModel, Field

from fastapitableau import FastAPITableau

app = FastAPITableau(
    title="Fancy Example",
    description="A *fancier* example FastAPITableau app.",
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
    "Given two lists of strings, iterate over them, concatenating parallel items."

    - **first**: the first list of strings
    - **second**: the second list of strings
    """
    result = [a + " " + b for a, b in zip(first, second)]
    return result


class TextModelForCapitalize2(BaseModel):
    text: List[str] = Field(
        None,
        title="The text to capitalize",
    )


@app.post(
    "/capitalize2",
    summary="Capitalize a list of strings",
    description="Capitalize each item in a list of strings",
)
def capitalize2(text: TextModelForCapitalize2 = Body(..., embed=True)) -> List[str]:
    capitalized = [t.upper() for t in text]
    return capitalized
