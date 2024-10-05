from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    location: str


class HotelPUTCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
