import os
from fastapi import FastAPI, Body, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, AnyHttpUrl
from bson import ObjectId
from typing import Optional, List
from pymongo import MongoClient
from dotenv import load_dotenv
import requests_async as requests

from ...db.connection import dbfilms
from ...serializers.film_schema import films_serializer, single_film_serializer

"""
Callbacks for CRUD - IMDB API operations
"""

API_PATH = "http://imdb:5000"

callback_router = APIRouter()

@callback_router.get(
    "{$callback_url}/api/v1/get_250/"
)
@callback_router.post(
    "{$callback_url}/"
)
async def postFilmsToDB():
    client = MongoClient(os.getenv("DATABASE_URL_CONNECTION"))
    db = client.films
    films = await dbfilms.get_films()
    for film in films:
        await dbfilms.post_film(film)
    return JSONResponse(status_code=status.HTTP_200_OK)


"""
Routers section
"""

router = APIRouter(
    prefix="/films",
)

# List all films in the database.
# If the database is empty, then we call the callback to populate it.
@router.get(
    "/", response_description="List films from the database", callbacks=callback_router.routes, tags=["Films"]
)
async def list_movies(callback_url: Optional[AnyHttpUrl] = API_PATH):
    films = dbfilms.find({})
    jsonFilms = films_serializer(films)

    # if the database is empty, we need to call the API to get some films
    if len(jsonFilms) == 0:
        response = await requests.get(f"{callback_url}/api/v1/get_250/")
        dbfilms.insert_many(response.json())
        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    return jsonFilms
