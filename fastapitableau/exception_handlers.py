from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY


async def tableau_http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    headers = getattr(exc, "headers", None)
    if headers:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": f"Server Error: {type(exc).__name__}",
                "info": str(exc.detail),
            },
            headers=headers,
        )
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": f"Server Error: {type(exc).__name__}",
                "info": str(exc.detail),
            },
        )


async def tableau_request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": f"Server Error: {type(exc).__name__}",
            "info": str(exc),
        },
    )


async def tableau_general_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "message": f"Server Error: {type(exc).__name__}",
            "info": str(exc),
        },
    )
