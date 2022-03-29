from urllib import response
from fastapi import FastAPI,APIRouter, Depends
from .db.mongoclient import dbusers
# from .db.connection import connect_to_mongo, get_database , AsyncIOMotorClient,user_collection_name, database_name
from .serializers.user_schema import users_serializer, single_user_serializer
from fastapi.middleware.cors import CORSMiddleware
from typing import List
# from .db.connection import db

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
    users = dbusers.find({})
    return users_serializer(users)