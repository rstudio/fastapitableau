import json
from typing import Any, Callable, Dict, Optional

from fastapi import Request, Response
from fastapi.dependencies.utils import request_body_to_args
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_flat_models_from_routes
from fastapi.routing import APIRoute
from pydantic.error_wrappers import ErrorWrapper
from pydantic.schema import field_schema, get_model_name_map

from .utils import event_from_receive, remove_prefix, replace_dict_keys


class TableauRoute(APIRoute):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._body_schema: Optional[Dict[str, Any]] = None

    def get_body_field_schema(self):
        # schema, definitions, nested models
        route_flat_models = get_flat_models_from_routes([self])
        route_model_name_map = get_model_name_map(route_flat_models)
        body_field_schema = field_schema(
            self.body_field, model_name_map=route_model_name_map
        )
        return body_field_schema

    @property
    def body_schema(self):
        if not self._body_schema:
            f_schema, f_definitions, f_nested_models = self.get_body_field_schema()

            if "$ref" in f_schema.keys():
                ref = remove_prefix(f_schema["$ref"], "#/definitions/")
                definition = f_definitions[ref]
            else:
                definition = f_schema
        else:
            definition = self._body_schema
        return definition

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            _request = await self.rewrite_request_body(request)
            return await original_route_handler(_request)

        return custom_route_handler

    async def body_will_validate(self, received_body: Dict[str, Any]):
        """
        This function tries to process the request body using FastAPI's own function, and returns False if it fails to process. It's potentially expensive, but could be useful as a stricter heuristic for deciding whether to rewrite the request body.
        """
        values, errors = await request_body_to_args(
            self.dependant.body_params, received_body
        )
        return False if errors else True

    async def rewrite_request_body(self, request: Request) -> Request:  # noqa: C901
        # Consume entire message
        event = await event_from_receive(request.receive)
        try:
            received_body = json.loads(event["body"])
        except Exception as e:
            print("Failed to parse event body as JSON: {event}")
            print(e)
            raise e

        # Here, we only want to operate on Tableau requests. We have a few options.
        # 1. Duck typing, which is what the main branch does right now. It checks to see if this a dict and contains the keys "script" and "data".
        # 2. Validate. Try to process the body with FastAPI's args and see if it works. If it doesn't, try this method.
        # 3. Use headers.
        body_will_validate = await self.body_will_validate(received_body)
        if (
            not body_will_validate
            and isinstance(received_body, Dict)
            and set(received_body.keys()) == {"script", "data"}
        ):
            data = received_body["data"]

            body_type = self.body_schema["type"]

            if body_type == "array":

                if len(data) == 1:
                    _body = list(data.values())[0]

                else:
                    error = ValueError(
                        f"The endpoint {self.name} expects to receive a list, but received a {type(data)} from Tableau."
                    )
                    raise RequestValidationError([ErrorWrapper(error, "body")])

            elif body_type == "object":
                properties = self.body_schema["properties"]

                if len(properties) == len(data):
                    expected_names = list(properties.keys())
                    name_map: Dict[str, str] = {}
                    for i, new_name in enumerate(expected_names):
                        old_name = "_arg" + str(i + 1)
                        name_map[old_name] = new_name
                    _body = replace_dict_keys(data, name_map)
                else:
                    error = ValueError(
                        f"The route {self.name} expects {len(properties)} arguments, but received {len(data)} from Tableau."
                    )
                    raise RequestValidationError([ErrorWrapper(error, "body")])
            else:
                _body = data

            event["body"] = bytes(json.dumps(_body), encoding="utf-8")

        async def _receive():
            return event

        return Request(request.scope, _receive)
