from datetime import datetime

from pydantic import BaseModel


class BookingADD(BaseModel):
    room_id: int
    date_from: datetime
    date_to: datetime


class Booking(BookingADD):
    user_id: int
    price: int
