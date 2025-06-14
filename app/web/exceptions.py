from typing import Final, NamedTuple

from fastapi import Request, Response, status
from starlette.responses import JSONResponse

from app.exceptions.access import AccessError
from app.exceptions.base import NotFoundError
from app.models.http.responses.exceptions.access_error import AccessErrorResponse
from app.models.http.responses.exceptions.base import BaseExceptionResponse
from app.models.http.responses.exceptions.not_found import NotFoundResponse


class HTTPError(NamedTuple):
    status_code: int
    response_model: type[BaseExceptionResponse]


API_ERRORS: Final[dict[type[Exception], HTTPError]] = {
    AccessError: HTTPError(
        status_code=status.HTTP_403_FORBIDDEN,
        response_model=AccessErrorResponse,
    ),
    NotFoundError: HTTPError(
        status_code=status.HTTP_404_NOT_FOUND,
        response_model=NotFoundResponse,
    ),
}


# noinspection PyUnusedLocal
async def handle_error(_: Request, exc: Exception) -> Response:
    http_error: HTTPError = API_ERRORS[type(exc)]
    return JSONResponse(
        status_code=http_error.status_code,
        content={"detail": http_error.response_model(message=str(exc)).model_dump()},
    )
