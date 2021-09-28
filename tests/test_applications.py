from fastapi.testclient import TestClient

from .main import app

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
