from fastapi import FastAPI, Body, HTTPException, status, APIRouter,Depends
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from ...db.connection import user_collection, group_collection
from ...serializers.group_schema import groups_serializer, single_group_serializer
from ...models.user_model import UserBase, UserInDB, UserToken
from ..helpers.user_helper import get_all_group_of_user
from ..helpers.suggestions_helper import suggestions
from ...models.group_model import Group

router = APIRouter(
    prefix="/suggestions",
)

@router.post("/for{groupname}", tags=["Group"]) #, dependencies=[Depends(JWTBearer())])
async def make_suggestions(groupname: str):
    return await suggestions(groupname)
