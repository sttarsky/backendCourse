from fastapi import Depends, Query, Request
from pydantic import BaseModel
from typing import Annotated

from src.databases import async_session_maker
from src.exceptions import NoAccessTokenHTTPException, IncorrectTokenException, IncorrectTokenHTTPException
from src.services.auth import AuthServices
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=0)]
    per_page: Annotated[int | None, Query(None, ge=0, le=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise NoAccessTokenHTTPException
    return access_token


def get_cur_user(token: str = Depends(get_token)):
    try:
        data = AuthServices.decode_token(token)
        print(data)
    except IncorrectTokenException:
        raise IncorrectTokenHTTPException
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_cur_user)]


async def get_db():
    async with DBManager(async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
