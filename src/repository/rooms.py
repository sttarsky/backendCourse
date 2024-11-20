from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.rooms import RoomsOrm
from src.repository.base import BaseRepository
from src.repository.mappers.mappers import RoomMapper
from src.repository.utils import get_rooms


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomMapper

    async def get_filtered_by_time(self,
                                   hotel_id: int,
                                   date_from: date,
                                   date_to: date
                                   ):
        rooms_id_avaliable = get_rooms(hotel_id=hotel_id, date_to=date_to, date_from=date_from)
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_id_avaliable))
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(item) for item in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = (select(self.model)
                 .options(selectinload(self.model.facilities))
                 .filter_by(**filter_by)
                 )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)
