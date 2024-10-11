from fastapi import APIRouter

from src.databases import async_session_maker
from src.repository.users import UsersRepository
from src.schemas.users import UserRequestADD, UserADD

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])


@router.post("/registration")
async def registr(data: UserRequestADD):
    hashed_pass = "1233445hdghdfg"
    new_user_data = UserADD(email=data.email,
                            surname=data.surname,
                            nickname=data.nickname,
                            hash_password=hashed_pass)
    async with async_session_maker() as session:
        await UsersRepository().add(new_user_data)
        await session.commit()
