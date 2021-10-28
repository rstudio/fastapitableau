import logging
import os
import sys
from typing import Optional

from starlette.datastructures import Headers
from starlette.types import Scope


class ScopeAdapter(logging.LoggerAdapter):
    """
    This adapter will prepend the correlation ID of a scope dict passed in via
    the "scope" keyword argument.
    """

    def process(self, msg, kwargs):
        extra = kwargs.get("extra", {})
        if "scope" not in extra.keys():
            return msg, kwargs
        else:
            correlation_id = get_correlation_id(extra["scope"])
            kwargs["extra"]["correlation_id"] = correlation_id
            prefix = f"[{correlation_id}] " if correlation_id is not None else ""
            return prefix + msg, kwargs


def get_correlation_id(scope: Scope = None, headers: Headers = None) -> Optional[str]:
    headers = Headers(scope=scope, headers=headers)
    correlation_id_keys = ["x-rs-correlation-id", "x-correlation-id"]
    for key in correlation_id_keys:
        if key in headers.keys():
            return headers[key]
    return None


base_logger = logging.getLogger("fastapitableau")
base_logger.setLevel(
    getattr(logging, os.environ.get("FASTAPITABLEAU_LOG_LEVEL", "INFO").upper())
)
logging.basicConfig(format="%(message)s", stream=sys.stdout)

# FORMAT = '%(correlation_id)-20s %(message)s'
# logging.basicConfig(format=FORMAT, stream=sys.stdout)

logger = ScopeAdapter(base_logger, {})
