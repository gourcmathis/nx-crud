
def single_user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "password": user["password"]
    }


def users_serializer(users) -> list:
    return [single_user_serializer(user) for user in users]