import logging

import pytest  # noqa: F401
from fastapi.testclient import TestClient

from .main import app, make_data


def test_evaluate_request_logs_with_correlation_id(caplog):
    caplog.set_level(logging.DEBUG, logger="fastapitableau")
    client = TestClient(app)

    cid = "02224a4a-9f85-4c10-9223-c5bc92258882"
    data = make_data("/paste", [["big", "small", "fluffy"], ["dog", "cat", "bunny"]])
    client.post("/evaluate", headers={"x-correlation-id": cid}, data=data)
    assert cid in caplog.text
    assert "Rewriting" in caplog.text


def test_no_logging(caplog):
    caplog.set_level(logging.WARNING, logger="fastapitableau")
    client = TestClient(app)

    cid = "02224a4a-9f85-4c10-9223-c5bc92258882"
    data = make_data("/paste", [["big", "small", "fluffy"], ["dog", "cat", "bunny"]])
    client.post("/evaluate", headers={"x-correlation-id": cid}, data=data)
    assert cid not in caplog.text
    assert "Rewriting" not in caplog.text
