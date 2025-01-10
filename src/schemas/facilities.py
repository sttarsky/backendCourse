from pydantic import BaseModel


class FacilityADD(BaseModel):
    title: str


class Facility(FacilityADD):
    id: int


class RoomFacilityADD(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityADD):
    id: int
