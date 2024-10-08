from distutils.util import execute

from fastapi import APIRouter, Query, Body
from sqlalchemy import insert

from src.databases import async_session_maker, engine
from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPUTCH
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


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
async def put_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        update_hotel = HotelsRepository.edit(session, hotel_data)
        session.commit()
        return {"status": "ok"}


@router.patch("/{hotel_id}", summary='Частичное обновление отелей',
              description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>")
def patch_hotel(hotel_id: int, hotel_data: HotelPUTCH):
    if hotel_data.title and hotel_data.name:
        return put_hotel(hotel_id, hotel_data.title, hotel_data.name)
    else:
        global hotels
        for hotel in hotels:
            if hotel.get("id") == hotel_id:
                if hotel_data.title:
                    hotel["title"] = hotel_data.title
                if hotel_data.name:
                    hotel["name"] = hotel_data.name
                return {"status": "ok"}
            else:
                return {"status": "error"}


@router.delete("/{hotel_id}")
def del_hotel(hotel_id: int):
    async with async_session_maker() as session:
        update_hotel = HotelsRepository.delete(session, hotel_id)
        session.commit()
        return {"status": "ok"}
