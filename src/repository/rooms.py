from datetime import date
from src.models.rooms import RoomsOrm
from src.repository.base import BaseRepository
from src.repository.utils import get_rooms
from src.schemas.rooms import Rooms


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_filtered_by_time(self,
                                   hotel_id: int,
                                   date_from: date,
                                   date_to: date
                                   ):
        rooms_id_avaliable = get_rooms(hotel_id=hotel_id, date_to=date_to, date_from=date_from)
        return await self.get_filtered(self.model.id.in_(rooms_id_avaliable))
