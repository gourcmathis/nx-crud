
def single_film_serializer(film) -> dict:
    return {
        "id": str(film["_id"]),
        "imdb_id": film["id"],
        "title": film["title"],
        "year": film["description"] if "description" in film else "",
        "image": film["image"] if "image" in film else "",
        "description": film["plot"] if "plot" in film else "",
        "genres": film["genreList"] if "genreList" in film else [],
        "trailer": film["trailer"] if "trailer" in film else "",
        "rating": film["imDbRating"] if "imDbRating" in film else "",
        "runtime": film["runtimeStr"] if "runtimeStr" in film else "",
    }

def films_serializer(films) -> list:
    return [single_film_serializer(film) for film in films]