from fastapi import FastAPI, Body, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ...db.connection import user_collection
from ...serializers.user_schema import users_serializer, single_user_serializer
from ...crud.user import create_user, check_free_username_and_email
from ...models.user_model import UserInCreate, UserInDB

router = APIRouter(
    prefix="/users",
)

@router.get("/")
async def users():
    users = user_collection.find({})
    return users_serializer(users)

@router.post("/sign_up")
async def sign_up(user: UserInCreate):
    await check_free_username_and_email(user.username,user.email)
    usr = await create_user(user)
    return usr