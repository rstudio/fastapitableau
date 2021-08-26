import json
from typing import Any, Callable, Dict, List, Tuple

from fastapi import FastAPI, Request, Response
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from starlette.types import Receive


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
            self.openapi_schema = openapi_schema
        return self.openapi_schema


class TableauExtensionMiddleware:
    """
    Rewrites requests sent to the "/evaluate" endpoint. To do this, it receives the triggering event and uses the body of the request, then passes on the event in an awaitable object.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] == "http" and scope["path"] == "/evaluate":
            # If we need to handle larger, multipart requests, this is where we should do so.
            _scope, _receive = await rewrite_scope_path(scope, receive)
            await self.app(_scope, _receive, send)
        else:
            await self.app(scope, receive, send)


async def rewrite_scope_path(scope: Dict, receive: Receive) -> Tuple[Dict, Receive]:
    event = await receive()
    print(event)

    body = json.loads(event["body"])
    target_path = body["script"]

    scope["path"] = target_path
    scope["raw_path"] = bytes(target_path, encoding="utf-8")

    async def _receive():
        return event

    return scope, _receive


class TableauRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            _request = await rewrite_request_body(request, self)
            return await original_route_handler(_request)

        return custom_route_handler


async def rewrite_request_body(request: Request, route: APIRoute) -> Request:
    # Extract new, rename args
    event = await request.receive()
    body = json.loads(event["body"])

    # TODO: Better way to detect Tableau origin? Custom header if it is sent to /evaluate maybe?
    if isinstance(body, Dict) and set(body.keys()) == {"script", "data"}:
        data = body["data"]
        if len(data) == 1:
            _body = list(data.values())[0]
        elif len(data) > 1:
            new_keys = [param.name for param in route.dependant.body_params]
            _body = replace_dict_keys(data, new_keys)
        event["body"] = bytes(json.dumps(_body), encoding="utf-8")

    async def _receive():
        return event

    return Request(request.scope, _receive)


def replace_dict_keys(d: Dict, new_keys: List):
    old_keys = sorted(d.keys())
    for old, new in zip(old_keys, new_keys):
        d[new] = d.pop(old)
    return d
