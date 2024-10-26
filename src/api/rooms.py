from fastapi import APIRouter, HTTPException, Body

from src.databases import async_session_maker
from src.repository.rooms import RoomsRepository
from src.schemas.rooms import RoomADD, RoomPATCH, RoomADDRequest, RoomPATCHRequest

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).get_filtered(hotel_id=hotel_id)
        return result


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_one_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)
        if not result:
            raise HTTPException(status_code=404, detail='Room not found')
        return result


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id: int, room_data: RoomADDRequest = Body()):
    _room_data = RoomADD(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room_id(hotel_id: int, room_id: int, room_data: RoomADDRequest):
    _room_data = RoomADD(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, id=room_id)
        await session.commit()
        return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_hotel(hotel_id: int, room_id: int, room_data: RoomPATCHRequest):
    _room_data = RoomPATCH(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()
        return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def del_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id, hotel_id=hotel_id)
        await session.commit()
        return {"status": "ok"}
