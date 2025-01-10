from src.schemas.hotels import HotelADD


async def test_add_hotel(db):
    hotels_data = HotelADD(title='5 Stars Hotel Resort', location='Краснодар')
    await db.hotels.add(hotels_data)
    await db.commit()
