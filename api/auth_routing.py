from fastapi.routing import APIRouter
from settings.auth import (
    verified_user,
    authorize,
    pwd_context,
    create_access_jwt,
    create_refresh_jwt,
)
from models.user_model import User
from schemas.user_schema import UserPost, UserGet, UserLogin
from fastapi import Depends, HTTPException, status

auth_router = APIRouter(prefix="/api/v1", tags=["Auth"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(body: UserPost):
    password_hashed = pwd_context.hash(body.password_hash)
    # turn payload into dict
    data = body.model_dump(by_alias=True, exclude_unset=True)
    data['password_hash'] = password_hashed
    # Check if email already exists
    existing = await User.filter(email=body.email).exists()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists"
        )
    # Create user
    user_obj = await User.create(**data)
    # Return created user
    user = await UserGet.from_tortoise_orm(user_obj)
    # get the created user.id
    user_id = user.model_dump()["id"]
    return {"message": "User created successfully", "user": user, "user_id": user_id}


@auth_router.post("/login")
async def login_user(body: UserLogin):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )
    # check if user exists
    user = await User.filter(email=body.email).first()
    if not user:
        raise error
    # check if password is correct
    matches = pwd_context.verify(body.password, user.password_hash)
    if not matches:
        raise error
    # create jwt access token
    data = {"user_name": user.email}
    access_token = create_access_jwt(data)
    # create jwt refresh token
    refresh_token = create_refresh_jwt(data)
    # store the refresh token in the database.In this project,it's stored in the user table
    await User.filter(email=body.email).update(**({"refresh_token": refresh_token}))
    return {
        "message": "Login successful",
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@auth_router.post("/refresh_token")
async def refresh_token(token_data: dict = Depends(authorize)):
    return token_data


@auth_router.get("/user_data")
async def protected_data(user: User = Depends(verified_user)):
    return {
        "status": "authorized",
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
