from datetime import date

from sqlalchemy import select

from src.models.bookings import BookingsORM
from src.repository.base import BaseRepository
from src.repository.mappers.mappers import BookingMapper


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingMapper

    async def get_bookings_checkin(self):
        query = (
            select(self.model)
            .filter(self.model.date_from == date.today())
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in result.scalars().all()]
