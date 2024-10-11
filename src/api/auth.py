from fastapi import APIRouter
from passlib.context import CryptContext

from src.databases import async_session_maker
from src.repository.users import UsersRepository
from src.schemas.users import UserRequestADD, UserADD

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/registration")
async def registr(data: UserRequestADD):
    hashed_pass = pwd_context.hash(data.password)
    new_user_data = UserADD(email=data.email,
                            surname=data.surname,
                            nickname=data.nickname,
                            hashed_password=hashed_pass)
    async with async_session_maker() as session:
        check = await UsersRepository(session).get_one_or_none(email=data.email)
        if not check:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
            return {'status': 'ok'}
        else:
            await session.rollback()
            return {'status': 'user exist'}
