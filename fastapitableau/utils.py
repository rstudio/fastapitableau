from typing import Dict

from fastapi import Request
from starlette.types import Receive


def replace_dict_keys(old_dict: Dict, new_keys: Dict[str, str]):
    new_dict: Dict = {}
    for old, new in new_keys.items():
        new_dict[new] = old_dict[old]
    return new_dict


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def calc_app_base_url(request: Request):
    app_base_url = request.headers.get("RStudio-Connect-App-Base-URL")
    if not app_base_url:
        app_base_url = "/"
    elif app_base_url[-1] != "/":
        app_base_url += "/"
    return app_base_url


async def event_from_receive(receive: Receive) -> Dict:
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

    return event
