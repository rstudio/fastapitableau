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
