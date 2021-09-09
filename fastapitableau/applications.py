from typing import Any, Dict

from fastapi import FastAPI

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
