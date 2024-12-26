from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingADD, BookingADDRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return bookings


@router.post("")
async def post_booking(user_id: UserIdDep, booking_data: BookingADDRequest, db: DBDep):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="No such room")
    room_price: int = room.price
    _booking_data = BookingADD(user_id=user_id, price=room_price, **booking_data.model_dump())
    booking = await db.bookings.add_booking(_booking_data)
    await db.commit()
    return {"status": "ok", "booking": booking}


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()
