from dataclasses import dataclass
from inspect import Signature, signature
from typing import Any, List


@dataclass
class ParamInfo:
    name: str
    type: str
    tableau_type: str
    required: bool
    default: Any

    def __init__(self, param):
        self.name = param.name
        self.type = param._type_display()
        self.tableau_type = tableau_type_for_python_type(self.type)
        self.required = param.required
        self.default = param.default


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
        self.type = str(return_annotation).removeprefix("typing.")
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
    return_info: ReturnInfo

    def __init__(self, route):
        self.path = route.path
        self.description = route.description
        self.summary = route.summary
        self.body_params = [ParamInfo(param) for param in route.dependant.body_params]
        self.return_info = ReturnInfo(route)
        self.usage = self._tableau_usage_str()

    def _tableau_usage_str(self):
        tableau_funcs = {
            "List[bool]": "SCRIPT_BOOL",
            "List[str]": "SCRIPT_STR",
            "List[int]": "SCRIPT_INT",
            "List[float]": "SCRIPT_REAL",
            "": "SCRIPT_STR",
        }

        if self.return_info.type not in tableau_funcs.keys():
            raise TypeError("Unexpected return type: %s" % (self.return_info.type))
        else:
            tableau_func = tableau_funcs[self.return_info.type]

        params = ", ".join([p.name for p in self.body_params])

        return f'{tableau_func}("{self.path}", {params})'


def extract_routes_info(app):
    routes_info = [
        RouteInfo(route)
        for route in app.routes
        if "TableauRoute" in route.__class__.__name__
    ]
    return routes_info


def tableau_type_for_python_type(python_type: str) -> str:
    tableau_types = {
        "List[bool]": "bool",
        "List[str]": "str",
        "List[int]": "int",
        "List[float]": "real",
        "": "string",
    }

    if python_type not in tableau_types.keys():
        raise TypeError("Unexpected type: %s" % (python_type))
    else:
        tableau_type = tableau_types[python_type]
    return tableau_type
