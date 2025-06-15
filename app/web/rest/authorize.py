from typing import Annotated, Any, Final, Optional

import jwt
from eth_account import Account
from eth_account.messages import encode_defunct
from fastapi import APIRouter, Body

from app.models.http.requests.auth import AuthorizationRequest
from app.models.http.responses.string import StringResponse
from app.models.sql.user import User
from app.web.depends.rest.global_di import DI_AppConfig, DI_Repository

router: Final[APIRouter] = APIRouter()


@router.post(
    path="/authorize",
    description="You should send signature from YELLOW wallet and PAYLOAD",
)
async def authorization_handler(
    data: Annotated[AuthorizationRequest, Body()],
    app_config: DI_AppConfig,
    repository: DI_Repository,
) -> StringResponse:
    msg = encode_defunct(hexstr=data.payload)
    recovered_address: str = Account.recover_message(msg, signature=data.payload)

    user: Optional[User] = await repository.users.get(wallet=recovered_address)

    if user is None:
        user = User(wallet=recovered_address)
        await repository.uow.commit(user)

    payload: dict[str, Any] = {
        "wallet": recovered_address,
    }

    return StringResponse(
        data=jwt.encode(
            payload=payload,
            key=app_config.jwt.secret.get_secret_value(),
            algorithm=app_config.jwt.algorithm,
        ),
        message="Authorization successful",  # type: ignore[call-arg]
    )
