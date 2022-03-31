from .rwmodel import RWModel, DBModelMixin
from typing import Optional
from pydantic import BaseModel, EmailStr, AnyUrl, Field
from ..security.security import verify_password, generate_salt, get_password_hash, pwd_context
from ..db.connection import user_collection,group_collection
from ..models.group_model import Group

class UserBase(RWModel):
    username: str
    email: EmailStr
    bio: Optional[str] = ""
    image: Optional[AnyUrl] = None


class UserInDB(UserBase):
    salt: str = ""
    password: str = ""

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.password)
    
    def change_password(self, password: str):
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
    token: str
    def create_group(self, group: Group) -> Group:
        """
            group: Group, group for creation
            description: insert a group in database and add the creator like first member
        """
        group.author=self.username
        group.listmember.append(self.username)
        grp = Group(**group.dict())
        
        row = group_collection.insert_one(grp.dict())

        return grp

class UserInResponse(RWModel):
    user: UserToken

class UserInLogin(RWModel):
    email: EmailStr
    password: str
    
    