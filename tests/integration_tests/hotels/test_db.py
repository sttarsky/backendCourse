from src.databases import async_session_maker
from src.schemas.hotels import HotelADD
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotels_data = HotelADD(title='5 Stars Hotel Resort', location='Краснодар')
    async with DBManager(async_session_maker) as db:
        new_hotel_data = await db.hotels.add(hotels_data)
        print(f"{new_hotel_data=}")
    ...
