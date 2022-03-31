from fastapi import FastAPI, Body, HTTPException, status, APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ...db.connection import user_collection, group_collection
from ...serializers.group_schema import groups_serializer
from ...crud.helpers.user_helper import create_access_token
from ...models.user_model import UserToken

from ...models.group_model import Group
from datetime import timedelta
from ...security.security import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix="/groups",
)

@router.get("/", tags=["Group"],)
async def groups():
    groups = group_collection.find({})
    return groups_serializer(groups)


@router.post("/create",
    response_model=Group,
    tags=["Group"],
    status_code=HTTP_201_CREATED,
)
async def create(username:str, group: Group):
    usr = user_collection.find_one({"username":username})
    
    if usr:
        user = UserToken(**usr)
        grp  = user.create_group(group)
        
        # access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        # token = await create_access_token(data={"groupname": group.groupname}, expires_delta=access_token_expires)
        return grp
    else:
        raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Création de groupe impossible: username of creator incorrecte",
            )

