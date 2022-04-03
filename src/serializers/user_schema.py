# from ..models.user_model import UserInDB,UserInCreate

def single_user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"],
        "already_seen": user["already_seen"] if "already_seen" in user else [],
        "favorite_films": user["favorite_films"] if "favorite_films" in user else [],
        "favorite_genres": user["favorite_genres"] if "favorite_genres" in user else [],
        "list_group": user["list_group"] if "list_group" in user else [],
    }


def users_serializer(users) -> list:
    return [single_user_serializer(user) for user in users]