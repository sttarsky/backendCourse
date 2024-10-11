from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestADD(BaseModel):
    email: EmailStr
    password: str
    nickname: str
    surname: str


class UserADD(BaseModel):
    email: EmailStr
    hash_password: str
    nickname: str
    surname: str


class User(BaseModel):
    id: int
    email: EmailStr
    nickname: str

    model_config = ConfigDict(from_attributes=True)
