import os
from typing import Any, Dict

from fastapi import APIRouter, FastAPI, Request

from fastapitableau.openapi import rewrite_tableau_openapi
from fastapitableau.pages import built_in_pages, statics

from .middleware import TableauExtensionMiddleware
from .routing import TableauRoute


class FastAPITableau(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_middleware(TableauExtensionMiddleware)
        self.router.route_class = TableauRoute
        self.mount("/static", statics, name="static")
        self.include_router(built_in_pages)
        self.include_router(info_router)
        self.docs_url = None  # We will be serving up our own docs
        self.use_tableau_api_schema = False
        self.server_addr = os.getenv("CONNECT_SERVER", "")
        self.appGUID = os.getenv("CONNECT_CONTENT_GUID", "")
        self.appPath = "/"
        if len(self.appGUID) > 0:
            self.appPath = "/connect/#/apps/{}/".format(self.appGUID)
        self.is_connect = False
        if os.getenv("RSTUDIO_PRODUCT", "") == "CONNECT":
            self.is_connect = True

    def openapi(self) -> Dict[str, Any]:
        orig_desc = self.description
        self.openapi_schema = None
        if self.use_tableau_api_schema:
            self.description = (
                orig_desc
                + """
            <br><br>
            `
            NOTE: This documentation outlines the API requests that Tableau will make to the endpoint. They are very different than the standard web requests made available from this FastAPI endpoint.
            `
            """
            )
            schema = super().openapi()
            tableau_paths = [
                "/" + route.name
                for route in self.routes
                if isinstance(route, TableauRoute)
            ]
            self.openapi_schema = rewrite_tableau_openapi(schema, tableau_paths)
        else:
            self.description = (
                orig_desc
                + """
            <br><br>
            `
            NOTE: This documentation outlines the standard web requests made available from this FastAPI endpoint. They are very different than the requests which Tableau will make to this endpoint.
            `
            """
            )
            self.openapi_schema = super().openapi()

        self.description = orig_desc
        return self.openapi_schema


info_router = APIRouter()


@info_router.get("/info", include_in_schema=False)
def info(request: Request):
    return {
        "description": "FastAPITableau API",
        # "creation_time": "0",
        # "state_path": "e:\\dev\\server\\server\\server",
        "server_version": "0.0.1",
        "name": "Server",  # TODO: Make this use the application name
        "versions": {"v1": {"features": {}}},
    }
