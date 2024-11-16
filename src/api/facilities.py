
from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityADD

router = APIRouter(prefix="/facilities", tags=['Удобства'])


@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def post_facilities(db: DBDep, title: FacilityADD = Body()):
    facility = await db.facilities.add(title)
    await db.commit()
    return {"status": "ok", "facility": facility}
