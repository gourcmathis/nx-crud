from fastapi import FastAPI, Body, HTTPException, status, APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ...db.connection import user_collection
from ...serializers.user_schema import users_serializer, single_user_serializer
from ...crud.helpers.user_helper import create_user, check_free_username_and_email, create_access_token, get_user_by_email
from ...models.user_model import UserInCreate, UserInDB, UserInResponse, UserToken, UserInLogin
from datetime import timedelta
from ...security.security import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/users",
)

@router.get("/")
async def users():
    users = user_collection.find({})
    return users_serializer(users)

@router.post("/login", response_model=UserInResponse, tags=["authentication"])
async def login(user: UserInLogin):

    usr = await get_user_by_email(user.email)

    if not usr or not usr.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password"
        )

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    token = await create_access_token(data={"username": usr.username}, expires_delta=access_token_expires)
    return UserInResponse(user=UserToken(**usr.dict(), token=token))


@router.post("/sign_up",
    response_model=UserInResponse,
    tags=["authentication"],
    status_code=HTTP_201_CREATED,
)
async def sign_up(user: UserInCreate):
    
    await check_free_username_and_email(user.username,user.email)
    usr = await create_user(user)

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    token = await create_access_token(data={"username": user.username}, expires_delta=access_token_expires)

    return UserInResponse(user=UserToken(**usr.dict(), token=token))

