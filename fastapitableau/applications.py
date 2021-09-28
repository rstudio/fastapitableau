from typing import Any, Dict

from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from fastapitableau.exception_handlers import (
    tableau_general_exception_handler,
    tableau_http_exception_handler,
    tableau_request_validation_exception_handler,
)
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
        if not self.description:
            self.description = "Description not provided"

        # Add exception handlers
        self.exception_handlers[HTTPException] = tableau_http_exception_handler
        self.exception_handlers[
            RequestValidationError
        ] = tableau_request_validation_exception_handler
        self.exception_handlers[Exception] = tableau_general_exception_handler
        self.middleware_stack = self.build_middleware_stack()

    def openapi(self) -> Dict[str, Any]:
        orig_desc = self.description
        self.openapi_schema = None
        if self.use_tableau_api_schema:
            self.description = (
                orig_desc
                + """
            <br><br>
            *NOTE: This page's example API requests are formatted like the requests that Tableau will send. They are different from standard web requests, which are documented [here](../docs_standard).*
            """
            )
            schema = super().openapi()
            tableau_paths = [
                route.path for route in self.routes if isinstance(route, TableauRoute)
            ]
            self.openapi_schema = rewrite_tableau_openapi(schema, tableau_paths)
        else:
            self.description = (
                orig_desc
                + """
            <br><br>
            *NOTE: This page's example API requests are formatted like standard web requests. They are different from the requests that Tableau will send, which are documented [here](../docs_tableau).*
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
        "name": request.app.title,
        "versions": {"v1": {"features": {}}},
    }
