from pydantic import BaseModel


class DataMapper:
    db_model = None
    schema: BaseModel = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data: BaseModel):
        return cls.db_model(**data.model_dump())
