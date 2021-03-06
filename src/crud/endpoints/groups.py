from fastapi import FastAPI, Body, HTTPException, status, APIRouter,Depends
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from ...db.connection import user_collection, group_collection
from ...serializers.group_schema import groups_serializer, single_group_serializer
from ...security.security import create_access_token
from ...models.user_model import UserBase, UserInDB, UserToken
from ..helpers.group_helper import add_member, check_member_already_in_group, check_groupname_exist_already, get_all_members_group
from ..helpers.user_helper import get_all_group_of_user
from ...models.group_model import Group
from datetime import timedelta
from typing import List
from ...security.security import ACCESS_TOKEN_EXPIRE_MINUTES, JWTBearer

router = APIRouter(
    prefix="/groups",
)

@router.get("/", tags=["Group"]) #, dependencies=[Depends(JWTBearer())])
async def groups():
    groups = group_collection.find({})
    return groups_serializer(groups)


@router.post("/create/by={username}",
    response_model=Group,
    tags=["Group"],
    status_code=HTTP_201_CREATED,
    # dependencies=[Depends(JWTBearer())]
)
async def create(username:str, group: OAuth2PasswordRequestForm = Depends(Group)) -> Group:
    usr = user_collection.find_one({"username":username})

    if usr != None:
        user = UserToken(**usr)
        await check_groupname_exist_already(group.groupname)
        grp  = user.create_group(group)

    # add all movies seen by user who create the group
        for film in user.already_seen:
            grp.aready_seen_by_allmember.append(film)
        group_collection.update_one({ "groupname": grp.groupname },{"$set": {"aready_seen_by_allmember": grp.aready_seen_by_allmember}})

        return grp
    else:
        raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Création de groupe impossible",
            )

@router.post("/addmember/username={username}/groupname={groupname}",
    response_model=Group,
    tags=["Group"],
    # dependencies=[Depends(JWTBearer())]
)
async def addmember(username:str, groupname: str) -> Group:
    await check_member_already_in_group(username, groupname)

    grp  = await add_member(username, groupname)

    return grp

@router.get("/allmembers/groupname={groupname}",
    response_model=List[UserBase],
    tags=["Group"],
    # dependencies=[Depends(JWTBearer())]
)
async def get_all_members(groupname: str) -> List[UserBase]:
    all_members = await get_all_members_group(groupname)

    return all_members


@router.get("/allgroups/of={username}",
    response_model=List[Group],
    tags=["Group"],
    # dependencies=[Depends(JWTBearer())]
)
async def get_all_groups(username: str) -> List[Group]:
    all_groups = await get_all_group_of_user(username)

    return all_groups
