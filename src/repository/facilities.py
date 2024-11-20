from os.path import exists

from sqlalchemy import select, insert, delete

from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.repository.base import BaseRepository
from src.repository.mappers.mappers import FacilityMapper
from src.schemas.facilities import RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    mapper = FacilityMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]):
        query = select(RoomsFacilitiesORM).filter_by(room_id=room_id)
        facilities = await self.session.execute(query)
        exist_facilities = [item.facility_id for item in facilities.scalars().all()]
        add_facilities = list(set(facilities_ids) - set(exist_facilities))
        rem_facilities = list(set(exist_facilities) - set(facilities_ids))
        if add_facilities:
            add_data = [{"room_id": room_id, "facility_id": facility_id} for facility_id in add_facilities]
            add_stmt = insert(RoomsFacilitiesORM).values(add_data)
            await self.session.execute(add_stmt)
        if rem_facilities:
            rem_stmt = (
                delete(RoomsFacilitiesORM)
                .filter(
                    RoomsFacilitiesORM.room_id == room_id,
                    RoomsFacilitiesORM.facility_id.in_(rem_facilities)
                )
            )
            await self.session.execute(rem_stmt)
