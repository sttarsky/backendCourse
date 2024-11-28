from typing import TypeVar
from pydantic import BaseModel

from src.databases import Base

SchemaType = TypeVar('SchemaType', bound=BaseModel)
ModelType = TypeVar('ModelType', bound=Base)


class DataMapper:
    db_model: type[ModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: BaseModel):
        return cls.db_model(**data.model_dump())
