import logging
import os
import sys

log = logging.getLogger("connect_fastapi_runtime")
log.setLevel(getattr(logging, os.environ.get("LOG_LEVEL", "INFO").upper()))
logging.basicConfig(format="%(message)s", stream=sys.stdout)


class VerboseLoggingMiddleware:  # pragma: no cover
    def __init__(self, app):
        self.app = app
        log.setLevel(logging.DEBUG)

    async def __call__(self, scope, receive, send) -> None:
        log.debug("\nConnectVerboseLoggingMiddleware: scope = %s", scope)

        async def _receive():
            event = await receive()
            log.debug("\nreceive: %s for scope %s", event, scope)
            return event

        async def _send(event):
            log.debug("\nsend: %s for scope %s", event, scope)
            await send(event)

        await self.app(scope, _receive, _send)
