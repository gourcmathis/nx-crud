
def single_user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "adresse": user["adresse"],
    }


def users_serializer(users) -> list:
    return [single_user_serializer(user) for user in users]