
from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.init import redis_manager
from src.schemas.facilities import FacilityADD
import json

router = APIRouter(prefix="/facilities", tags=['Удобства'])


@router.get("")
async def get_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get('facilities')
    if not facilities_from_cache:
        print('Go in database')
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [facility.model_dump() for facility in facilities]
        facilities_json = json.dumps(facilities_schemas, ensure_ascii=False)
        await redis_manager.set('facilities', facilities_json, 10)
        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts


@router.post("")
async def post_facilities(db: DBDep, title: FacilityADD = Body()):
    facility = await db.facilities.add(title)
    await db.commit()
    return {"status": "ok", "facility": facility}
