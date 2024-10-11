from pydantic import BaseModel, ConfigDict


class UserRequestADD(BaseModel):
    email: str
    password: str
    nickname: str
    surname: str


class UserADD(BaseModel):
    email: str
    hash_password: str
    nickname: str
    surname: str


class User(BaseModel):
    id: int
    email: str
    nickname: str

    model_config = ConfigDict(from_attributes=True)
