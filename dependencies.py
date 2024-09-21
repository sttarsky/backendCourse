
from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(None, ge=0)]
    per_page: Annotated[int | None, Query(None, ge=0, le=30)]

PaginationDep = Annotated[PaginationParams, Depends()]