from datetime import date

from sqlalchemy import select, func
from watchfiles import awatch

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repository.base import BaseRepository
from src.repository.utils import get_rooms
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self, location, title, limit, offset):
        query = select(self.model)
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(item) for item in result.scalars().all()]

    async def get_filtered_by_time(self,
                                   date_from: date,
                                   date_to: date
                                   ):
        rooms_to_get = get_rooms(date_to=date_to, date_from=date_from)
        hotels_to_get = (select(RoomsOrm.hotel_id)
                         .select_from(RoomsOrm)
                         .filter(RoomsOrm.id.in_(rooms_to_get))
                         )
        return await self.get_filtered(self.model.id.in_(hotels_to_get))
