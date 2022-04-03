from .rwmodel import RWModel
from typing import Optional, List

class Group(RWModel):
    groupname: str
    author: Optional[str] = ""
    description: Optional[str] = ""
    image: Optional[str] = ""
    listmember: List[Optional[str]] = []
    aready_seen_by_allmember: List[Optional[str]] = []
    list_favorites_films: List[Optional[str]] = []
    list_favorites_genres: List[Optional[str]] = []
    
