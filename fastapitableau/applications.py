from typing import Any, Dict

from fastapi import APIRouter, FastAPI, Request

from fastapitableau.openapi import rewrite_tableau_openapi

from .middleware import TableauExtensionMiddleware
from .routing import TableauRoute


class FastAPITableau(FastAPI):
    def __init__(self):
        super().__init__()
        self.add_middleware(TableauExtensionMiddleware)
        self.router.route_class = TableauRoute
        self.include_router(info_router)

    def openapi(self) -> Dict[str, Any]:
        if not self.openapi_schema:
            openapi_schema = super().openapi()
            tableau_paths = [
                "/" + route.name
                for route in self.routes
                if isinstance(route, TableauRoute)
            ]
            openapi_schema = rewrite_tableau_openapi(openapi_schema, tableau_paths)
            self.openapi_schema = openapi_schema
        return self.openapi_schema


info_router = APIRouter()


@info_router.get("/info")
def info(request: Request):
    return {
        "description": "FastAPITableau API",
        # "creation_time": "0",
        # "state_path": "e:\\dev\\server\\server\\server",
        "server_version": "0.0.1",
        "name": "Server",  # TODO: Make this use the application name
        "versions": {
            "v1": {
                "features": {
                    "authentication": {"required": True, "methods": {"basic-auth": {}}}
                }
            }
        },
    }
