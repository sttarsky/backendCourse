# ruff: noqa: E402
import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from httpx import AsyncClient
import pytest

from src.api.dependencies import get_db
from src.config import settings
from src.databases import Base, engine_null_pool, async_null_session_maker
from src.main import app
from src.models import *  # noqa
from src.schemas.hotels import HotelADD
from src.schemas.rooms import RoomADD
from src.utils.db_manager import DBManager


async def get_db_null_pool():
    async with DBManager(session_factory=async_null_session_maker) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def check_db():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_db):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def create_hotels_rooms(setup_database):
    mock_hotels = "tests/mock_hotels.json"
    mock_rooms = "tests/mock_rooms.json"
    with open(mock_hotels, 'r') as file:
        hotels_to_incert = json.load(file)
    with open(mock_rooms, 'r') as file:
        rooms_to_incert = json.load(file)
    hotels = [HotelADD.model_validate(hotel) for hotel in hotels_to_incert]
    rooms = [RoomADD.model_validate(room) for room in rooms_to_incert]
    async with DBManager(session_factory=async_null_session_maker) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/registration",
        json={
            "email": "kot@pes.com",
            "password": "1234",
            "nickname": "Kot",
            "surname": "Kotov"

        }
    )


@pytest.fixture(scope="session", autouse=True)
async def authenticated_ac(ac, register_user):
    await ac.post(
        "/auth/login",
        json={
            "email": "kot@pes.com",
            "password": "1234"
        }
    )
    assert ac.cookies["access_token"]
    yield ac
