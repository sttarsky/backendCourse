from datetime import date
from random import randint

from asyncpg.pgproto.pgproto import timedelta

from src.schemas.bookings import BookingADD


async def test_add_hotel(db):
    user = (await db.users.get_all())[0].id
    room = (await db.rooms.get_all())[0].id
    booking = BookingADD(
        user_id=user,
        room_id=room,
        date_from=date.today(),
        date_to=date.today() + timedelta(days=1),
        price=randint(100, 2000)
    )
    new_booking = await db.bookings.add(booking)
    await db.commit()
    print(f"{new_booking=}")
