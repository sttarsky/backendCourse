from datetime import date
from sqlalchemy import select, func

from src.databases import engine
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsOrm
from src.repository.base import BaseRepository
from src.schemas.rooms import Rooms


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_filtered_by_time(self,
                                   hotel_id: int,
                                   date_from: date,
                                   date_to: date
                                   ):

        """
        !with rooms_booked as (
            select bookings.room_id, count(*) as booked
            from bookings
            where date_from <= '2034-12-14' and date_to >= '2034-11-01'
            group by room_id
        )
        """
        rooms_booked = (select(BookingsORM.room_id, func.count("*").label("booked"))
                        .select_from(BookingsORM)
                        .filter(BookingsORM.date_from <= date_to,
                                BookingsORM.date_to >= date_from)
                        .group_by(BookingsORM.room_id)
                        .cte(name="rooms_booked")
                        )
        """
        rooms_purches as (
            select rooms.id as room_id, rooms.quantity,  quantity - coalesce(booked, 0) as rooms_left
            from rooms
            left join rooms_booked
            on rooms_booked.room_id = rooms.id
        )
        """
        rooms_purches = (
            select(
                self.model.id.label("room_id"),
                (self.model.quantity - func.coalesce(rooms_booked.c.booked, 0)).label("rooms_left")
            )
            .select_from(self.model)
            .outerjoin(rooms_booked, self.model.id == rooms_booked.c.room_id)
            .cte("rooms_purches")
        )
        """
        select *
        from rooms_purches
        where rooms_left > 0;
        """
        query = (
            select("*")
            .select_from(rooms_purches)
            .filter(rooms_purches.c.rooms_left > 0)
        )
        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))
