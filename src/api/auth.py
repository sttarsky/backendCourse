from fastapi import APIRouter, HTTPException, Response
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import UserNotExist
from src.schemas.users import UserRequestADD, UserADD, UserRequest
from src.services.auth import AuthServices

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/login")
async def login_user(data: UserRequest, response: Response, db: DBDep):
    try:
        user = await db.users.get_user_with_hashed_pass(email=data.email)
    except UserNotExist as ex:
        raise HTTPException(status_code=401, detail=ex.detail)
    if not AuthServices().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    access_token = AuthServices().create_access_token({"id": user.id})
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token}


@router.post("/registration")
async def registr(data: UserRequestADD, db: DBDep):
    hashed_pass = AuthServices().hash_password(data.password)
    new_user_data = UserADD(
        email=data.email,
        surname=data.surname,
        nickname=data.nickname,
        hashed_password=hashed_pass,
    )
    try:
        await db.users.add(new_user_data)
        await db.commit()
        return {"status": "ok"}
    except IntegrityError:
        raise HTTPException(409, detail="User already exist")


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    result = await db.users.get_one_or_none(id=user_id)
    return result


@router.post("/logout")
async def get_logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"detail": "Successfully logged out"}
