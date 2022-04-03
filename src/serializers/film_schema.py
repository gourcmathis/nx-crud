def single_film_serializer(film) -> dict:
    genres = []
    for genre in range(len(film["genreList"])):
        # push values to a list of genres
        genres.append(film["genreList"][genre]['value'])
        
    return {
        "id": str(film["_id"]),
        "imdb_id": film["id"],
        "title": film["title"],
        "year": film["description"] if "description" in film else "",
        "image": film["image"] if "image" in film else "",
        "description": film["plot"] if "plot" in film else "",
        "genres": genres if "genreList" in film else [],
        "trailer": film["trailer"] if "trailer" in film else "",
        "rating": film["imDbRating"] if "imDbRating" in film else "",
        "runtime": film["runtimeStr"] if "runtimeStr" in film else "",
    }

def films_serializer(films) -> list:
    return [single_film_serializer(film) for film in films]