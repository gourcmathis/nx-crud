from fastapi import APIRouter
from ..helpers.suggestions_helper import suggestions

router = APIRouter(
    prefix="/suggestions",
)

@router.post("/for{groupname}", tags=["Group"])
async def make_suggestions(groupname: str):
    return await suggestions(groupname)
