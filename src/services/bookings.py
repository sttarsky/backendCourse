from src.exceptions import ObjectNotFoundException, RoomNotFoundException, DateMissmatchExeption
from src.schemas.bookings import BookingADD, BookingADDRequest
from src.services.base import BaseService


class BookingService(BaseService):
    async def get_my_bookings(self, user_id):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def post_booking(self, user_id: int, data: BookingADDRequest):
        if data.date_from > data.date_to:
            raise DateMissmatchExeption
        try:
            room = await self.db.rooms.get_one(id=data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        hotel = await self.db.hotels.get_one(id=room.hotel_id)
        room_price: int = room.price
        _booking_data = BookingADD(
            user_id=user_id, price=room_price, **data.model_dump()
        )
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        await self.db.commit()
        return booking

    async def get_all_bookings(self):
        return await self.db.bookings.get_all()
