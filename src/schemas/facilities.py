from pydantic import BaseModel, ConfigDict


class FacilityADD(BaseModel):
    title: str


class Facility(FacilityADD):
    id: int

    model_config = ConfigDict(from_attributes=True)
