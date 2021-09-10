from fastapitableau import rstudio_connect
import os

def test_check_rstudio_connect():
    # These tests aren't run in a Connect environment.
    assert rstudio_connect.check_rstudio_connect() is False

    indicators = {
        "RSTUDIO_PRODUCT": "CONNECT",
        "RSTUDIO_CONNECT_HASTE": "set",
        "R_SESSION_TMPDIR": "/opt/rstudio-connect/mnt/tmp",
    }

    # We'll test three different indicators.
    for k, v in indicators.items():
        os.environ[k] = v
        assert rstudio_connect.check_rstudio_connect() is True
        os.environ.pop(k)
