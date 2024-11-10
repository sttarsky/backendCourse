from datetime import date

from fastapi import APIRouter, Query, Body
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.facilities import FacilitiesADD
from src.schemas.hotels import HotelADD, HotelPATCH

router = APIRouter(prefix="/facilities", tags=['Удобства'])


@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def post_facilities(db: DBDep, title: FacilitiesADD):
    facility = await db.facilities.add(title)
    await db.commit()
    return {"status": "ok", "facility": facility}
