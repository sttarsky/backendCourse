import json

from httpx import AsyncClient
import pytest

from src.config import settings
from src.databases import Base, engine_null_pool, async_null_session_maker
from src.main import app
from src.models import *  # noqa
from src.schemas.hotels import HotelADD
from src.schemas.rooms import RoomADD
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
async def check_db():
    assert settings.MODE == "TEST"


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
    async with DBManager(session_factory=async_null_session_maker) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)
        await db.commit()


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
