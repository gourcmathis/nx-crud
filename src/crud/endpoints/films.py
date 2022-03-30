import os
from fastapi import FastAPI, Body, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
from pymongo import MongoClient
from dotenv import load_dotenv 

from ..db.connection import dbfilms
from ..serializers.film_schema import films_serializer, single_film_serializer

API_PATH = "localhost:5000/api/v1"


class FilmModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "imdb_id": "tt1160419",
                "title": "Dune",
                "image": "https://imdb-api.com/images/original/MV5BN2FjNmEyNWMtYzM0ZS00NjIyLTg5YzYtYThlMGVjNzE1OGViXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_Ratio0.6837_AL_.jpg",
                "description": "(2021)",
                "genres": "Action, Adventure, Drama"
            }
        }


router = APIRouter(
    prefix="/films",
)


@router.get(
    "/", response_description="List all films", #response_model=List[FilmModel]
)
async def list_movies():
    films = dbfilms.find({})
    return films_serializer(films)