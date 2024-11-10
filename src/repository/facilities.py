from src.models.facilities import FacilitiesORM
from src.repository.base import BaseRepository
from src.schemas.facilities import Facilities


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facilities
