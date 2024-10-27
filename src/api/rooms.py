from fastapi import APIRouter, HTTPException, Body
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomADD, RoomPATCH, RoomADDRequest, RoomPATCHRequest

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(hotel_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_one_room(hotel_id: int, db: DBDep, room_id: int):
    result = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if not result:
        raise HTTPException(status_code=404, detail='Room not found')
    return result


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, db: DBDep, room_data: RoomADDRequest = Body()):
    _room_data = RoomADD(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room_id(hotel_id: int, room_id: int, db: DBDep, room_data: RoomADDRequest):
    _room_data = RoomADD(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.add(_room_data, id=room_id)
    await db.commit()
    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_hotel(hotel_id: int, room_id: int, db: DBDep, room_data: RoomPATCHRequest):
    _room_data = RoomPATCH(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.add(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def del_hotel(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "ok"}
