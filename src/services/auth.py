from datetime import timezone, datetime, timedelta

from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
from src.config import settings
from src.exceptions import EmailNotRegisteredException, IncorrectPasswordException, ObjectAlreadyExistException, \
    UserAlreadyExistException, IncorrectTokenHTTPException
from src.schemas.users import UserRequest, UserRequestADD, UserADD
from src.services.base import BaseService


class AuthServices(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenHTTPException
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def login_user(self, data: UserRequest):
        user = await self.db.users.get_user_with_hashed_pass(email=data.email)
        if not user:
            raise EmailNotRegisteredException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    async def register_user(self, data: UserRequestADD):
        hashed_pass = self.hash_password(data.password)
        new_user_data = UserADD(
            email=data.email,
            surname=data.surname,
            nickname=data.nickname,
            hashed_password=hashed_pass,
        )
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
            return {"status": "ok"}
        except ObjectAlreadyExistException as ex:
            raise UserAlreadyExistException from ex

    async def get_one_or_none_user(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)
