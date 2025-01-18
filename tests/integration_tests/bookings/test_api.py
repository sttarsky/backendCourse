import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize("room_id, date_from, date_to, status_code",
                         [(1, '2025-01-26', '2025-01-27', 200),
                          (1, '2025-01-26', '2025-01-27', 200),
                          (1, '2025-01-26', '2025-01-27', 200),
                          (1, '2025-01-26', '2025-01-27', 200),
                          (1, '2025-01-26', '2025-01-27', 200),
                          (1, '2025-01-26', '2025-01-27', 409)])
async def test_add_booking(db, authenticated_ac, room_id, date_from, date_to, status_code):
    result = await authenticated_ac.post("/bookings",
                                         json={
                                             "room_id": room_id,
                                             "date_from": date_from,
                                             "date_to": date_to,
                                         })

    assert result.status_code == status_code
    if result.status_code == 200:
        res = result.json()
        assert isinstance(res, dict)
        assert res["status"] == "ok"
        assert "booking" in res


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize("room_id, date_from, date_to, status_code, count", [
    (1, '2025-01-26', '2025-01-27', 200, 1),
    (1, '2025-01-26', '2025-01-30', 200, 2),
    (1, '2025-01-26', '2025-02-27', 200, 3),
])
async def test_add_and_get_bookings(
        room_id,
        date_from,
        date_to,
        status_code,
        count,
        delete_all_bookings,
        authenticated_ac,):
    result = await authenticated_ac.post("/bookings",
                                         json={
                                             "room_id": room_id,
                                             "date_from": date_from,
                                             "date_to": date_to,
                                         })
    assert result.status_code == 200
    result = await authenticated_ac.get("/bookings/me")
    assert isinstance(result.json(), list)
    assert len(result.json()) == count
