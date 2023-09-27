from typing import Optional

from fastapitableau import utils


def test_replace_dict_keys():
    x = {
        "_arg1": ["foo"],
        "_arg2": ["bar"],
        "_arg3": ["baz"],
    }

    new_keys = {
        "_arg1": "first",
        "_arg2": "second",
        "_arg3": "third",
    }

    replaced = utils.replace_dict_keys(x, new_keys)
    assert list(replaced.keys()) == ["first", "second", "third"]


def test_unwrap_optional():
    # Unwrapped optional value is the same as the original value.
    # Its type is the non-optional version of that type.
    x: Optional[int] = 1
    unwrapped_x = utils.unwrap_optional(x)
    assert unwrapped_x == 1
    assert type(unwrapped_x) is int

    # Unwrapping None is a ValueError.
    x: Optional[str] = None
    try:
        utils.unwrap_optional(x)
    except ValueError:
        pass
    else:
        assert False, "unwrap_optional should have raised ValueError"
