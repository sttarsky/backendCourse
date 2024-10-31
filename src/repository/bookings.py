from src.models.bookings import BookingsORM
from src.repository.base import BaseRepository
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Booking
