import json
from typing import Dict, Tuple

from starlette.types import Receive

from fastapitableau.logger import logger
from fastapitableau.utils import event_from_receive


class TableauExtensionMiddleware:
    """
    Rewrite the path of requests sent from Tableau. Tableau sends all its
    requests to the "/evaluate" endpoint. We unpack them and rewrite the path to
    the contents of the "script" key in the request body.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send) -> None:
        logger.debug("Received request with scope: %s", scope, extra={"scope": scope})
        # Strip root_path (e.g. /content/<guid>) to get the app-relative path,
        # matching how FastAPI/Starlette resolve routes behind a proxy.
        path = scope.get("path", "")
        root_path = scope.get("root_path", "")
        if root_path and path.startswith(root_path):
            path = path[len(root_path) :]
        if scope["type"] == "http" and path == "/evaluate":
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

        # Shallow copy is sufficient here because we only replace immutable
        # values (str, bytes). Do not mutate nested structures (e.g. headers,
        # state) on new_scope — they are shared with the original.
        new_scope = scope.copy()
        new_scope["path"] = target_path
        new_scope["raw_path"] = bytes(target_path, encoding="utf-8")

        async def _receive():
            return event

        return new_scope, _receive
