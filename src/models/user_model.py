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
        return verify_password(self.salt + password, self.password)
    
    async def change_password(self, password: str):
        self.salt = generate_salt()
        self.password = get_password_hash(self.salt + password)


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
        #specify author of group
        group.author=self.username

        #update list of member 
        group.listmember.append(self.username)

        for film in self.favorite_films:
            group.list_favorites_films.append(film)
        
        for genre in self.favorite_genres:
            group.list_favorites_genres.append(genre)

        #update list of group
        self.list_group.append(group.groupname)
        
        #updat elist of group in database
        user_collection.update_one({"username":self.username}, {"$set":{"list_group":self.list_group}})
        
        #crete group
        group_collection.insert_one(group.dict())

        return group

class UserInResponse(RWModel):
    user: UserToken
    message: Optional[str]

class UserInLogin(RWModel):
    email: EmailStr
    password: str
    
    