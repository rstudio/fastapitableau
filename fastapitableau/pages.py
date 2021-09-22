import os
from urllib.parse import urlparse

from commonmark import commonmark  # type: ignore[import]
from fastapi import Request
from fastapi.routing import APIRouter
from pkg_resources import resource_filename
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from fastapitableau import rstudio_connect
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

    return custom_get_swagger_ui_html(
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
    return custom_get_swagger_ui_html(
        openapi_url=openapi_url,
        title="OpenAPI: Tableau-Style Requests",
        home_url=app_base_url,
    )


# cloned from FastAPI library..
def custom_get_swagger_ui_html(
    *,
    openapi_url: str,
    title: str,
    swagger_js_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui-bundle.js",
    swagger_css_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@3/swagger-ui.css",
    swagger_favicon_url: str = "https://fastapi.tiangolo.com/img/favicon.png",
    home_url: str,
) -> HTMLResponse:

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <link rel="shortcut icon" href="{swagger_favicon_url}">
    <link rel="stylesheet" type="text/css" href="static/css/styles.css">
    <title>{title}</title>
    </head>
    <body>

    <!-- BEGIN: Insert our header into the documentation -->
    <header class="md-header" data-md-component="header" data-md-state="shadow">
        <nav class="md-header__inner md-grid" aria-label="Header">
        <a href="{home_url}">
            <label class="md-header__button md-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122.88 113.97"><path d="M18.69,73.37,59.18,32.86c2.14-2.14,2.41-2.23,4.63,0l40.38,40.51V114h-30V86.55a3.38,3.38,0,0,0-3.37-3.37H52.08a3.38,3.38,0,0,0-3.37,3.37V114h-30V73.37ZM60.17.88,0,57.38l14.84,7.79,42.5-42.86c3.64-3.66,3.68-3.74,7.29-.16l43.41,43,14.84-7.79L62.62.79c-1.08-1-1.24-1.13-2.45.09Z"></path></svg>
            </label>
        </a>
        <div class="md-header__title" data-md-component="header-title">
            <div class="md-header__ellipsis">
            <div class="md-header__topic">
                <span class="md-ellipsis">
                    FastAPI Tableau — {title}
                </span>
            </div>
            </div>
        </div>
        </nav>
    </header>
    <!-- END: Insert our header into the documentation -->

    <!-- BEGIN: Small container to make positions consistent between this and other pages -->
    <div class="swagger-container">
    <!-- END: Small container -->

    <div id="swagger-ui">
    </div>

    <!-- BEGIN: Close our small container -->
    </div>
    <!-- END: Close small container -->

    <script src="{swagger_js_url}"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
    const ui = SwaggerUIBundle({{
        url: '{openapi_url}',
    """

    html += """
        dom_id: '#swagger-ui',
        presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout",
        deepLinking: true,
        showExtensions: true,
        showCommonExtensions: true
    })"""

    html += """
    </script>
    </body>
    </html>
    """
    return HTMLResponse(html)
