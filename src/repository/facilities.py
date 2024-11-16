from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repository.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facility


class RoomsFacilitisRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility
