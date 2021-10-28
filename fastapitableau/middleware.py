import json
from typing import Dict, Tuple

from starlette.types import Receive

from fastapitableau.logger import logger
from fastapitableau.utils import event_from_receive


class TableauExtensionMiddleware:
    """
    Rewrites requests sent to the "/evaluate" endpoint. To do this, it receives the triggering event and uses the body of the request, then passes on the event in an awaitable object.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send) -> None:
        logger.debug("Received request with scope: %s", scope, extra={"scope": scope})
        if scope["type"] == "http" and scope["path"] == "/evaluate":
            _scope, _receive = await self.rewrite_scope_path(scope, receive)
            await self.app(_scope, _receive, send)
        else:
            await self.app(scope, receive, send)

    @staticmethod
    async def rewrite_scope_path(scope: Dict, receive: Receive) -> Tuple[Dict, Receive]:
        event = await event_from_receive(receive)

        logger.debug("Received event: %s", event, extra={"scope": scope})

        try:
            body = json.loads(event["body"])
        except Exception as e:
            print("Failed to parse event body as JSON: {event}")
            print(e)
            raise e

        target_path = body["script"]
        if target_path[0] != "/":
            target_path = "/" + target_path

        logger.debug(
            "Rewriting path for Tableau request: '%s'",
            target_path,
            extra={"scope": scope},
        )

        scope["path"] = target_path
        scope["raw_path"] = bytes(target_path, encoding="utf-8")

        async def _receive():
            return event

        return scope, _receive
