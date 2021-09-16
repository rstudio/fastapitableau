from commonmark import commonmark  # type: ignore[import]
from fastapi import Request
from fastapi.routing import APIRouter
from pkg_resources import resource_filename
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from fastapitableau import rstudio_connect
from fastapitableau.user_guide import extract_routes_info


def markdown_filter(text):
    return commonmark(text)


templates_directory = resource_filename("fastapitableau", "templates")

statics = StaticFiles(packages=["fastapitableau"])
jinja_templates = Jinja2Templates(directory=templates_directory)
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
