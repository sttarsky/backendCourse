from src.models.rooms import RoomsOrm
from src.repository.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm
