import pytest

import fastapitableau.user_guide as user_guide


@pytest.mark.parametrize(
    "python_type,expected",
    [
        ("List[bool]", "Boolean"),
        ("List[str]", "String"),
        ("List[int]", "Integer (whole number)"),
        ("List[float]", "Real (decimal number)"),
        ("", "String"),
        ("bool", "Boolean"),
        ("str", "String"),
        ("int", "Integer (whole number)"),
        ("float", "Real (decimal number)"),
    ],
)
def test_tableau_name_for_python_type2(python_type, expected):
    assert user_guide.tableau_name_for_python_type(python_type) == expected


def test_custom_type_error():
    with pytest.raises(TypeError):
        user_guide.tableau_name_for_python_type("CustomType")
