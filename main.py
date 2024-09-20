import asyncio
import threading
import time

import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]


@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync. Потоков: {threading.active_count()}")
    print(f"sync. Начал {id}: {time.time():.2f}")
    time.sleep(3)
    print(f"sync. Закончил {id}: {time.time():.2f}")


@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async. Потоков: {threading.active_count()}")
    print(f"async. Начал {id}: {time.time():.2f}")
    await asyncio.sleep(3)
    print(f"async. Закончил {id}: {time.time():.2f}")

@app.get('/hotels')
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    _hotels = []
    for hotel in hotels:
        if id and hotel.get("id") != id:
            continue
        if title and hotel.get("title") != title:
            continue
        _hotels.append(hotel)

    return _hotels


@app.post("/hotels")
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append(
        {"id": hotels[-1]["id"] + 1,
         "titel": title}
    )
    return {"status": "ok"}


@app.put("/hotels/{hotel_id}")
def put_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    global hotels
    update_hotel: list[dict] = [hotel for hotel in hotels if hotel.get("id") == hotel_id]
    if update_hotel:
        update_hotel[0]["title"] = title
        update_hotel[0]["name"] = name
        return {"status": "ok"}
    else:
        return {"status": "error"}


@app.patch("/hotels/{hotel_id}")
def patch_hotel(hotel_id: int, title: str | None = Body(), name: str | None = Body()):
    if title and name:
        return put_hotel(hotel_id, title, name)
    else:
        global hotels
        for hotel in hotels:
            if hotel.get("id") == hotel_id:
                if title:
                    hotel["title"] = title
                if name:
                    hotel["name"] = name
                return {"status": "ok"}
            else:
                return {"status": "error"}


@app.delete("/hotels/{hotel_id}")
def del_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel.get("id") != hotel_id]
    return {"status": "ok"}


# @app.get('/')
# def func():
#     return "Hello, World!!!!!!!"


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
