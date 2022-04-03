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
from ..helpers.suggestions_helper import suggestions
from ...models.group_model import Group
from datetime import timedelta
from typing import List
from ...security.security import ACCESS_TOKEN_EXPIRE_MINUTES, JWTBearer

router = APIRouter(
    prefix="/suggestions",
)

@router.post("/for{groupname}", tags=["Group"]) #, dependencies=[Depends(JWTBearer())])
async def make_suggestions(groupname: str):
    pass