from datetime import timezone, datetime, timedelta

from fastapi import HTTPException
from passlib.context import CryptContext
import jwt

from src.config import settings


class AuthServices:
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
            raise HTTPException(status_code=401, detail="Wrong token")
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="token expired")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)
