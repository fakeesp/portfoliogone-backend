from pydantic import BaseModel


class AuthorizationRequest(BaseModel):
    signature: str
    payload: str
