from typing import Dict, List


def replace_dict_keys(d: Dict, new_keys: List):
    old_keys = sorted(d.keys())
    for old, new in zip(old_keys, new_keys):
        d[new] = d.pop(old)
    return d


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text
