from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityADD
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def post_facilities(db: DBDep, title: FacilityADD = Body()):
    facility = await db.facilities.add(title)
    test_task.delay()
    await db.commit()
    return {"status": "ok", "facility": facility}
