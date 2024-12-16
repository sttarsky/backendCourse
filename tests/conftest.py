from httpx import AsyncClient
import pytest

from src.config import settings
from src.databases import Base, engine_null_pool
from src.main import app
from src.models import *  # noqa


@pytest.fixture(scope="session", autouse=True)
async def check_db():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_db):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        result = await ac.post(
            "/auth/registration",
            json={
                "email": "kot@pes.com",
                "password": "1234",
                "nickname": "Kot",
                "surname": "Kotov"

            }
        )
        print(result)