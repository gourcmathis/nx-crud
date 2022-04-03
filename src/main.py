from urllib import response
from fastapi import FastAPI,APIRouter, Depends
# from .db.connection import user_collection
# from .serializers.user_schema import users_serializer, single_user_serializer
from fastapi.middleware.cors import CORSMiddleware
# from .crud.user import create_user, check_free_username_and_email
# from .models.user_model import UserInCreate, UserInDB

from src.crud.endpoints import films, users, groups, suggestions

app = FastAPI()
origins = [
    "http://localhost:8080",
]


app.include_router(films.router)
app.include_router(users.router)
app.include_router(groups.router)
app.include_router(suggestions.router)

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