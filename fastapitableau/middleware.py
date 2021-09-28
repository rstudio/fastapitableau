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
            _scope, _receive = await self.rewrite_scope_path(scope, receive)
            await self.app(_scope, _receive, send)
        else:
            await self.app(scope, receive, send)

    @staticmethod
    async def rewrite_scope_path(scope: Dict, receive: Receive) -> Tuple[Dict, Receive]:
        # Consume and gather event body
        message_body = b""
        more_body = True
        while more_body:
            message = await receive()
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

        target_path = body["script"]
        if target_path[0] != "/":
            target_path = "/" + target_path

        scope["path"] = target_path
        scope["raw_path"] = bytes(target_path, encoding="utf-8")

        async def _receive():
            return event

        return scope, _receive
