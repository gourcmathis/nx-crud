# Serialize films from imdb database, this structure will be used in our database
def imdb_single_film_serializer(film) -> dict:
    genres = []
    for genre in range(len(film["genreList"])):
        # push values to a list of genres
        genres.append(film["genreList"][genre]['value'])

    return {
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

# Serialize films from our database
def netflex_single_film_serializer(film) -> dict:
    return {
        "id": str(film["_id"]),
        "imdb_id": film["imdb_id"],
        "title": film["title"],
        "year": film["year"] if "year" in film else "",
        "image": film["image"] if "image" in film else "",
        "description": film["description"] if "description" in film else "",
        "genres": film["genres"] if "genres" in film else [],
        "trailer": film["trailer"] if "trailer" in film else "",
        "rating": film["rating"] if "rating" in film else "",
        "runtime": film["runtime"] if "runtime" in film else "",
    }


# Serialize films from imdb database, this structure will be used in our database
def imdb_films_serializer(films) -> list:
    return [imdb_single_film_serializer(film) for film in films]


# Serialize films from our database
def films_serializer(films) -> list:
    return [netflex_single_film_serializer(film) for film in films]

