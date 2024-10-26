
from fastapi import APIRouter, HTTPException

from src.databases import async_session_maker
from src.repository.rooms import RoomsRepository
from src.schemas.rooms import RoomADD, RoomPATCH

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).get_all(hotel_id)
        return result


@router.get('/{hotel_id}/rooms/{room_id}')
async def get_one_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).get_one_or_none(hotel_id, room_id)
        if not result:
            raise HTTPException(status_code=404, detail='Room not found')
        return result


@router.post("/{hotel_id}/rooms")
async def create_room(room_data: RoomADD):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms")
async def put_hotel(hotel_id: int, room_data: RoomADD):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=hotel_id)
        await session.commit()
        return {"status": "ok"}


@router.patch("/{room_id}")
async def patch_hotel(room_id: int, room_data: RoomPATCH):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()
        return {"status": "ok"}


@router.delete("/{hotel_id}")
async def del_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=hotel_id)
        await session.commit()
        return {"status": "ok"}


