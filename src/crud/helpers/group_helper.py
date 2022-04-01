# from datetime import datetime, timedelta
# from jose import JWTError, jwt
from ...models.user_model import UserInDB, UserBase
from ...models.group_model import Group
# from ..security.security import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from typing import Optional, List
from ...db.connection import user_collection, group_collection
from pydantic import EmailStr
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


async def get_groupby_groupname(groupname: str):
    """
        groupname: str, name unique of user
        description: get group by groupname
    """
    row = group_collection.find_one({"groupname": groupname})
    if row:
        return Group(**row)

async def check_groupname_exist_already(groupname: str):
    """
        groupname: Optional[str], name unique of group
        description: verify if a group's name exist in database with the groupname {groupname}
    """
    
    group_by_groupname = await get_groupby_groupname(groupname)
    if group_by_groupname:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Un groupe avec ce nom existe déjà, veuillez changer de nom s'il vous plaît!",
        )

async def check_member_already_in_group(username: str,groupname: str):
    exist_group = await get_groupby_groupname(groupname)

    exist_user = user_collection.find_one({"username": username})

    if exist_group and exist_user:
        if username in exist_group.listmember:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Cet utilisateur est déjà dans ce groupe!",
            )
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Ce groupe n'existe pas!",
        )

async def add_member(username: str,groupname: str) -> Group:

        exist_group = group_collection.find_one({"groupname": groupname})
        exist_user = user_collection.find_one({"username": username})
        if exist_group and exist_user:
            # group = Group(**exist_group)
            user  = UserInDB(**exist_user)
            exist_group.listmember.append(user.username)
            row = group_collection.update_one({ "groupname": groupname },{"$set": {"listmember": exist_group.listmember}})
            return exist_group


async def get_all_members_group(groupname: str) -> List[UserBase]:
    exist_group = group_collection.find_one({"groupname":groupname})
    
    if exist_group:
        group = Group(**exist_group)
        # list_username_member = group.listmember.copy()
        list_users = []
        for username in group.listmember:
            user_bdd = user_collection.find_one({"username":username})
            user = UserBase(**user_bdd)
            list_users.append(user)
        return list_users


# async def get_listmember_group_by_groupname(groupname: str) -> List[UserInDB]:
#     """
#         groupname: str, name unique of user
#         description: get group by groupname
#     """
#     list_
#     row = group_collection.find_one({"groupname": groupname})

#     if row:
#         return Group(**row)