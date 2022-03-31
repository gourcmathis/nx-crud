from typing import Optional
from pydantic import BaseModel, AnyUrl, Field

class FilmBase(BaseModel):
    imdb_id: str
    title: str
    year: Optional[str] = ""
    description: Optional[str] = ""
    genres: Optional[list] = None
    image: Optional[str] = ""
    trailer: Optional[str] = ""
    rating: Optional[str] = ""

