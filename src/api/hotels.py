from fastapi import APIRouter, Query, Body
from sqlalchemy import insert, select

from src.databases import async_session_maker, engine
from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPUTCH

router = APIRouter(prefix="/hotels", tags=['Отели'])


@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels
    # if pagination.page and pagination.per_page:
    #     return _hotels[(pagination.page - 1) * pagination.per_page: pagination.per_page * pagination.page]
    # else:
    #     return _hotels


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "location": "ул. Моря, 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай У фонтана",
            "location": "ул. Шейха, 2",
        }
    }
})):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(bind=engine, compile_kwargs={'literal_binds': True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "ok"}


@router.put("/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    update_hotel: list[dict] = [hotel for hotel in hotels if hotel.get("id") == hotel_id]
    if update_hotel:
        update_hotel[0]["title"] = hotel_data.title
        update_hotel[0]["name"] = hotel_data.name
        return {"status": "ok"}
    else:
        return {"status": "error"}


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
    global hotels
    hotels = [hotel for hotel in hotels if hotel.get("id") != hotel_id]
    return {"status": "ok"}
