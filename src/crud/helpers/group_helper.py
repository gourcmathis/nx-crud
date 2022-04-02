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
        """
        username: sername of user to add
        groupname: str, name unique of group
        description: add member in group by his username
        return: Group updated
        """

        exist_group = group_collection.find_one({"groupname": groupname})
        exist_user = user_collection.find_one({"username": username})

        if exist_group and exist_user:
            user  = UserInDB(**exist_user)
            group = Group(**exist_group)
            group.listmember.append(user.username)
            for film in user.already_seen:
                group.aready_seen_by_allmember.append(film)
            group_collection.update_one({ "groupname": groupname },{"$set": {"listmember": group.listmember}})
            group_collection.update_one({ "groupname": groupname },{"$set": {"aready_seen_by_allmember": group.aready_seen_by_allmember}})
            return group

# async def get_user():

async def add_many_member(list_username: List[str], groupname: str) -> Group:
    """
        list_username: list of username to add in group
        groupname: str, name unique of group
        description: add many member in group by their usernames
        return: Group updated
    """
    for username in list_username:
       group = await add_member(username, groupname)
    
    return group


async def get_all_members_group(groupname: str) -> List[UserBase]:
    """
        groupname: str, name unique of group
        description: get all member of group by groupname
        return: Group updated
    """
    exist_group = group_collection.find_one({"groupname":groupname})
    
    if exist_group:
        group = Group(**exist_group)
        list_users = []
        for username in group.listmember:
            user_bdd = user_collection.find_one({"username":username})
            user = UserBase(**user_bdd)
            list_users.append(user)
        return list_users