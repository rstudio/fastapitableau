import pytest

from fastapitableau import user_guide

from .main import app


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
        ("CustomType", "<Warning: No equivalent Tableau type for 'CustomType'>"),
    ],
)
def test_tableau_name_for_python_type2(python_type, expected):
    assert user_guide.tableau_name_for_python_type(python_type) == expected


# Confirm that parameters are populated as expected. This is to ensure that we
# catch any name changes that might occur when our dependencies change.
def test_param_info_creation():
    r = app.router.routes[-6]
    p = r.dependant.body_params[0]
    param_info = user_guide.ParamInfo(p)
    assert param_info.name == "numbers"
    assert param_info.type == "List[float]"
    assert param_info.tableau_type == "Real (decimal number)"
    assert param_info.required is True
    assert param_info.default is user_guide.PydanticUndefined
    assert param_info.details == "Required"


# Confirm that return value information is extracted as expected.
def test_return_info_creation():
    r = app.router.routes[-6]
    return_info = user_guide.ReturnInfo(r)
    assert return_info.type == "List[float]"
    assert return_info.desc == "Numbers with added number"


# Confirm that route information is extracted as expected.
def test_route_info_creation():
    r = app.router.routes[-6]
    route_info = user_guide.RouteInfo(r)

    assert route_info.path == "/multiply"
    assert route_info.usage == 'SCRIPT_REAL("/multiply", numbers)'
    assert route_info.summary == "An endpoint that requires a query parameter"
    assert (
        route_info.description
        == "A function that adds a number to a list of numbers. This is intended to test query parameters."
    )
    assert (
        repr(route_info.body_params)
        == "[ParamInfo(name='numbers', type='List[float]', tableau_type='Real (decimal number)', required=True, default=PydanticUndefined, details='Required')]"
    )
    assert (
        repr(route_info.query_params)
        == "[ParamInfo(name='multiplier', type='float', tableau_type='Real (decimal number)', required=True, default=PydanticUndefined, details='Required')]"
    )
    assert (
        repr(route_info.return_info)
        == "ReturnInfo(type='List[float]', desc='Numbers with added number')"
    )
