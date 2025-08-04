from fastapi import Header, HTTPException, status
from typing import Annotated
from config.settings import settings

GLOBAL_TOKEN = settings.global_token


async def verify_token(authorization: Annotated[str | None, Header()] = None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Missing or invalid Authorization header")

    token = authorization.split(" ")[1]
    if token != GLOBAL_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return token
