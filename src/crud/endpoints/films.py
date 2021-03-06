import os
from fastapi import HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
from pydantic import AnyHttpUrl
from typing import Optional, List
from pymongo import MongoClient
import requests_async as requests
from ...db.connection import dbfilms
from ...serializers.film_schema import films_serializer, netflex_single_film_serializer, imdb_films_serializer
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
    "/", response_description="List films from the database", 
    response_model=List[FilmBase], callbacks=callback_router.routes, 
    tags=["Films"],
)
async def list_movies(callback_url: Optional[AnyHttpUrl] = API_PATH):
    films = dbfilms.find({})
    jsonFilms = films_serializer(films)

    # if the database is empty, we need to call the API to get some films
    if len(jsonFilms) == 0:
        response = await requests.get(f"{callback_url}/api/v1/get_100/")
        serializer = imdb_films_serializer(response.json())
        dbfilms.insert_many(serializer)
        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
        )
    return jsonFilms



# Get a single film by its ID from netflexdb.
@router.get(
    "/id={imdb_id}", response_description="Get a single film from mongodb", response_model=FilmBase, callbacks=callback_router.routes, tags=["Films"],
)
async def get_movie(imdb_id: str):
    film_req = dbfilms.find_one({"imdb_id": imdb_id})
    if film_req is None:
        raise HTTPException(status_code=404, detail="Film not found")
    film = netflex_single_film_serializer(film_req)
    
    # if film doesnt have trailer, make a call to the API to get it
    if film["trailer"] == "":
        response = await requests.get(f"{API_PATH}/api/v1/get_trailer/{imdb_id}")
        if response.status_code == 200:
            film["trailer"] = response.json()
            dbfilms.update_one({"id": imdb_id}, {"$set": {"trailer": response.json()}})

    return (film)

# Search films by title from the database
@router.get(
    "/search/title={title}", response_description="Search films by title from the database", response_model=List[FilmBase], tags=["Films"],
)
async def search_movie(title: str):
    films_req = dbfilms.find({"title": {"$regex": title, "$options": "i"}})
    films =  films_serializer(films_req)
    if (len(films) == 0):
        raise HTTPException(status_code=404, detail="Film not found")
    return films

@router.post(
    "/id={imdb_id}/as_already_seen/by={username}", response_description="Films", 
    tags=["add film as already seen by user"],
)
async def film_already_seen(imdb_id: str, username: str) -> UserToken:
    user =  await add_film_already_seen(imdb_id, username)
    if user:
        return user

# Get a single film by its ID from netflexdb.
@router.get(
    "/genres/id={imdb_id}", response_description="Get genre from a film", tags=["Films"],
)
async def get_movie(imdb_id: str):
    film_req = dbfilms.find_one({"id": imdb_id})
    if film_req is None:
        raise HTTPException(status_code=404, detail="Film not found")
    film = netflex_single_film_serializer(film_req)
    
    genres = []
    for genre in range(len(film["genres"])):
        # push values to a list of genres
        genres.append(film["genres"][genre]['value'])

    return genres