from .rwmodel import RWModel, DBModelMixin
from typing import Optional
from pydantic import BaseModel, EmailStr, AnyUrl, Field
from ..security.security import verify_password, generate_salt, get_password_hash, pwd_context

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
    

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None