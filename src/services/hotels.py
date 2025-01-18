from datetime import date

from src.exceptions import check_dates
from src.services.base import BaseService
from src.schemas.hotels import HotelADD, HotelPATCH


class HotelService(BaseService):
    async def get_filtered_by_time(self,
                                   pagination,
                                   location: str | None,
                                   title: str | None,
                                   date_from: date,
                                   date_to: date,
                                   ):
        check_dates(date_from, date_to)
        per_page = pagination.per_page or 5
        offset = per_page * (pagination.page - 1)
        return await self.db.hotels.get_filtered_by_time(
            date_to=date_to,
            date_from=date_from,
            limit=per_page,
            offset=offset,
            location=location,
            title=title,
        )

    async def get_one(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, data: HotelADD):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def edit_hotel(self, hotel_id: int, data: HotelADD):
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()

    async def edit_hotel_partially(self, hotel_id: int, data: HotelPATCH, exclude_unset: bool = False):
        await self.db.hotels.edit(data, exclude_unset=exclude_unset, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
