import secrets
import string

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from tortoise.transactions import in_transaction

from app.database.models import User
from app.authentication.auth import create_access_token, create_refresh_token, decode_jwt, get_password_hash, sign_jwt, \
    verify_password
from app.authentication.auth_bearer import JWTBearer
from app.authentication.dependencies import current_user
from app.schemas.user import UserCreate, UserLogin

router = APIRouter()

@router.get("/user", dependencies=[Depends(JWTBearer())])
async def current_user(request: Request, user: User = Depends(current_user)):
    try:
        user_details={
            "first_name":user.first_name,
            "last_name":user.last_name,
            "username":user.username,
            "created_at":user.created_at,
            "updated_at":user.updated_at,
        }
        
        return {"message": "success", "user": user_details}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/signup")
async def sign_up(user_data: UserCreate):
    try:
        # Check if the user with the same username already exists
        user_exists = await User.filter(username=user_data.username).first()
        if user_exists:
            raise HTTPException(status_code=400, detail="User with this username already exists")

        # Create the user
        user = await User.create(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            password=get_password_hash(user_data.password),
        )

        return {"message": "success"}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


# User login API
@router.post("/login")
async def login(user_data: UserLogin):
    try:
        user = await User.get_or_none(username=user_data.username)
        if not user or not verify_password(user_data.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        # Create an access token
        access_token = create_access_token(user_data.username)
        refresh_token = create_refresh_token(user_data.username)
        
        return {"message": "success", "access_token": access_token, "token_type": "bearer",
                "refresh_token": refresh_token}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
