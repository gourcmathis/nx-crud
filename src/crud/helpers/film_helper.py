
from ...models.film_model import FilmBase
from typing import Optional
from ...db.connection import user_collection, dbfilms
from ...models.user_model import UserToken
from .user_helper import get_user
from starlette.exceptions import HTTPException




async def add_film_already_seen(imdb_id: str, username: str):
    exist_user = await get_user(username)
    exist_film = dbfilms.find_one({"id":imdb_id})

    if exist_user and exist_film:
        if imdb_id in exist_user.already_seen:
            raise HTTPException(
                status_code=400,
                detail="Ce film est déjà dans la liste de film vue de cet utilisateur!",
            )
        exist_user.already_seen.append(imdb_id)

        user_collection.update_one({"username":username},{"$set":{"already_seen":exist_user.already_seen}})
        user = user_collection.find_one({"username":username})
        user = UserToken(**user)
        # return single_user_serializer(user)
        return user