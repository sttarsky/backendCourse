from src.models.bookings import BookingsORM
from src.repository.base import BaseRepository
from src.repository.mappers.mappers import BookingMapper


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingMapper
