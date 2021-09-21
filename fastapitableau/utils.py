from typing import Dict, List

from fastapi import Request


def replace_dict_keys(d: Dict, new_keys: List):
    old_keys = sorted(d.keys())
    for old, new in zip(old_keys, new_keys):
        d[new] = d.pop(old)
    return d


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
