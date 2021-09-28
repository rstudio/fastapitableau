from copy import deepcopy
from typing import Dict, List, Optional

from starlette.responses import HTMLResponse

from fastapitableau.utils import replace_dict_keys


def rewrite_tableau_openapi(
    openapi: Dict, rewrite_paths: Optional[List[str]] = None
) -> Dict:
    openapi = deepcopy(openapi)
    schemas = openapi["components"]["schemas"]

    if rewrite_paths is None:
        rewrite_paths = list(openapi["paths"].keys())

    for path_name in rewrite_paths:
        print("Rewriting " + path_name)

        path = openapi["paths"][path_name]
        request_body = path.get("post").get("requestBody")

        if request_body is None:
            continue  # We skip rewriting functions that just take the whole request

        path_schema = request_body["content"]["application/json"]["schema"]

        if "$ref" not in path_schema.keys():
            # Do some moving around of elements to make the single field appear as a referenced schema

            schema_name = "Body_" + path["post"]["operationId"]
            schema_ref = "#/components/schemas/" + schema_name

            # schema = openapi["components"]["schemas"][schema_name]
            lowercase_title = path_schema["title"].lower()

            schema = {
                "title": schema_name,
                "required": [lowercase_title],
                "type": "object",
                "properties": {lowercase_title: path_schema},
            }

            # Replace components with newly created reference schema
            path["post"]["requestBody"]["content"]["application/json"]["schema"] = {
                "$ref": schema_ref
            }
            openapi["components"]["schemas"][schema_name] = schema

            # Overwrite the path_schema object with the new ref
            path_schema = path["post"]["requestBody"]["content"]["application/json"][
                "schema"
            ]

        schema_ref = path_schema["$ref"]
        schema_name = schema_ref.split("/")[-1]

        tab_schema_name = schema_name + "_tableau"
        tab_schema_ref = schema_ref + "_tableau"

        schema = openapi["components"]["schemas"][schema_name]

        # Generate a list of the expected Tableau labels. If it is in `required`, relabel it there, and add it to the list of new keys.
        new_keys: Dict[str, str] = {}
        for i, key in enumerate(schema["properties"].keys()):
            new_key_name = "_arg" + str(i + 1)
            new_keys[key] = new_key_name
            schema["required"] = [
                x if x != key else new_key_name for x in schema["required"]
            ]
        schema["properties"] = replace_dict_keys(schema["properties"], new_keys)
        tab_schema = {
            "title": tab_schema_name,
            "required": ["script", "data"],
            "type": "object",
            "properties": {
                "script": {"title": "Script", "type": "string", "default": path_name},
                "data": {"$ref": schema_ref},
            },
        }

        # Insert the tableau request schema into schemas and change the path schema ref to point to it.
        schemas[tab_schema_name] = tab_schema
        path_schema["$ref"] = tab_schema_ref

    return openapi


# Vendored and modified from FastAPI.
def get_swagger_ui_html(
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
            <a href="{home_url}" class="nav-bar">
                <label class="md-header__button md-icon">
                    <!-- back icon -->
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122.88 122.88"><title>back</title><path class="cls-1" d="M61.44,0A61.51,61.51,0,1,1,18,18,61.25,61.25,0,0,1,61.44,0Zm5,45.27A7.23,7.23,0,1,0,56.14,35.13L35,56.57a7.24,7.24,0,0,0,0,10.15l20.71,21A7.23,7.23,0,1,0,66.06,77.62l-8.73-8.87,24.86-.15a7.24,7.24,0,1,0-.13-14.47l-24.44.14,8.84-9Z"/></svg>
                </label>
                <div class="md-header__title" data-md-component="header-title">
                    <div class="md-header__ellipsis">
                        <div class="md-header__topic">
                            <span class="md-ellipsis">
                                FastAPI Tableau — {title}
                            </span>
                        </div>
                    </div>
                </div>
            </a>
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
