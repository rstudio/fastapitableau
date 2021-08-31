from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class PasteSchema(BaseModel):
    first: str
    second: str


class TableauRequest(BaseModel):
    script: str = "/paste"
    data: Any


@app.post("/paste")
def paste(tr: TableauRequest) -> str:
    return "yes"
