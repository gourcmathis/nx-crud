

from ...models.group_model import Group
from ...models.film_model import FilmBase
from typing import List
from ...db.connection import group_collection, dbfilms
from ...serializers.film_schema import films_serializer
from starlette.exceptions import HTTPException


async def suggestions(groupname: str) -> List[FilmBase]:
    exist_group = group_collection.find_one({"groupname":groupname})
    print(exist_group)
    if exist_group != None:
        group = Group(**exist_group)

        list_films_not_already_seen = dbfilms.find({ "id": { "$nin": group.aready_seen_by_allmember } })
        list_films_liked = dbfilms.find({ "id": { "$in": group.list_favorites_films } })
        list_films_with_genre_liked = dbfilms.find({ "genres":{"$in": group.list_favorites_genres} })

        return films_serializer(list_films_with_genre_liked)
    else:
        raise HTTPException(
                status_code=404,
                detail="Group inexistant!!",
            )

        





