from urllib import response
from fastapi import FastAPI,APIRouter, Depends
from .db.connection import user_collection
from .serializers.user_schema import users_serializer, single_user_serializer
from fastapi.middleware.cors import CORSMiddleware
from .crud.user import create_user, check_free_username_and_email
from .models.user_model import UserInCreate, UserInDB

app = FastAPI()
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_event_handler("startup",connect_to_mongo)

@app.get("/")
async def home():
    return "add success Mamiwata!"

@app.get("/users")
async def users():
    users = user_collection.find({})
    return users_serializer(users)

@app.post("/sign_up")
async def sign_up(user: UserInCreate):
    await check_free_username_and_email(user.username,user.email)
    usr = await create_user(user)
    return usr