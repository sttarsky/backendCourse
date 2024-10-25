from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel
from typing import Annotated

from src.services.auth import AuthServices


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=0)]
    per_page: Annotated[int | None, Query(None, ge=0, le=30)]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request):
    access_token = request.cookies.get('access_token')
    print(access_token)
    if not access_token:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return access_token


def get_cur_user(token: str = Depends(get_token)):
    result = AuthServices.decode_token(token)
    return result


UserIdDep = Annotated[int, Depends(get_cur_user)]
