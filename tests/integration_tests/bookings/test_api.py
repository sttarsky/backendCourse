import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code",
                         [(1, '2025-01-26', '2025-01-27', 200),
                          (1, '2025-01-26', '2025-01-27', 200),
                          (1, '2025-01-26', '2025-01-27', 200),
                          (1, '2025-01-26', '2025-01-27', 200),
                          (1, '2025-01-26', '2025-01-27', 200),
                          (1, '2025-01-26', '2025-01-27', 500)])
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
