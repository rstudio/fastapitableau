import json

import pytest

from fastapitableau.middleware import TableauExtensionMiddleware


@pytest.mark.asyncio
async def test_rewrite_scope_path_does_not_mutate_original():
    """
    Regression test for #51: the middleware must not mutate the original
    ASGI scope dict. A shallow copy is made instead so that upstream middleware
    still sees the original path.
    """
    original_scope = {
        "type": "http",
        "path": "/evaluate",
        "raw_path": b"/evaluate",
        "headers": [],
    }
    body = json.dumps({"script": "/capitalize", "data": {"_arg1": ["hello"]}})

    async def mock_receive():
        return {"type": "http.request", "body": body.encode(), "more_body": False}

    new_scope, _ = await TableauExtensionMiddleware.rewrite_scope_path(
        original_scope, mock_receive
    )

    # The original scope must be unchanged
    assert original_scope["path"] == "/evaluate"
    assert original_scope["raw_path"] == b"/evaluate"

    # The new scope has the rewritten path
    assert new_scope["path"] == "/capitalize"
    assert new_scope["raw_path"] == b"/capitalize"

    # They are distinct dicts
    assert new_scope is not original_scope
