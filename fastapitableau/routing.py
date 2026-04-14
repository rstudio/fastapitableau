import json
from typing import Any, Callable, Dict, MutableMapping, Optional

from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from pydantic import TypeAdapter, ValidationError

from fastapitableau.logger import logger
from fastapitableau.utils import event_from_receive, replace_dict_keys


class TableauRoute(APIRoute):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._body_schema: Optional[Dict[str, Any]] = None
        self._body_type_adapter: Optional[TypeAdapter] = None
        if self.body_field is not None:
            if hasattr(self.body_field, "_type_adapter"):
                self._body_type_adapter = self.body_field._type_adapter
            else:
                self._body_type_adapter = TypeAdapter(self.body_field.type_)

    def get_body_field_schema(self):
        if self._body_type_adapter is None:
            return {}, {}
        schema = self._body_type_adapter.json_schema()
        definitions = schema.pop("$defs", {})
        return schema, definitions

    @property
    def body_schema(self):
        if not self._body_schema:
            f_schema, f_definitions = self.get_body_field_schema()

            if "$ref" in f_schema:
                ref = f_schema["$ref"].removeprefix("#/$defs/")
                definition = f_definitions[ref]
            else:
                definition = f_schema
        else:
            definition = self._body_schema
        return definition

    #
    def get_route_handler(self) -> Callable:
        """
        Override the base route handler to rewrite the body of tableau requests
        into the shape FastAPI routes expect.
        """
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            event = await event_from_receive(request.receive)
            try:
                body = json.loads(event["body"])
            except Exception as e:
                logger.warning(
                    "Failed to parse event body as JSON: %s",
                    event["body"],
                    extra={"scope": request.scope},
                )
                raise e

            _body = await self.ensure_request_body(body, scope=request.scope)
            event["body"] = bytes(json.dumps(_body), encoding="utf-8")

            async def _receive():
                return event

            _request = Request(request.scope, _receive)

            return await original_route_handler(_request)

        return custom_route_handler

    async def ensure_request_body(
        self, body: Dict, scope: Optional[MutableMapping] = None
    ) -> Dict:
        """
        Rewrites requests that look like they come from Tableau into ordinary
        requests. Leave other requests unchanged.
        """
        body_will_validate = self.body_will_validate(body)
        if body_will_validate:
            _body = body
            logger.debug(
                "Not rewriting body for request to '%s': %s",
                self.path,
                _body,
                extra={"scope": scope},
            )
        elif isinstance(body, Dict) and set(body.keys()) == {"script", "data"}:
            # It looks like a Tableau request.
            data = body["data"]
            if self.body_schema["type"] == "array":
                # If sent a single array, we raise it up a level to serve as the entire request body.
                if len(data) == 1:
                    _body = list(data.values())[0]
                else:
                    error = ValueError(
                        f"The endpoint {self.name} expects to receive a list, but received a {type(data)} from Tableau."
                    )
                    raise RequestValidationError([error])

            elif self.body_schema["type"] == "object":
                # Rename Tableau _arg[n] arguments to the argument names we expect.
                # Order based on argument numbering from Tableau.
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
                    raise RequestValidationError([error])
            logger.debug(
                "Rewriting body for Tableau request to '%s': %s",
                self.path,
                _body,
                extra={"scope": scope},
            )
        return _body

    def body_will_validate(self, body: Any) -> bool:
        """
        Check whether the body will pass validation against the route's expected
        type. Returns True if valid (no rewriting needed), False otherwise.
        """
        if self._body_type_adapter is None:
            return True
        try:
            self._body_type_adapter.validate_python(body)
            return True
        except ValidationError:
            return False
