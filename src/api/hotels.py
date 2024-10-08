from fastapi import APIRouter, Query, Body

from src.databases import async_session_maker
from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelADD, HotelPATCH
from src.repository.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=['Отели'])


@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description='Адрес отеля'),
        title: str | None = Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    offset = per_page * (pagination.page - 1)
    async with (async_session_maker() as session):
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=offset
        )


@router.get("/{hotel_id}")
async def get_one_or_none(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        return hotel


@router.post("")
async def create_hotel(hotel_data: HotelADD = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Rich 5 звезд у моря",
            "location": "Сочи,ул. Моря, 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Relax resort у фонтана",
            "location": "Дубай, ул. Шейха, 2",
        }
    }
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def put_hotel(hotel_id: int, hotel_data: HotelADD):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
        return {"status": "ok"}


@router.patch("/{hotel_id}", summary='Частичное обновление отелей',
              description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>")
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
        return {"status": "ok"}


@router.delete("/{hotel_id}")
async def del_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
        return {"status": "ok"}
