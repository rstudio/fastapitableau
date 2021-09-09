from commonmark import commonmark  # type: ignore[import]
from fastapi import Request
from fastapi.routing import APIRouter
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import fastapitableau.templates

try:
    import importlib.resources as resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as resources  # type: ignore[import, no-redef]


def markdown_filter(text):
    return commonmark(text)


template_dir = resources.files(fastapitableau.templates)

statics = StaticFiles(packages=["fastapitableau"])
templates = Jinja2Templates(directory=template_dir)  # type: ignore[arg-type]
templates.env.filters["markdown"] = markdown_filter

built_in_pages = APIRouter()


@built_in_pages.get("/")
async def home(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context=context)


@built_in_pages.get("/user_guide")
async def user_guide(request: Request):
    routes = request.app.routes
    context = {"title": request.app.title, "routes": routes, "request": request}
    return templates.TemplateResponse("user_guide.html", context=context)
