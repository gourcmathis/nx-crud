
def single_group_serializer(group) -> dict:
    return {
        "id": str(group["_id"]),
        "groupname": group["groupname"],
        "author": group["author"] if "author" in group else "",
        "description": group["description"] if "description" in group else "",
        "image": group["image"] if "image" in group else "",
        "listmember": group["listmember"] if "listmember" in group else [],
        "aready_seen_by_allmember": group["aready_seen_by_allmember"] if "aready_seen_by_allmember" in group else [],
        "list_favorites_films": group["list_favorites_films"] if "list_favorites_films" in group else [],
        "list_favorites_genres": group["list_favorites_genres"] if "list_favorites_genres" in group else [],
    }

def groups_serializer(groups) -> list:
    return [single_group_serializer(group) for group in groups]