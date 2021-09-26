# https://github.com/tiangolo/fastapi/blob/7b6e198d314e320256c2ed8b62430b2a42c31cb5/fastapi/openapi/utils.py#L387

from typing import Any, Dict

from fastapi.openapi.utils import (
    get_flat_models_from_routes,
    get_model_definitions,
    get_openapi,
)
from pydantic import BaseModel
from pydantic.fields import ModelField
from pydantic.schema import (
    field_schema,
    get_flat_models_from_fields,
    get_model_name_map,
)

from fastapitableau.routing import TableauRoute
from fastapitableau.utils import replace_dict_keys

# def get_tableau_models(routes):
#     flat_models = get_flat_models_from_routes(routes)
#     model_name_map = get_model_name_map(flat_models)
#     definitions = get_model_definitions(
#         flat_models=flat_models, model_name_map=model_name_map
#     )
#     for route in routes:
#         if isinstance(route, routing.APIRoute):
#             result = get_openapi_path(route=route, model_name_map=model_name_map)
#             if result:
#                 path, security_schemes, path_definitions = result
#                 if path:
#                     paths.setdefault(route.path_format, {}).update(path)
#                 if security_schemes:
#                     components.setdefault("securitySchemes", {}).update(
#                         security_schemes
#                     )
#                 if path_definitions:
#                     definitions.update(path_definitions)
#     if definitions:
#         components["schemas"] = {k: definitions[k] for k in sorted(definitions)}
#     if components:
#         output["components"] = components
#     output["paths"] = paths


routes = app.routes


for route in routes:
    print(dir(route))


openapi = app.openapi()

print(openapi)

tableau_request_structure = {"script": ""}


schema = openapi["components"]["schemas"]["Body_paste_paste_post"]

# Generate a list of the expected Tableau labels. If it is in `required`, relabel it there, and add it to the list of new keys.
new_keys = []
for i, key in enumerate(schema["properties"].keys()):
    new_key_name = "_arg" + str(i + 1)
    new_keys.append(new_key_name)
    schema["required"] = [x if x != key else new_key_name for x in schema["required"]]
schema["properties"] = replace_dict_keys(schema["properties"], new_keys)


output: Dict[str, Any] = {}
components: Dict[str, Dict[str, Any]] = {}
paths: Dict[str, Dict[str, Any]] = {}
flat_models = get_flat_models_from_routes(routes)
model_name_map = get_model_name_map(flat_models)
definitions = get_model_definitions(
    flat_models=flat_models, model_name_map=model_name_map
)
for route in routes:
    if isinstance(route, TableauRoute):
        result = get_openapi_path(route=route, model_name_map=model_name_map)
        print(result)
        if result:
            path, security_schemes, path_definitions = result
            if path:
                paths.setdefault(route.path_format, {}).update(path)
            if security_schemes:
                components.setdefault("securitySchemes", {}).update(security_schemes)
            if path_definitions:
                definitions.update(path_definitions)
if definitions:
    components["schemas"] = {k: definitions[k] for k in sorted(definitions)}
if components:
    output["components"] = components
output["paths"] = paths
if tags:
    output["tags"] = tags
return jsonable_encoder(OpenAPI(**output), by_alias=True, exclude_none=True)  # type: ignore
