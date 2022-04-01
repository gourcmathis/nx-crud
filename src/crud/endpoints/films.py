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
from ...serializers.user_schema import single_user_serializer
from ...models.film_model import FilmBase
from ..helpers.film_helper import add_film_already_seen, UserToken

"""
Callbacks for CRUD - IMDB API operations
"""

API_PATH = "http://imdb:5000"

callback_router = APIRouter()

@callback_router.get(
    "{$callback_url}/api/v1/"
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
    "/", response_description="List films from the database", response_model=FilmBase, callbacks=callback_router.routes, tags=["Show all films"],
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


# Get a single film by its ID from netflexdb.
@router.get(
    "/id={imdb_id}", response_description="Get a single film from mongodb", response_model=FilmBase, callbacks=callback_router.routes, tags=["Get a film by id from netflexdb"],
)
async def get_movie(imdb_id: str):
    film_req = dbfilms.find_one({"id": imdb_id})
    if film_req is None:
        raise HTTPException(status_code=404, detail="Film not found")
    film = single_film_serializer(film_req)
    
    # if film doesnt have trailer, make a call to the API to get it
    if film["trailer"] == "":
        response = await requests.get(f"{API_PATH}/api/v1/get_trailer/{imdb_id}")
        if response.status_code == 200:
            film["trailer"] = response.json()
            dbfilms.update_one({"id": imdb_id}, {"$set": {"trailer": response.json()}})

    return (film)

# Search films by title from the database
@router.get(
    "/search/title={title}", response_description="Search films by title from the database", response_model=List[FilmBase], tags=["Search films by title"],
)
async def search_movie(title: str):
    films_req = dbfilms.find({"title": {"$regex": title, "$options": "i"}})
    films =  films_serializer(films_req)
    if (len(films) == 0):
        raise HTTPException(status_code=404, detail="Film not found")
    return films

@router.post(
    "/id={imdb_id}/as_already_seen/by={username}", response_description="add film alredy seen by user in his list already seen", 
    tags=["add film as already seen by user"],
)
async def film_already_seen(imdb_id: str, username: str) -> UserToken:
    user =  await add_film_already_seen(imdb_id, username)
    if user:
        # user = single_user_serializer(user)
        return user