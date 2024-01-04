from fastapi import Request
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def current_user(request: Request):
    user = request.state.user
    return user
