from fastapi import APIRouter, HTTPException, Response, Request

from src.api.dependencies import UserIdDep
from src.databases import async_session_maker
from src.repository.users import UsersRepository
from src.schemas.users import UserRequestADD, UserADD, UserRequest
from src.services.auth import AuthServices

router = APIRouter(prefix='/auth', tags=['Авторизация и аутентификация'])


@router.post("/login")
async def login_user(data: UserRequest,
                     response: Response):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_pass(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail='No such user')
        if not AuthServices().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='Incorrect password')
        access_token = AuthServices().create_access_token({'id': user.id})
        response.set_cookie(key='access_token', value=access_token)
        return {'access_token': access_token}


@router.post("/registration")
async def registr(data: UserRequestADD):
    hashed_pass = AuthServices().hash_password(data.password)
    new_user_data = UserADD(email=data.email,
                            surname=data.surname,
                            nickname=data.nickname,
                            hashed_password=hashed_pass)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
        return {'status': 'ok'}


@router.get("/me")
async def get_me(
        user_id: UserIdDep
):
    async with async_session_maker() as session:
        result = await UsersRepository(session).get_one_or_none(id=user_id)
        return result


@router.post('/logout')
async def get_logout(
        response: Response
):
    print(response)
    response.delete_cookie(key='access_token')
    return {"detail": "Successfully logged out"}
