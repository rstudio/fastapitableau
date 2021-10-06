from unittest import TestCase

import pytest

from .main import app

capitalize_body_expected = ["foo", "bar"]
capitalize_body_tableau = {"script": "/capitalize", "data": {"_arg1": ["foo", "bar"]}}

paste_body_expected = {"first": ["A", "B", "C"], "second": ["D", "E", "F"]}
paste_body_tableau = {
    "script": "/paste",
    "data": {"_arg1": ["A", "B", "C"], "_arg2": ["D", "E", "F"]},
}


@pytest.mark.parametrize(
    "path,received_body,expected_body",
    [
        ("/capitalize", capitalize_body_expected, capitalize_body_expected),
        ("capitalize_pyd", capitalize_body_tableau, capitalize_body_expected),
        ("/paste", paste_body_expected, paste_body_expected),
        ("paste_pyd", paste_body_tableau, paste_body_expected),
    ],
)
async def test_ensure_request_body(path, received_body, expected_body):
    for route in app.routes:
        if route.path == path:
            break
    ensured_body = await route.ensure_request_body(received_body)
    TestCase().assertDictEqual(expected_body, ensured_body)
