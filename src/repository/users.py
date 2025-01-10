from pydantic import EmailStr

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
        model = result.scalars().one_or_none()
        if not model:
            return None
        return UserWithHashedPass.model_validate(model)
