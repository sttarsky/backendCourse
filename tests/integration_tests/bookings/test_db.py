from datetime import date
from random import randint

from asyncpg.pgproto.pgproto import timedelta

from src.schemas.bookings import BookingADD


async def test_booking_crud(db):
    user = (await db.users.get_all())[0].id
    room = (await db.rooms.get_all())[0].id
    booking = BookingADD(
        user_id=user,
        room_id=room,
        date_from=date.today(),
        date_to=date.today() + timedelta(days=1),
        price=randint(100, 2000),
    )
    new_booking = await db.bookings.add(booking)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.user_id == new_booking.user_id
    assert booking.room_id == new_booking.room_id
    booking.date_to = date.today() + timedelta(days=randint(15, 25))
    #
    await db.bookings.edit(id=booking.id, data=booking)
    assert await db.bookings.get_one_or_none(**booking.model_dump())
    await db.bookings.delete(**booking.model_dump())
    assert (await db.bookings.get_one_or_none(**booking.model_dump())) is None
