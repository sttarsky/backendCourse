import pytest


@pytest.mark.parametrize("email, password, nickname, surname, status_code", [
    ("test@test.ru", "123456", "Test", "Test2", 200),
    ("test@test.ru", "123456", "Test", "Test2", 409)
])
async def test_full_auth(email, password, nickname, surname, status_code, ac):
    result_registration = await ac.post("/auth/registration",
                                        json={
                                            "email": email,
                                            "password": password,
                                            "nickname": nickname,
                                            "surname": surname,
                                        })
    assert result_registration.status_code == status_code
    if status_code != 200:
        return
    result_login = await ac.post("/auth/login",
                                 json={
                                     "email": email,
                                     "password": password,
                                 })
    assert result_login.status_code == status_code
    assert ac.cookies["access_token"]
    assert "access_token" in result_login.json()

    user_result = await ac.get("/auth/me")
    assert user_result.status_code == status_code
    assert user_result.json().get("email") == email

    await ac.post("/auth/logout")
    assert ac.cookies.get("access_token") is None
