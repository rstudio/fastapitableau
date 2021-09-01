from typing import Any, Dict

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from fastapitableau.openapi import rewrite_tableau_openapi

from .middleware import TableauExtensionMiddleware
from .routing import TableauRoute


class FastAPITableau(FastAPI):
    def __init__(self):
        super().__init__()
        self.add_middleware(TableauExtensionMiddleware)
        self.router.route_class = TableauRoute

    def openapi(self) -> Dict[str, Any]:
        if not self.openapi_schema:
            openapi_schema = get_openapi(
                title=self.title,
                version=self.version,
                openapi_version=self.openapi_version,
                description=self.description,
                terms_of_service=self.terms_of_service,
                contact=self.contact,
                license_info=self.license_info,
                routes=self.routes,
                tags=self.openapi_tags,
                servers=self.servers,
            )
            # This is where custom openapi modification logic will go
            tableau_paths = [
                "/" + route.name
                for route in self.routes
                if isinstance(route, TableauRoute)
            ]
            openapi_schema = rewrite_tableau_openapi(openapi_schema, tableau_paths)
            self.openapi_schema = openapi_schema
        return self.openapi_schema
