import os

from fastapitableau import rstudio_connect


def test_check_rstudio_connect():
    # These tests aren't run in a Connect environment.
    assert rstudio_connect.check_rstudio_connect() is False

    indicators = {
        "RSTUDIO_PRODUCT": "CONNECT",
    }

    # We'll test the one indicator.
    for k, v in indicators.items():
        os.environ[k] = v
        assert rstudio_connect.check_rstudio_connect() is True
        os.environ.pop(k)
