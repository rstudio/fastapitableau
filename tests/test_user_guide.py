import pytest
import pytest_subtests  # type: ignore[import]

import fastapitableau.user_guide as user_guide

subtests = pytest_subtests.subtests


def test_tableau_name_for_python_type(subtests):
    test_values = {
        "List[bool]": "Boolean",
        "List[str]": "String",
        "List[int]": "Integer (whole number)",
        "List[float]": "Real (decimal number)",
        "": "String",
        "bool": "Boolean",
        "str": "String",
        "int": "Integer (whole number)",
        "float": "Real (decimal number)",
    }
    for python, expected in test_values.items():
        with subtests.test(msg=python, python=python, expected=expected):
            assert user_guide.tableau_name_for_python_type(python) == expected

    with pytest.raises(TypeError):
        user_guide.tableau_name_for_python_type("CustomType")
