

from tokenize import group
from ...models.user_model import UserInDB, UserBase
from ...models.group_model import Group
from ...models.film_model import FilmBase
from typing import Optional, List
from ...db.connection import user_collection, group_collection, dbfilms
from pydantic import EmailStr
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

async def suggestions(groupname: str) -> List[FilmBase]:
    exist_group = group_collection.find_one({"groupname":groupname})
    list_films_suggested =  []
    if exist_group != None:
        group = Group(**exist_group)
    
        list_films_not_already_seen = dbfilms.find({ "id": { "$nin": group.aready_seen_by_allmember } })
        list_films_liked = dbfilms.find({ "id": { "$in": group.list_favorites_films } })
        list_films_with_genre_liked = dbfilms.find({ "genres.value": { "$in": group.list_favorites_genres } })
        # ici trier les résultats puis faire un return, ensuite dans le endpoints suggestions.py faire la route des suggestions
    raise HTTPException(
            status_code=404,
            detail="Groupe inexistant: Donc suggestion impossible!",
        )

        





