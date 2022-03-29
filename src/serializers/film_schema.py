
def single_film_serializer(film) -> dict:
    return {
        "id": str(film["_id"]),
        "imdb_id": film["id"],
        "title": film["title"],
        "image": film["image"],
        "description": film["description"],
        "genres": film["genres"]
    }

def films_serializer(films) -> list:
    return [single_film_serializer(film) for film in films]