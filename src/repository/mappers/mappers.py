from src.models.hotels import HotelsOrm
from src.repository.mappers.base import DataMapper
from src.schemas.hotels import Hotel


class HotelMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel
