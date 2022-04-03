
from ...models.user_model import UserInDB, UserInCreate,UserToken, UserBase
from ...models.group_model import Group
from ...models.token_model import TokenPayload
from ...serializers.user_schema import single_user_serializer
from ...security.security import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from tortoise.exceptions import DoesNotExist
from fastapi import Depends, HTTPException, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from bson.objectid import ObjectId
from ...db.connection import user_collection, dbfilms, group_collection
from pydantic import EmailStr
from jose import JWTError, jwt
from typing import Optional, List
from starlette.exceptions import HTTPException
from fastapi import Depends, Header
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
)

JWT_TOKEN_PREFIX = "Token"

async def create_user(user: UserInCreate) -> UserInDB:
    """
        user: UserInCreate, user for creation
        description: insert a user in database
    """
    usr = UserInDB(**user.dict())
    usr.change_password(user.password)
    
    row = user_collection.insert_one(usr.dict())

    return usr

async def get_user(username: str) -> UserInDB:
    """
        username: str, name unique of user
        description: get user by username
    """
    row = user_collection.find_one({"username": username})
    if row == None:
        raise                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        HTTPException(
            status_code=404, detail=" user not found by username!"
        )
    else:
        return UserInDB(**row)

async def get_user_by_email(email: str) -> UserBase:
    """
        email: EmailStr, email unique of user
        description: get user by email
    """
    row = user_collection.find_one({"email": email})
    if row == None:
        HTTPException(
                status_code=404, detail=" user not found by email!"
            )
    else:   
        return UserInDB(**row)

async def get_all_group_of_user(username: str) -> List:
    """
        username: Optional[str], name unique of user
        email: Optional[EmailStr], email unique of user
        description: verify if a user exist in database with the username or/and email given
    """
    list_group = []
    exist_user = user_collection.find_one({"username":username})

    if exist_user != None:
        user = UserInDB(**exist_user)
        for groupname in user.list_group:
            group = group_collection.find_one({"groupname": groupname})
            grp = Group(**group)
            list_group.append(grp)
        return list_group


async def check_free_username_and_email(
     username: Optional[str] = None, email: Optional[EmailStr] = None
):
    """
        username: Optional[str], name unique of user
        email: Optional[EmailStr], email unique of user
        description: verify if a user exist in database with the username or/and email given
    """
    if username:
        user_by_username = user_collection.find_one({"username": username})

        if user_by_username != None:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Un utilisateur avec ce username existe déjà!",
            )

    if email:
        user_by_email = user_collection.find_one({"email": email})
        if user_by_email != None:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Vous êtes déjà inscrit",
            )


async def get_films_already_seen_by_user(username: str) -> List[str]:
    exist_user = user_collection.find_one({"username":username})

    if exist_user:
        user = UserBase(**exist_user)
        return  user.already_seen

    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail="Aucun films déjà vue",
    )


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        token_url: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": token_url, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail="Not authenticated",
                )
            else:
                return None

        return param


security = OAuth2PasswordBearerCookie(token_url="/login")


async def get_current_user(token: str = Depends(security)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenPayload(username=username)
    except JWTError:
        raise credentials_exception
    try:
        user = user_collection.find_one({"username":token_data.username})
    except DoesNotExist:
        raise credentials_exception
    
    user = user_collection.find_one({"username":token_data.username})
    
    if user == None:
        raise credentials_exception

    return single_user_serializer(user)