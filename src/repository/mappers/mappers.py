from src.models.bookings import BookingsORM
from src.models.facilities import FacilitiesORM
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.users import UsersORM
from src.repository.mappers.base import DataMapper
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility
from src.schemas.hotels import Hotel
from src.schemas.rooms import Rooms, RoomWithRels
from src.schemas.users import User


class HotelMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class BookingMapper(DataMapper):
    db_model = BookingsORM
    schema = Booking


class FacilityMapper(DataMapper):
    db_model = FacilitiesORM
    schema = Facility


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithRels


class RoomMapper(DataMapper):
    db_model = RoomsOrm
    schema = Rooms


class UserMapper(DataMapper):
    db_model = UsersORM
    schema = User
