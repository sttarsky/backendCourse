from fastapi import APIRouter, HTTPException, Response
from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ObjectAlreadyExistException, EmailNotRegisteredException, EmailNotRegisteredHTTPException, \
    IncorrectPasswordHTTPException, IncorrectPasswordException, UserAlreadyExistException, \
    UserEmailAlreadyExistHTTPException
from src.schemas.users import UserRequestADD, UserADD, UserRequest
from src.services.auth import AuthServices

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/login")
async def login_user(data: UserRequest, response: Response, db: DBDep):
    try:
        access_token = await AuthServices(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token}


@router.post("/registration")
async def registr(data: UserRequestADD, db: DBDep):
    try:
        await AuthServices(db).register_user(data)
        return {"status": "OK"}
    except UserAlreadyExistException:
        raise UserEmailAlreadyExistHTTPException


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await AuthServices(db).get_one_or_none_user(user_id)


@router.post("/logout")
async def get_logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"detail": "Successfully logged out"}
