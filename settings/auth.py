from passlib.context import CryptContext
from jose import jwt
from datetime import datetime
from settings.configuration import Config
from fastapi import Depends, HTTPException, status
from jose.exceptions import JWTError
from fastapi.security import OAuth2PasswordBearer
from models.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization credentials"
)


def create_access_jwt(data: dict):
    data["exp"] = datetime.now() + Config.JWT_ACCESS_EXP
    data["mode"] = "access_token"
    return jwt.encode(data, Config.SECRET_KEY, algorithm=Config.ALGORITHM)


def create_refresh_jwt(data: dict):
    data["exp"] = datetime.now() + Config.JWT_REFRESH_EXP
    data["mode"] = "refresh_token"
    return jwt.encode(data, Config.SECRET_KEY, algorithm=Config.ALGORITHM)


async def authorize(token: str = Depends(oauth_scheme)) -> dict:
    # validate the refresh jwt token
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        # check if "mode":"refresh_token" is in the token payload
        if "user_name" not in data or data["mode"] != "refresh_token":
            raise error
        # check if user exists
        user = await User.filter(email=data["user_name"]).first()
        if not user or user.refresh_token != token:
            raise error
        # generate new refresh token and update user
        data = {"user_name": user.email}
        refresh_token = create_refresh_jwt(data)
        await User.filter(email=user.email).update(**({"refresh_token": refresh_token}))
        # generate new access token
        access_token = create_access_jwt(data)
        return {"access_token": access_token, "refresh_token": refresh_token}
    except JWTError:
        raise error


async def verified_user(token: str = Depends(oauth_scheme)) -> dict:
    # validate the access jwt token
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        # check if "mode":"refresh_token" is in the token payload
        if "user_name" not in data or data["mode"] != "access_token":
            raise error
        # check if user exists
        user = await User.filter(email=data["user_name"]).first()
        if not user:
            raise error
        return {"user_id": user.id, "email": user.email}
    except JWTError:
        raise error
