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
    await check_groupname_exist_already(group.groupname)

    if usr != None:
        user = UserToken(**usr)
        grp  = user.create_group(group)

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
async def get_members(groupname: str) -> List[UserBase]:
    all_members = await get_all_members_group(groupname)

    return all_members