from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException
from src.schemas.bookings import BookingADD, BookingADDRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return bookings


@router.post("")
async def post_booking(user_id: UserIdDep, booking_data: BookingADDRequest, db: DBDep):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="No such room")
    hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingADD(
        user_id=user_id, price=room_price, **booking_data.model_dump()
    )
    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    await db.commit()
    return {"status": "ok", "booking": booking}


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()
