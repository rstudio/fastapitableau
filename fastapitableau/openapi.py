from typing import Any, Dict, Optional, Type

from fastapi import params
from fastapi.dependencies.utils import (
    Dependant,
    check_file_field,
    get_flat_dependant,
    get_schema_compatible_field,
)
from fastapi.utils import create_response_field
from pydantic import BaseModel, create_model
from pydantic.fields import ModelField

# from fastapi.openapi.utils import *


def get_body_field(*, dependant: Dependant, name: str) -> Optional[ModelField]:
    flat_dependant = get_flat_dependant(dependant)  # noqa: F405
    if not flat_dependant.body_params:
        return None
    first_param = flat_dependant.body_params[0]
    field_info = first_param.field_info
    embed = getattr(field_info, "embed", None)
    body_param_names_set = {param.name for param in flat_dependant.body_params}
    if len(body_param_names_set) == 1 and not embed:
        final_field = get_schema_compatible_field(field=first_param)  # noqa: F405
        check_file_field(final_field)  # noqa: F405
        return final_field
    # If one field requires to embed, all have to be embedded
    # in case a sub-dependency is evaluated with a single unique body field
    # That is combined (embedded) with other body fields
    for param in flat_dependant.body_params:
        setattr(param.field_info, "embed", True)
    model_name = "Body_" + name
    BodyModel: Type[BaseModel] = create_model(model_name)
    for f in flat_dependant.body_params:
        BodyModel.__fields__[f.name] = get_schema_compatible_field(
            field=f
        )  # noqa: F405
    required = any(True for f in flat_dependant.body_params if f.required)

    BodyFieldInfo_kwargs: Dict[str, Any] = dict(default=None)
    if any(isinstance(f.field_info, params.File) for f in flat_dependant.body_params):
        BodyFieldInfo: Type[params.Body] = params.File
    elif any(isinstance(f.field_info, params.Form) for f in flat_dependant.body_params):
        BodyFieldInfo = params.Form
    else:
        BodyFieldInfo = params.Body

        body_param_media_types = [
            getattr(f.field_info, "media_type")
            for f in flat_dependant.body_params
            if isinstance(f.field_info, params.Body)
        ]
        if len(set(body_param_media_types)) == 1:
            BodyFieldInfo_kwargs["media_type"] = body_param_media_types[0]
    final_field = create_response_field(
        name="body",
        type_=BodyModel,
        required=required,
        alias="body",
        field_info=BodyFieldInfo(**BodyFieldInfo_kwargs),
    )
    check_file_field(final_field)
    return final_field
