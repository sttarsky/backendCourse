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
        price=randint(100, 2000)
    )
    assert await db.bookings.add(booking)
    booking.date_to = date.today() + timedelta(days=randint(15, 25))
    await db.bookings.edit(data=booking, exclude_unset=True)
    print(f"booking={booking.model_dump()}")
    assert await db.bookings.get_one_or_none(**booking.model_dump())
    await db.bookings.delete(**booking.model_dump())
    assert (await db.bookings.get_one_or_none(**booking.model_dump())) is None
