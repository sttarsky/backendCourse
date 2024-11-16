from pydantic import BaseModel, ConfigDict, Field

from src.schemas.hotels import Hotel


class RoomADDRequest(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int
    facilities: list[int] | None = None


class RoomADD(BaseModel):
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int


class Rooms(RoomADD):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomPATCHRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)


class RoomPATCH(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
