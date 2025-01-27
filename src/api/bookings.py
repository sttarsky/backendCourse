from fastapi import APIRouter
from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsAreBookedException, RoomNotFoundException, \
    RoomNotFoundHTTPException, AllRoomsAreBookedHTTPException, DateMissmatchExeption, DateMissmatchHTTPExeption
from src.schemas.bookings import BookingADDRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("")
async def post_booking(user_id: UserIdDep, booking_data: BookingADDRequest, db: DBDep):
    try:
        booking = await BookingService(db).post_booking(user_id, booking_data)
    except DateMissmatchExeption:
        raise DateMissmatchHTTPExeption
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    return {"status": "ok", "booking": booking}


@router.get("")
async def get_all_bookings(db: DBDep):
    return await BookingService(db).get_all_bookings()
