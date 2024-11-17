from pydantic import BaseModel, ConfigDict, Field

from src.schemas.facilities import Facility


class RoomADDRequest(BaseModel):
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int
    facilities: list[int] = Field(default_factory=list)


class RoomADD(BaseModel):
    hotel_id: int
    title: str
    description: str | None = Field(None)
    price: int
    quantity: int


class Rooms(RoomADD):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RoomWithRels(Rooms):
    facilities: list[Facility]


class RoomPATCHRequest(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
    facilities_ids: list[int] | None = Field(None)


class RoomPATCH(BaseModel):
    hotel_id: int | None = Field(None)
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)
