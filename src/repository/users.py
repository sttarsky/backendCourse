from pydantic import EmailStr
from sqlalchemy.exc import NoResultFound

from src.exceptions import UserNotExist
from src.models.users import UsersORM
from src.repository.base import BaseRepository
from src.repository.mappers.mappers import UserMapper
from src.schemas.users import UserWithHashedPass
from sqlalchemy import select


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserMapper

    async def get_user_with_hashed_pass(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
            return UserWithHashedPass.model_validate(model)
        except NoResultFound:
            raise UserNotExist
