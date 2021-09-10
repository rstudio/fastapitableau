from os import environ, getcwd
from re import match
import requests


def check_rstudio_connect():
    """Returns True if running in RStudio Connect"""
    checks = [
        # This first check is only valid for recent versions.
        environ.get("RSTUDIO_PRODUCT") == "CONNECT",
        "RSTUDIO_CONNECT_HASTE" in environ.keys(),
        getcwd() == "/opt/rstudio-connect/mnt/app",
        environ.get("LOGNAME") == "rstudio-connect",
        environ.get("R_CONFIG_ACTIVE") == "rsconnect",
        environ.get("TMPDIR") == "/opt/rstudio-connect/mnt/tmp",
        match(r"^/opt/rstudio-connect/mnt/tmp", str(environ.get("R_SESSION_TMPDIR"))),
    ]
    return any(checks)


def warning_message():
    # Check Connect. Return None if none


    connect_server = environ.get("CONNECT_SERVER")
    # DEBUG: Print CONNECT_SERVER variable

    if connect_server is None:
        print("Debug message about CONNECT_SERVER not set")
        pass
        # DEBUG: Add a message if CONNECT_SERVER not defined
        # MESSAGE: CONNECT_SERVER not defined error message


    # We won't do that here cos it's a plumber thing
    # Parse server to get scheme
    # If scheme is None:
        # DEBUG: If server doesn't specify https:// or http://
        # MESSAGE: CONNECT_SERVER does not specify protocol


    connect_api_key = environ.get("CONNECT_API_KEY")
    # DEBUG: Print API key variable

    if connect_server is None:
        print("Debug message about CONNECT_SERVER not set")
        pass
        # DEBUG: Add a message if API key not defined
        # MESSAGE: API key not defined error message


    # https checking (probably don't need to do)


    # call API to see if thing is enabled.
    settings_url = connect_server + "__api__/server_settings"

    headers = {
        "Authorization": "Key " + connect_api_key
    }

    response = requests.get(settings_url, headers=headers)

    """
    If there's an error, we print an error message.
    DEBUG: We print a message with the status, reason, and message.
    """

    """
    Parse settings.

    If the tableau_integration_enabled key is not present:
        Send a message about now it's not present.
        Include server_settings.version and suggest upgrade.
    If it's false:
        Send a message about it being disabled
