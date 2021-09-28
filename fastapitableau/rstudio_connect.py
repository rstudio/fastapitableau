from os import environ, getcwd
from typing import List, Optional
from urllib.parse import urlparse

import requests


def check_rstudio_connect() -> bool:
    """Returns True if running in RStudio Connect"""
    checks = [
        # The first check is only valid for recent versions.
        environ.get("RSTUDIO_PRODUCT") == "CONNECT",
        # We still perform checks for evidence we're running on older Connect versions so we can show warning messages about upgrading.
        "RSTUDIO_CONNECT_HASTE" in environ.keys(),
        getcwd() == "/opt/rstudio-connect/mnt/app",
        environ.get("LOGNAME") == "rstudio-connect",
        environ.get("TMPDIR") == "/opt/rstudio-connect/mnt/tmp",
    ]
    return any(checks)


def warning_message() -> Optional[str]:  # noqa: C901
    """
    Generate a string of warning messages based on information gathered about our environment in RStudio Connect.
    """
    if not check_rstudio_connect():
        return None

    message_list: List[str] = []

    connect_server = environ.get("CONNECT_SERVER")

    if connect_server is None:
        message_list.append(
            "\n### The environment variable `CONNECT_SERVER` is not defined\n"
            "\n"
            "Possible Solutions:\n"
            "\n"
            "- Have your system administrator confirm `Applications.DefaultServerEnv` is enabled and that `Server.Address` has been defined within the `rstudio-connect.gcfg` file on the RStudio Connect server.,\n"
            "- Use the application settings for your content within the RStudio Connect dashboard to define the `CONNECT_SERVER` environment variable. It should be set to a reachable https or http address for the server.\n"
        )

    if urlparse(connect_server).scheme is None:
        message_list.append(
            f"### Environment Variable `CONNECT_SERVER` (value = `{connect_server}` ) does not specify the protocol (`https://` or `http://`)\n"
            "\n"
            "Possible Solutions:\n"
            "\n"
            "- Have your system administrator confirm that `Server.Address` has been configured with the proper format within the `rstudio-connect.gcfg` file on the RStudio Connect server.\n"
            "- Use the application settings for your content within the RStudio Connect dashboard to define the CONNECT_SERVER` environment variable with the proper protocol.\n"
        )

    connect_api_key = environ.get("CONNECT_API_KEY")

    if connect_api_key is None:
        message_list.append(
            "### The environment variable `CONNECT_API_KEY` is not defined\n"
            "\n"
            "Possible Solutions:\n"
            "\n"
            "- Have your administrator enable the `Applications.DefaultAPIKeyEnv` setting within the `rstudio-connect.gcfg` file on the RStudio Connect server.\n"
            "- Create an API key yourself and use the application settings for your content within the RStudio Connect dashboard to set the the `CONNECT_API_KEY` variable to its value.\n"
        )

    if len(message_list) != 0:
        messages = "\n\n---\n\n".join(message_list)
        return messages

    # Call RStudio Connect API to get server settings
    settings_url = str(connect_server) + "__api__/server_settings"

    headers = {"Authorization": "Key " + str(connect_api_key)}

    try:
        response = requests.get(settings_url, headers=headers, verify=False)
    except Exception as e:
        message_list.append(
            f"### API request to {connect_server} has failed with error:\n"
            f"{e}"
            "\n"
            "\nPossible Solutions:"
            "\n"
            "\n- If you have specified an API key, confirm it is valid."
            "\n- Confirm there is connectivity between the server itself and the address assigned to it: "
            f"{connect_server}"
            "."
            "\n- If using HTTPS along with self-signed certificates, you may need to allow the FastAPITableau package to use HTTP instead, by setting the environment variable `FASTAPITABLEAU_USE_HTTP` to `True` in the RStudio Connect application settings."
        )

    if response.status_code != 200:
        message_list.append(
            f"### API request to {connect_server} has failed with error: {response.text}\n"
            "\n"
            "Possible Solutions:\n"
            "\n"
            "- If you have specified an API_KEY, confirm it is valid.\n"
            f"- Confirm the server can be reached at {connect_server}.\n"
        )

    else:
        server_settings = response.json()
        if "tableau_integration_enabled" not in server_settings.keys():
            message_list.append(
                "### Tableau Integration Feature Flag is not available on the RStudio Connect server.\n"
                "\n"
                "Possible Solution:\n"
                "\n"
                "- Please upgrade to the latest version of RStudio Connect.\n"
            )
        elif server_settings["tableau_integration_enabled"] is False:
            message_list.append(
                "Tableau Integration has been disabled on the RStudio Connect server\n"
                "\n"
                "Possible Solution:\n"
                "\n"
                "- Please ask your administrator to set `TableauIntegration.Enabled` = `true` within `rstudio-connect.gcfg` file on the RStudio Connect server.\n"
            )

    if len(message_list) != 0:
        print(message_list)
        messages = "\n\n---\n\n".join(message_list)
        return messages
    else:
        return None
