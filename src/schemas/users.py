from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequest(BaseModel):
    email: EmailStr
    password: str


class UserRequestADD(UserRequest):
    nickname: str
    surname: str


class UserADD(BaseModel):
    email: EmailStr
    hashed_password: str
    nickname: str
    surname: str


class User(BaseModel):
    id: int
    email: EmailStr
    nickname: str

    model_config = ConfigDict(from_attributes=True)
