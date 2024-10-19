from datetime import timezone, datetime, timedelta
from os import access

from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
import jwt

from src.databases import async_session_maker
from src.repository.users import UsersRepository
from src.schemas.users import UserRequestADD, UserADD, UserRequest

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/login")
async def login_user(data: UserRequest):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail='No such user')
        access_token = create_access_token({'id': user.id})
        return {'access_token': access_token}


@router.post("/registration")
async def registr(data: UserRequestADD):
    hashed_pass = pwd_context.hash(data.password)
    new_user_data = UserADD(email=data.email,
                            surname=data.surname,
                            nickname=data.nickname,
                            hashed_password=hashed_pass)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
        return {'status': 'ok'}
