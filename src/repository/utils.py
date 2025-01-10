from datetime import date
from sqlalchemy import select, func
from src.models.bookings import BookingsORM
from src.models.rooms import RoomsOrm


def get_rooms(date_from: date, date_to: date, hotel_id: int = None):
    rooms_booked = (
        select(BookingsORM.room_id, func.count("*").label("booked"))
        .select_from(BookingsORM)
        .filter(BookingsORM.date_from <= date_to, BookingsORM.date_to >= date_from)
        .group_by(BookingsORM.room_id)
        .cte(name="rooms_booked")
    )
    rooms_purches = (
        select(
            RoomsOrm.id.label("room_id"),
            (RoomsOrm.quantity - func.coalesce(rooms_booked.c.booked, 0)).label(
                "rooms_left"
            ),
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_booked, RoomsOrm.id == rooms_booked.c.room_id)
        .cte("rooms_purches")
    )
    rooms_by_hotel = select(RoomsOrm.id).select_from(RoomsOrm)
    if hotel_id:
        rooms_by_hotel = rooms_by_hotel.filter_by(hotel_id=hotel_id)
    rooms_by_hotel = rooms_by_hotel.subquery(name="rooms_id_for_hotel")
    rooms_id_avaliable = (
        select(rooms_purches.c.room_id)
        .select_from(rooms_purches)
        .filter(
            rooms_purches.c.rooms_left > 0,
            rooms_purches.c.room_id.in_(select(rooms_by_hotel)),
        )
    )
    return rooms_id_avaliable
