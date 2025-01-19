from datetime import date

from fastapi import APIRouter, Body, Query
from src.api.dependencies import DBDep
from src.exceptions import (
    ObjectNotFoundException,
    HotelNotFoundHTTPException,
    RoomNotFoundHTTPException,
    RoomNotFoundException,
    HotelNotFoundException,
)
from src.schemas.facilities import RoomFacilityADD
from src.schemas.rooms import RoomADD, RoomPATCH, RoomADDRequest, RoomPATCHRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-11-01"),
    date_to: date = Query(example="2024-11-30"),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_one_room(hotel_id: int, db: DBDep, room_id: int):
    try:
        return await RoomService(db).get_one_room(hotel_id=hotel_id, room_id=room_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomADDRequest = Body(
        examples=[
            {
                "title": "string",
                "description": "string",
                "price": 1,
                "quantity": 0,
                "facilities": [],
            }
        ]
    ),
):
    try:
        room = await RoomService(db).create_room(room_data=room_data, hotel_id=hotel_id)
        return {"status": "OK", "data": room}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.put("/{hotel_id}/rooms/{room_id}")
async def put_room_id(
    hotel_id: int, room_id: int, db: DBDep, room_data: RoomADDRequest
):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)
    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def patch_hotel(
    hotel_id: int, room_id: int, db: DBDep, room_data: RoomPATCHRequest
):
    await RoomService(db).partially_edit_room(hotel_id, room_id, room_data)
    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def del_hotel(hotel_id: int, room_id: int, db: DBDep):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
        return {"status": "ok"}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
