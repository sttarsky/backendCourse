from src.models.hotels import HotelsOrm
from src.repository.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm
