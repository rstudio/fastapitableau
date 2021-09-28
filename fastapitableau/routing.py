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
        message_body = b""
        more_body = True
        while more_body:
            message = await request.receive()
            message_body += message.get("body", b"")
            more_body = message.get("more_body", False)

        event = {
            "type": message.get("type", "http.request"),
            "body": message_body,
            "more_body": more_body,
        }
        try:
            body = json.loads(event["body"])
        except Exception as e:
            print("Failed to parse event body as JSON: {event}")
            print(e)
            raise e

        if isinstance(body, Dict) and set(body.keys()) == {"script", "data"}:
            data = body["data"]
            if len(data) == 1:
                _body = list(data.values())[0]
            elif (
                len(data) > 1
                and "_arg1" in data.keys()
                and len(self.dependant.body_params) > 0
            ):
                # We only perform this replacement if there are more than zero body params. Otherwise, we will pass through the `data` object with no renaming, so the endpoint can define functions in terms of Tableau arg names.
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
