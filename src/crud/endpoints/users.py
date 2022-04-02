from fastapi import FastAPI, Body, HTTPException, status, APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from ...db.connection import user_collection
from ...serializers.user_schema import users_serializer
from ...crud.helpers.user_helper import create_user, check_free_username_and_email, get_user_by_email, get_films_already_seen_by_user, get_current_user
from ...security.security import create_access_token, JWTBearer, ACCESS_TOKEN_EXPIRE_MINUTES
from ...models.user_model import UserInCreate, UserInResponse, UserToken, UserInLogin, UserBase
from datetime import timedelta

router = APIRouter(
    prefix="/users",
)

@router.get("/", tags=["user"],)
async def users():
    users = user_collection.find({})
    return users_serializer(users)

@router.get("/whoami", tags=["user"], dependencies=[Depends(get_current_user)])
async def whoami(current_user: UserBase = Depends(get_current_user)):
    return current_user 

@router.post("/login", 
response_model=UserInResponse, 
tags=["authentication"],)
async def login(user: OAuth2PasswordRequestForm = Depends(UserInLogin)):

    usr = await get_user_by_email(user.email)

    if not usr or not usr.check_password(user.password):
        raise HTTPException(
            status_code=400, detail=" email ou password incorrecte"
        )

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    token = await create_access_token(data={"username": usr.username, "email": usr.email,"already_seen": usr.already_seen}, expires_delta=access_token_expires)

    token = jsonable_encoder(token)
    content = {"username":usr.username,"email":usr.email,"token":token,"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="Lax",
        secure=False,
    )

    # return UserInResponse(user=UserToken(**usr.dict(), token=token))
    return response


@router.post("/sign_up",
    response_model=UserInResponse,
    tags=["authentication"],
    status_code=HTTP_201_CREATED,
)
async def sign_up(user: OAuth2PasswordRequestForm = Depends(UserInCreate)):
    
    await check_free_username_and_email(user.username,user.email)
    usr = await create_user(user)

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    token = await create_access_token(data={"username": user.username, "email": user.email}, expires_delta=access_token_expires)

    return UserInResponse(user=UserToken(**usr.dict(), token=token))

@router.get("/already_seen",
    tags=["Film already seen"],
)
async def already_seen(username: str):
    list_film_already_seen = await get_films_already_seen_by_user(username)
    # access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    # token = await create_access_token(data={"username": user.username, "email": user.email}, expires_delta=access_token_expires)

    return list_film_already_seen