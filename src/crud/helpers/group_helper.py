# from datetime import datetime, timedelta
# from jose import JWTError, jwt
from ...models.user_model import UserInDB,UserInCreate, verify_password
from ...models.group_model import Group
# from ..security.security import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from typing import Optional, List
# from bson.objectid import ObjectId
from ...db.connection import user_collection,group_collection
# from ..serializers.user_schema import users_serializer, single_user_serializer
from pydantic import EmailStr
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY
)


# async def create_group(group: Group, user:Optional[UserInDB] = None) -> Group:
#     """
#         group: Group, group for creation
#         description: insert a group in database
#     """
#     if user:
#         grp = Group(**group.dict(), author=user.username)
#     else:
#         grp = Group(**group.dict())

#     row = group_collection.insert_one(grp.dict())

#     return grp

async def get_groupby_groupname(groupname: str):
    """
        groupname: str, name unique of user
        description: get group by groupname
    """
    row = group_collection.find_one({"groupname": groupname})
    if row:
        return Group(**row)

async def check_groupname_exist_already(
    groupname: Optional[str] = None
):
    """
        groupname: Optional[str], name unique of group
        description: verify if a group's name exist in database with the groupname {groupname}
    """
    if groupname:
        group_by_groupname = await get_groupby_groupname(groupname)
        if group_by_groupname:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Un groupe avec ce nom existe déjà, veuillez changer de nom s'il vous plaît!",
            )

async def addmember(groupname: str):
    pass

# async def get_listmember_group_by_groupname(groupname: str) -> List[UserInDB]:
#     """
#         groupname: str, name unique of user
#         description: get group by groupname
#     """
#     list_
#     row = group_collection.find_one({"groupname": groupname})

#     if row:
#         return Group(**row)