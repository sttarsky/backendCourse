from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingADDRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingADD(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int


class Booking(BookingADD):
    id: int