
from ...models.user_model import UserInDB, UserInCreate,UserBase, verify_password
from ...models.film_model import FilmBase
from ...security.security import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from bson.objectid import ObjectId
from ...db.connection import user_collection, dbfilms
from pydantic import EmailStr
from typing import Optional
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY
)

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
    if row:
        return UserInDB(**row)


async def get_user_by_email(email: EmailStr):
    """
        email: EmailStr, email unique of user
        description: get user by email
    """
    row = user_collection.find_one({"email": email})
    if row:
        return UserInDB(**row)


async def check_free_username_and_email(
     username: Optional[str] = None, email: Optional[EmailStr] = None
):
    """
        username: Optional[str], name unique of user
        email: Optional[EmailStr], email unique of user
        description: verify if a user exist in database with the username or/and email given
    """
    if username:
        user_by_username = await get_user(username)
        if user_by_username:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Un utilisateur avec ce username existe déjà!",
            )

    if email:
        user_by_email = await get_user_by_email(email)
        if user_by_email:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Vous êtes déjà inscrit",
            )





# async def authenticate_user(username: str, password: str):
#     user = get_user(username)
#     if not user:
#         return False
#     if not verify_password(password, user.password):
#         return False
#     return user


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user