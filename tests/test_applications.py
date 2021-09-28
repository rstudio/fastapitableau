import pytest
from fastapi.testclient import TestClient

from .main import app, make_data

client = TestClient(app)


def test_openapi_ui():
    response = client.get("docs_standard")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "swagger-ui-dist" in response.text

    response = client.get("docs_tableau")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "swagger-ui-dist" in response.text


def test_openapi_function():
    app.use_tableau_api_schema = False
    openapi_standard = app.openapi()
    assert list(openapi_standard["components"]["schemas"].keys()) == [
        "Body_paste_paste_post",
        "HTTPValidationError",
        "ValidationError",
    ]

    app.use_tableau_api_schema = True
    openapi_tableau = app.openapi()
    assert list(openapi_tableau["components"]["schemas"].keys()) == [
        "Body_paste_paste_post",
        "HTTPValidationError",
        "ValidationError",
        "Body_capitalize_capitalize_post",
        "Body_capitalize_capitalize_post_tableau",
        "Body_paste_paste_post_tableau",
        "Body_sum_multiply_post",
        "Body_sum_multiply_post_tableau",
        "Body_fail_fail_post",
        "Body_fail_fail_post_tableau",
        "Body_weird_type_weird_type_post",
        "Body_weird_type_weird_type_post_tableau",
    ]


def test_failure():
    response = client.post(
        "/evaluate",
        json={"script": "/fail", "data": {"_arg1": ["Toph", "Bill", "James"]}},
    )
    assert response.status_code == 420, (
        response.text
        == '{"message":"Server Error: HTTPException","info":"This didn\'t work"}'
    )


def test_single_arg_endpoint_tableau():
    data = make_data("/capitalize", [["dog", "cat", "bunny"]])
    response = client.post("/evaluate", data=data)
    assert response.status_code == 200, response.json() == ["DOG", "CAT", "BUNNY"]


def test_multi_arg_endpoint_tableau():
    data = make_data("/paste", [["big", "small", "fluffy"], ["dog", "cat", "bunny"]])
    response = client.post("/evaluate", data=data)
    assert response.status_code == 200, response.json() == [
        "big dog",
        "small cat",
        "fluffy bunny",
    ]


def test_variadic_endpoint():
    data = make_data("/variadic", [["big", "small", "fluffy"], ["dog", "cat", "bunny"]])
    response = client.post("/evaluate", data=data)
    assert response.status_code == 200, (
        response.json()
        == "{'_arg1': ['big', 'small', 'fluffy'], '_arg2': ['dog', 'cat', 'bunny']}"
    )


@pytest.mark.parametrize(
    "path,content",
    [
        ("/", "Documentation for this API"),
        (
            "setup_tableau",
            "Configure Tableau to access extensions hosted on RStudio Connect",
        ),
        ("tableau_usage", "SCRIPT_STR(&#34;/capitalize&#34;, text)"),
    ],
)
def test_tableau_name_for_python_type2(path, content):
    response = client.get(path)
    assert response.status_code == 200
    assert content in response.text
