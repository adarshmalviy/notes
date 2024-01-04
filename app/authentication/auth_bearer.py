from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database.models import User
from app.authentication.auth import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            username = self.get_username_from_token(credentials.credentials)
            request.state.user_username = username  # Store username in request state
            request.state.user = await User.get(username=username)  # Store current user object in request state
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def get_username_from_token(self, jwtoken: str) -> str:
        try:
            payload = decode_jwt(jwtoken)
            username = payload.get("sub")
            return username
        except Exception as e:
            print("Error decoding token:", str(e))
            return None

    def verify_jwt(self, jwtoken: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = decode_jwt(jwtoken)
            # print("payloads",payload)
        except Exception as e:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
