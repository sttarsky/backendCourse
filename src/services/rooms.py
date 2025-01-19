from src.exceptions import (
    check_dates,
    ObjectNotFoundException,
    HotelNotFoundException,
    RoomNotFoundException,
)
from src.schemas.facilities import RoomFacilityADD
from src.schemas.rooms import (
    RoomADDRequest,
    RoomADD,
    RoomPATCHRequest,
    RoomPATCH,
    Rooms,
)
from src.services.base import BaseService
from src.services.hotels import HotelService


class RoomService(BaseService):
    async def get_filtered_by_time(self, hotel_id, date_from, date_to):
        check_dates(date_from, date_to)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_one_room(self, hotel_id: int, room_id: int):
        return await self.db.rooms.get_one(id=room_id, hotel_id=hotel_id)

    async def create_room(self, hotel_id: int, room_data: RoomADDRequest):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex
        _room_data = RoomADD(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(_room_data)
        if room_data.facilities:
            rooms_facilities_data = [
                RoomFacilityADD(room_id=room.id, facility_id=item)
                for item in room_data.facilities
            ]
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
        await self.db.commit()
        return room

    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomADDRequest):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.get_room_with_check(room_id)
        _room_data = RoomADD(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(_room_data, id=room_id)
        await self.db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=room_data.facilities
        )
        await self.db.commit()

    async def partially_edit_room(
        self, hotel_id: int, room_id: int, room_data: RoomPATCHRequest
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id=hotel_id)
        await self.get_room_with_check(room_id)
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPATCH(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.edit(
            _room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id
        )
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id, facilities_ids=_room_data_dict["facilities_ids"]
            )
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)
        await self.db.rooms.delete_cascade(room_id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Rooms:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
