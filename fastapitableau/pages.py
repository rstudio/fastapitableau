from commonmark import commonmark  # type: ignore[import]
from fastapi import Request
from fastapi.routing import APIRouter
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from fastapitableau import rstudio_connect, templates
from fastapitableau.user_guide import extract_routes_info

try:
    from importlib.resources import files  # type: ignore[attr-defined]
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    from importlib_resources import files  # type: ignore[import, no-redef]


def markdown_filter(text):
    return commonmark(text)


template_files = files(templates)

statics = StaticFiles(packages=["fastapitableau"])
jinja_templates = Jinja2Templates(directory=template_files)  # type: ignore[arg-type]
jinja_templates.env.filters["markdown"] = markdown_filter

built_in_pages = APIRouter()


@built_in_pages.get("/")
async def home(request: Request):
    routes_info = extract_routes_info(request.app)
    context = {
        "request": request,
        "warning_message": rstudio_connect.warning_message(),
        "routes_info": routes_info,
    }
    return jinja_templates.TemplateResponse("index.html", context=context)


@built_in_pages.get("/user_guide")
async def user_guide(request: Request):
    routes = request.app.routes
    context = {"title": request.app.title, "routes": routes, "request": request}
    return jinja_templates.TemplateResponse("user_guide.html", context=context)
