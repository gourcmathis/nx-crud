from .rwmodel import RWModel, DBModelMixin
from typing import Optional, List
from pydantic import BaseModel, EmailStr, AnyUrl, Field

class Group(RWModel):
    groupname: str
    author: Optional[str] = ""
    description: Optional[str] = ""
    image: Optional[str] = ""
    listmember: List[Optional[str]] = []
    aready_seen_by_allmember: List[Optional[str]] = []