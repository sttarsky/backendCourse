from src.models.rooms import RoomsOrm
from src.repository.base import BaseRepository
from src.schemas.rooms import Rooms


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

