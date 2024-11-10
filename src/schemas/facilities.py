from pydantic import BaseModel, ConfigDict


class FacilitiesADD(BaseModel):
    title: str


class Facilities(FacilitiesADD):
    id: int

    model_config = ConfigDict(from_attributes=True)
