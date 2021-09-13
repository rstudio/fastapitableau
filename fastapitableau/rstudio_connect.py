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
    """
    Generate a string of warning messages based on information gathered about our environment in RStudio Connect.
    """
    if not check_rstudio_connect():
        return None

    connect_server = environ.get("CONNECT_SERVER")
    # TODO DEBUG: Print CONNECT_SERVER variable

    if connect_server is None:
        print("Debug message about CONNECT_SERVER not set")
        pass
        # TODO DEBUG: Add a message if CONNECT_SERVER not defined
        # TODO MESSAGE: CONNECT_SERVER not defined error message

    # TODO: We won't do that here cos it's a plumber thing??
    # Parse server to get scheme
    # If scheme is None:
    # DEBUG: If server doesn't specify https:// or http://
    # MESSAGE: CONNECT_SERVER does not specify protocol

    connect_api_key = environ.get("CONNECT_API_KEY")
    # TODO
    # DEBUG: Print API key variable

    if connect_server is None:
        print("Debug message about CONNECT_SERVER not set")
        pass
        # TODO
        # DEBUG: Add a message if API key not defined
        # MESSAGE: API key not defined error message

    # TODO https checking (probably don't need to do)

    # call API to see if thing is enabled.
    settings_url = connect_server + "__api__/server_settings"

    headers = {"Authorization": "Key " + connect_api_key}

    response = requests.get(settings_url, headers=headers, verify=False)

    if response.status_code != 200:
        print("Bad status code")
        # TODO: Message about how we can't get status

    else:
        server_settings = response.json()
        if "tableau_integration_enabled" not in server_settings.keys():
            print(
                f"Tableau.IntegrationEnabled is not present within server settings. This Connect server does not support the feature ({server_settings['version']})"
            )
            # TODO: Debug, message.

        elif server_settings["tableau_integration_enabled"] is False:
            print("Tableau integration is disabled")
            # TODO: Message about how setting is disabled.


messages = {
    "connect_server_not_defined": """
### The environment variable *CONNECT_SERVER* is not defined

Possible Solutions:

- Have your system administrator confirm *Applications.DefaultServerEnv* is enabled and that *Server.Address* has been defined within the *rstudio-connect.gcfg* file on the RStudio Connect server.",
- Use the application settings for your content within the RStudio Connect dashboard to define the *CONNECT_SERVER* environment variable. It should be set to a reachable https or http address for the server.""",
    "protocol_not_specified": f"""
### Environment Variable `CONNECT_SERVER` (value = `{environ.get("CONNECT_SERVER")}` ) does not specify the protocol (`https://` or `http://`)

Possible Solutions:

- Have your system administrator confirm that `Server.Address` has been configured with the proper format within the `rstudio-connect.gcfg` file on the RStudio Connect server.
- Use the application settings for your content within the RStudio Connect dashboard to define the CONNECT_SERVER` environment variable with the proper protocol.""",
    "connect_api_key_not_defined": """
### The environment variable `CONNECT_API_KEY` is not defined

Possible Solutions:

- Have your administrator enable the `Applications.DefaultAPIKeyEnv` setting within the `rstudio-connect.gcfg` file on the RStudio Connect server.
- Create an API key yourself and use the application settings for your content within the RStudio Connect dashboard to set the the `CONNECT_API_KEY` variable to its value.
""",
    "server_responded_with_error": f"""
### API request to {environ.get("CONNECT_SERVER")} has failed with error:"

Possible Solutions:

- If you have specified an API_KEY, confirm it is valid.
- Confirm the server can be reached at {environ.get("CONNECT_SERVER")}.
- TODO: Message about enabling self-signed certificates.
- TODO: There are two error messages in here. One on line 137.
""",
    "tableau_feature_not_available": """
### Tableau Integration Feature Flag is not available on the RStudio Connect server. Current server is version: TODO rework

Possible Solution:

- Please upgrade to the latest version of RStudio Connect.
""",
    "tableau_integration_disabled": """
Tableau Integration has been disabled on the RStudio Connect server

Possible Solution:

- Please ask your administrator to set `Tableau.TableauIntegrationEnabled` = `true` within `rstudio-connect.gcfg` file on the RStudio Connect server.
""",
}
