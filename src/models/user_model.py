from .rwmodel import RWModel, DBModelMixin
from typing import Optional, List
from pydantic import BaseModel, EmailStr, AnyUrl, Field
from ..security.security import verify_password, generate_salt, get_password_hash, pwd_context
from ..db.connection import user_collection,group_collection
from ..models.group_model import Group

class UserBase(RWModel):
    username: str
    email: EmailStr
    bio: Optional[str] = ""
    image: Optional[str] = None
    already_seen: List[Optional[str]] = []
    favorite_films: List[Optional[str]] = []
    favorite_genres: List[Optional[str]] = []
    list_group: List[Optional[str]] = []


class UserInDB(UserBase):
    salt: str = ""
    password: str = ""

    async def check_password(self, password: str):
        return await verify_password(self.salt + password, self.password)
    
    async def change_password(self, password: str):
        self.salt = await generate_salt()
        self.password = await get_password_hash(self.salt + password)


class UserInCreate(RWModel):
    """
    Email, username, and password are required for registering a new user
    """
    username: str
    email: EmailStr
    password: str

class UserToken(UserBase):
    token: Optional[str]
    def create_group(self, group: Group) -> Group:
        """
            group: Group, group for creation
            description: insert a group in database and add the creator like first member
        """
        group.author=self.username
        group.listmember.append(self.username)
        self.list_group.append(group)
        grp = Group(**group.dict())
        
        group_collection.insert_one(grp.dict())

        return grp

class UserInResponse(RWModel):
    user: UserToken

class UserInLogin(RWModel):
    email: EmailStr
    password: str
    
    