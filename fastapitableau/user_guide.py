from dataclasses import dataclass
from inspect import Signature, signature
from typing import Any, List, Optional
from urllib.parse import urljoin, urlparse

from fastapitableau.utils import remove_prefix


@dataclass
class ParamInfo:
    name: str
    type: str
    tableau_type: str
    required: bool
    default: Any
    details: str

    def __init__(self, param):
        self.name = param.name
        self.type = param._type_display()
        self.tableau_type = tableau_name_for_python_type(self.type)
        self.required = param.required
        self.default = param.default
        self.details = self._details()

    def _details(self) -> str:
        parts = []
        parts.append("required") if self.required else parts.append("optional")
        if self.default is not None:
            parts.append(f"default = {self.default}")
        return "; ".join(parts).capitalize()


@dataclass
class ReturnInfo:
    type: str
    desc: str

    def __init__(self, route):
        sig = signature(route.dependant.call)
        return_annotation = (
            sig.return_annotation
            if sig.return_annotation is not Signature.empty
            else None
        )
        self.type = remove_prefix(str(return_annotation), "typing.")
        self.desc = (
            route.response_description
            if route.response_description != "Successful Response"
            else ""
        )


@dataclass
class RouteInfo:
    path: str
    usage: str
    summary: str
    description: str
    body_params: List[ParamInfo]
    query_params: List[ParamInfo]
    return_info: ReturnInfo
    name: str

    def __init__(self, route, app_base_url: Optional[str]):
        if app_base_url:
            # Displays the path relative to the Connect domain, for Tableau purposes.
            self.path = urljoin(urlparse(app_base_url).path, route.path.strip("/"))
        else:
            self.path = route.path
        self.description = route.description
        self.summary = route.summary
        self.body_params = [ParamInfo(param) for param in route.dependant.body_params]
        self.query_params = [ParamInfo(param) for param in route.dependant.query_params]
        self.return_info = ReturnInfo(route)
        self.usage = self._tableau_usage_str()
        self.name = route.path.lstrip("/")

    def _tableau_usage_str(self):
        tableau_funcs = {
            "List[bool]": "SCRIPT_BOOL",
            "List[str]": "SCRIPT_STR",
            "List[int]": "SCRIPT_INT",
            "List[float]": "SCRIPT_REAL",
            "": "SCRIPT_STR",
        }

        if self.return_info.type not in tableau_funcs.keys():
            return f"<Warning: Cannot determine Tableau script command for return type '{self.return_info.type}'>"
        else:
            tableau_func = tableau_funcs[self.return_info.type]

        params = ", ".join([p.name for p in self.body_params])

        return f'{tableau_func}("{self.path}", {params})'


def extract_routes_info(app, app_base_url: Optional[str]):
    routes_info = [
        RouteInfo(route, app_base_url)
        for route in app.routes
        if "TableauRoute" in route.__class__.__name__
    ]
    return routes_info


def tableau_name_for_python_type(python_type: str) -> str:
    if "bool" in python_type:
        tableau_type = "Boolean"
    elif "str" in python_type:
        tableau_type = "String"
    elif "int" in python_type:
        tableau_type = "Integer (whole number)"
    elif "float" in python_type:
        tableau_type = "Real (decimal number)"
    elif python_type == "":
        tableau_type = "String"
    else:
        return f"<Warning: No equivalent Tableau type for '{python_type}'>"

    return tableau_type
