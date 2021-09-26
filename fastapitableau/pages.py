import os
from urllib.parse import urlparse

from commonmark import commonmark  # type: ignore[import]
from fastapi import Request
from fastapi.routing import APIRouter
from pkg_resources import resource_filename
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from fastapitableau import rstudio_connect
from fastapitableau.openapi import get_swagger_ui_html
from fastapitableau.user_guide import extract_routes_info
from fastapitableau.utils import calc_app_base_url


def markdown_filter(text):
    return commonmark(text)


templates_directory = resource_filename("fastapitableau", "templates")

statics = StaticFiles(packages=["fastapitableau"])
jinja_templates = Jinja2Templates(directory=templates_directory)
jinja_templates.env.filters["markdown"] = markdown_filter

built_in_pages = APIRouter()


@built_in_pages.get("/", include_in_schema=False)
async def home(request: Request):
    context = {
        "request": request,
        "warning_message": rstudio_connect.warning_message(),
        "app_base_url": calc_app_base_url(request),
    }
    return jinja_templates.TemplateResponse("index.html", context=context)


@built_in_pages.get("/setup_tableau", include_in_schema=False)
async def setup(request: Request):
    server = os.getenv("CONNECT_SERVER", "")
    parts = urlparse(server)
    # <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    server_domain = (
        "<The URL for your RStudio Connect server (e.g. https://connect.example.com)>"
    )
    server_port = "<The port on which your RStudio Connect is listening>"
    netloc = parts.netloc.split(":")
    if len(netloc) > 1:
        server_domain = parts.scheme + "://" + netloc[0]
        server_port = netloc[1]

    context = {
        "request": request,
        "warning_message": rstudio_connect.warning_message(),
        "server_domain": server_domain,
        "server_port": server_port,
        "app_base_url": calc_app_base_url(request),
    }
    return jinja_templates.TemplateResponse("setup_tableau.html", context=context)


@built_in_pages.get("/tableau_usage", include_in_schema=False)
async def tableau_usage(request: Request):
    routes_info = extract_routes_info(
        app=request.app,
        app_base_url=calc_app_base_url(request),
    )
    context = {
        "request": request,
        "warning_message": rstudio_connect.warning_message(),
        "routes_info": routes_info,
        "app_base_url": calc_app_base_url(request),
    }
    return jinja_templates.TemplateResponse("tableau_usage.html", context=context)


# We're bypassing the built-in generation of the docs so we can show two different
# versions of the OpenAPI docs: the default and then one reconfigured for Tableau.
@built_in_pages.get("/docs_standard", include_in_schema=False)
async def docs_openAPI(request: Request):
    root_path = request.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + "/openapi.json"
    request.app.use_tableau_api_schema = False
    app_base_url = calc_app_base_url(request)

    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title="OpenAPI: Standard Web Requests",
        home_url=app_base_url,
    )


@built_in_pages.get("/docs_tableau", include_in_schema=False)
async def docs_tableau_openAPI(request: Request):
    root_path = request.scope.get("root_path", "").rstrip("/")
    openapi_url = root_path + "/openapi.json"
    app_base_url = calc_app_base_url(request)

    request.app.use_tableau_api_schema = True
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title="OpenAPI: Tableau-Style Requests",
        home_url=app_base_url,
    )
