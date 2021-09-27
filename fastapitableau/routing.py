import json
from typing import Callable, Dict

from fastapi import Request, Response
from fastapi.routing import APIRoute

from .utils import replace_dict_keys


class TableauRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            _request = await self.rewrite_request_body(request)
            return await original_route_handler(_request)

        return custom_route_handler

    async def rewrite_request_body(self, request: Request) -> Request:
        # Extract new, rename args
        event = await request.receive()
        body = json.loads(event["body"])

        # TODO: Better way to detect Tableau origin? Custom header if it is sent to /evaluate maybe?
        if isinstance(body, Dict) and set(body.keys()) == {"script", "data"}:
            data = body["data"]
            if len(data) == 1:
                _body = list(data.values())[0]
            elif len(data) > 1 and "_arg1" in data.keys():
                new_keys: Dict[str, str] = {}
                for i, param in enumerate(self.dependant.body_params):
                    new_keys["_arg" + str(i + 1)] = param.name
                _body = replace_dict_keys(data, new_keys)
            else:
                _body = data
            event["body"] = bytes(json.dumps(_body), encoding="utf-8")

        async def _receive():
            return event

        return Request(request.scope, _receive)
