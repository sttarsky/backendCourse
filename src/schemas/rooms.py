from pydantic import BaseModel, ConfigDict, Field
from src.schemas.hotels import Hotel


class RoomADD(BaseModel):
    hotel_id: Hotel
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int


class Rooms(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPATCH(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
