import json
from typing import Dict, Tuple

from starlette.types import Receive


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
