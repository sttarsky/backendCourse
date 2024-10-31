from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingADD, Booking

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def post_booking(user_id: UserIdDep, booking: BookingADD, db: DBDep):
    user_id = await db.users.get_one_or_none(id=user_id)
    room = await db.rooms.get_one_or_none(id=booking.room_id)
    if not room:
        raise HTTPException(status_code=400, detail="No such room")
    _booking = Booking(user_id=user_id.id, **booking.model_dump())
    db.bookings.add(_booking)
    db.commit()
