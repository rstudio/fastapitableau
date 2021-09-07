from copy import deepcopy
from typing import Dict, List, Optional

from fastapitableau.utils import replace_dict_keys


def rewrite_tableau_openapi(
    openapi: Dict, rewrite_paths: Optional[List[str]] = None
) -> Dict:
    openapi = deepcopy(openapi)
    schemas = openapi["components"]["schemas"]

    if rewrite_paths is None:
        rewrite_paths = list(openapi["paths"].keys())

    for path_name in rewrite_paths:
        print("Rewriting " + path_name)

        path = openapi["paths"][path_name]
        path_schema = path["post"]["requestBody"]["content"]["application/json"][
            "schema"
        ]

        if "$ref" not in path_schema.keys():
            # Do some moving around of elements to make the single field appear as a referenced schema

            schema_name = "Body_" + path["post"]["operationId"]
            schema_ref = "#/components/schemas/" + schema_name

            # schema = openapi["components"]["schemas"][schema_name]
            lowercase_title = path_schema["title"].lower()

            schema = {
                "title": schema_name,
                "required": [lowercase_title],
                "type": "object",
                "properties": {lowercase_title: path_schema},
            }

            # Replace components with newly created reference schema
            path["post"]["requestBody"]["content"]["application/json"]["schema"] = {
                "$ref": schema_ref
            }
            openapi["components"]["schemas"][schema_name] = schema

            # Overwrite the path_schema object with the new ref
            path_schema = path["post"]["requestBody"]["content"]["application/json"][
                "schema"
            ]

        schema_ref = path_schema["$ref"]
        schema_name = schema_ref.split("/")[-1]

        tab_schema_name = schema_name + "_tableau"
        tab_schema_ref = schema_ref + "_tableau"

        schema = openapi["components"]["schemas"][schema_name]

        # Generate a list of the expected Tableau labels. If it is in `required`, relabel it there, and add it to the list of new keys.
        new_keys = []
        for i, key in enumerate(schema["properties"].keys()):
            new_key_name = "arg" + str(i + 1) + "_"
            new_keys.append(new_key_name)
            schema["required"] = [
                x if x != key else new_key_name for x in schema["required"]
            ]
        schema["properties"] = replace_dict_keys(schema["properties"], new_keys)

        tab_schema = {
            "title": tab_schema_name,
            "required": ["script", "data"],
            "type": "object",
            "properties": {
                "script": {"title": "Script", "type": "string", "default": path_name},
                "data": {"$ref": schema_ref},
            },
        }

        # Insert the tableau request schema into schemas and change the path schema ref to point to it.
        schemas[tab_schema_name] = tab_schema
        path_schema["$ref"] = tab_schema_ref

    return openapi
