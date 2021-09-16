from dataclasses import dataclass
from inspect import Signature, signature
from typing import Any, List


@dataclass
class ParamInfo:
    name: str
    type: str
    required: bool
    default: Any

    def __init__(self, param):
        self.name = param.name
        self.type = param._type_display()
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
        self.usage = "USAGE TKTKTKTK Lorem Ipsum blah blah"  # TODO


def extract_routes_info(app):
    routes_info = [
        RouteInfo(route)
        for route in app.routes
        if "TableauRoute" in route.__class__.__name__
    ]
    return routes_info
