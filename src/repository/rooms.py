from datetime import date

from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.exceptions import RoomNotFoundException
from src.models.rooms import RoomsOrm
from src.repository.base import BaseRepository
from src.repository.mappers.mappers import (
    RoomMapper,
    RoomWithRelsMapper,
    RoomFacilityDataMapper,
)
from src.repository.utils import get_rooms


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomMapper

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_id_avaliable = get_rooms(
            hotel_id=hotel_id, date_to=date_to, date_from=date_from
        )
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_id_avaliable))
        )
        result = await self.session.execute(query)
        return [
            RoomWithRelsMapper.map_to_domain_entity(item)
            for item in result.scalars().all()
        ]

    async def get_one(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
            return RoomWithRelsMapper.map_to_domain_entity(model)
        except NoResultFound:
            raise RoomNotFoundException

    async def delete_cascade(self, room_id: int, hotel_id: int) -> None:
        delete_stmt = delete(RoomFacilityDataMapper.db_model).filter_by(room_id=room_id)
        await self.session.execute(delete_stmt)
        await self.delete(id=room_id, hotel_id=hotel_id)
