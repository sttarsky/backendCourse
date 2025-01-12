from datetime import date

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.exceptions import AllRoomsAreBookedException
from src.models import RoomsOrm
from src.models.bookings import BookingsORM
from src.repository.base import BaseRepository
from src.repository.mappers.mappers import BookingMapper
from src.repository.utils import get_rooms
from src.schemas.bookings import BookingADD


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingMapper

    async def get_bookings_checkin(self):
        query = select(self.model).filter(self.model.date_from == date.today())
        result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(booking)
            for booking in result.scalars().all()
        ]

    async def add_booking(self, data: BookingADD, hotel_id: int):
        rooms_to_get = get_rooms(
            date_to=data.date_to, date_from=data.date_from, hotel_id=hotel_id
        )
        check_available = (
            select(RoomsOrm.id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id == data.room_id)
            .filter(RoomsOrm.id.in_(rooms_to_get))
        )
        result = await self.session.execute(check_available)
        try:
            result.scalar_one()
        except NoResultFound:
            raise AllRoomsAreBookedException
        return await self.add(data)
