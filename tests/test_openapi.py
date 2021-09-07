import pytest

from fastapitableau.openapi import rewrite_tableau_openapi


@pytest.fixture
def openapi_schema():
    return {
        "openapi": "3.0.2",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/capitalize": {
                "post": {
                    "summary": "Capitalize",
                    "operationId": "capitalize_capitalize_post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Text",
                                    "type": "array",
                                    "items": {"type": "string"},
                                }
                            }
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        },
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                    },
                }
            },
            "/paste": {
                "post": {
                    "summary": "Paste",
                    "operationId": "paste_paste_post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_paste_paste_post"
                                }
                            }
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        },
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "Body_paste_paste_post": {
                    "title": "Body_paste_paste_post",
                    "required": ["first", "second"],
                    "type": "object",
                    "properties": {
                        "first": {
                            "title": "First",
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "second": {
                            "title": "Second",
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                },
                "HTTPValidationError": {
                    "title": "HTTPValidationError",
                    "type": "object",
                    "properties": {
                        "detail": {
                            "title": "Detail",
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                        }
                    },
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "loc": {
                            "title": "Location",
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "msg": {"title": "Message", "type": "string"},
                        "type": {"title": "Error Type", "type": "string"},
                    },
                },
            }
        },
    }


@pytest.fixture
def tableau_openapi_schema():
    return {
        "openapi": "3.0.2",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/capitalize": {
                "post": {
                    "summary": "Capitalize",
                    "operationId": "capitalize_capitalize_post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_capitalize_capitalize_post_tableau"
                                }
                            }
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        },
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                    },
                }
            },
            "/paste": {
                "post": {
                    "summary": "Paste",
                    "operationId": "paste_paste_post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Body_paste_paste_post_tableau"
                                }
                            }
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        },
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "Body_paste_paste_post": {
                    "title": "Body_paste_paste_post",
                    "required": ["arg1_", "arg2_"],
                    "type": "object",
                    "properties": {
                        "arg1_": {
                            "title": "First",
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "arg2_": {
                            "title": "Second",
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                },
                "HTTPValidationError": {
                    "title": "HTTPValidationError",
                    "type": "object",
                    "properties": {
                        "detail": {
                            "title": "Detail",
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                        }
                    },
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "loc": {
                            "title": "Location",
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "msg": {"title": "Message", "type": "string"},
                        "type": {"title": "Error Type", "type": "string"},
                    },
                },
                "Body_capitalize_capitalize_post": {
                    "title": "Body_capitalize_capitalize_post",
                    "required": ["arg1_"],
                    "type": "object",
                    "properties": {
                        "arg1_": {
                            "title": "Text",
                            "type": "array",
                            "items": {"type": "string"},
                        }
                    },
                },
                "Body_capitalize_capitalize_post_tableau": {
                    "title": "Body_capitalize_capitalize_post_tableau",
                    "required": ["script", "data"],
                    "type": "object",
                    "properties": {
                        "script": {
                            "title": "Script",
                            "type": "string",
                            "default": "/capitalize",
                        },
                        "data": {
                            "$ref": "#/components/schemas/Body_capitalize_capitalize_post"
                        },
                    },
                },
                "Body_paste_paste_post_tableau": {
                    "title": "Body_paste_paste_post_tableau",
                    "required": ["script", "data"],
                    "type": "object",
                    "properties": {
                        "script": {
                            "title": "Script",
                            "type": "string",
                            "default": "/paste",
                        },
                        "data": {"$ref": "#/components/schemas/Body_paste_paste_post"},
                    },
                },
            }
        },
    }


def test_rewrite_all_paths(openapi_schema, tableau_openapi_schema):
    rewritten_schema = rewrite_tableau_openapi(openapi_schema)
    assert rewritten_schema == tableau_openapi_schema


def test_rewrite_single_path(openapi_schema, tableau_openapi_schema):
    # Test rewriting /capitalize
    rewritten_capitalize = rewrite_tableau_openapi(openapi_schema, ["/capitalize"])

    # Assert that /capitalize has been rewritten
    assert (
        rewritten_capitalize["paths"]["/capitalize"]
        == tableau_openapi_schema["paths"]["/capitalize"]
    )
    assert (
        "Body_capitalize_capitalize_post_tableau"
        in rewritten_capitalize["components"]["schemas"].keys()
    )
    for component in [
        "Body_capitalize_capitalize_post_tableau",
        "Body_capitalize_capitalize_post",
    ]:
        assert (
            rewritten_capitalize["components"]["schemas"][component]
            == tableau_openapi_schema["components"]["schemas"][component]
        )

    # Assert that /paste has not been rewritten
    assert rewritten_capitalize["paths"]["/paste"] == openapi_schema["paths"]["/paste"]
    assert (
        "Body_paste_paste_post_tableau"
        not in rewritten_capitalize["components"]["schemas"].keys()
    )
    assert (
        rewritten_capitalize["components"]["schemas"]["Body_paste_paste_post"]
        == openapi_schema["components"]["schemas"]["Body_paste_paste_post"]
    )

    # Test rewriting /paste
    rewritten_paste = rewrite_tableau_openapi(openapi_schema, ["/paste"])

    print(rewritten_paste)

    # Assert that /capitalize has not been rewritten
    assert (
        rewritten_paste["paths"]["/capitalize"]
        == openapi_schema["paths"]["/capitalize"]
    )
    # In this case, neither component will be in the "schemas" property.
    for component in [
        "Body_capitalize_capitalize_post_tableau",
        "Body_capitalize_capitalize_post",
    ]:
        assert component not in rewritten_paste["components"]["schemas"].keys()

    # Assert that /paste has been rewritten
    assert (
        rewritten_paste["paths"]["/paste"] == tableau_openapi_schema["paths"]["/paste"]
    )
    assert (
        "Body_paste_paste_post_tableau"
        in rewritten_paste["components"]["schemas"].keys()
    )
    for component in ["Body_paste_paste_post_tableau", "Body_paste_paste_post"]:
        assert (
            rewritten_paste["components"]["schemas"][component]
            == tableau_openapi_schema["components"]["schemas"][component]
        )
