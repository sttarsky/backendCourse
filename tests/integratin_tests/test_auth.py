from src.services.auth import AuthServices


def test_create_and_decode_access_token():
    data = {"user_id": 1}
    jwt_token = AuthServices().create_access_token(data)

    assert jwt_token
    assert isinstance(jwt_token, str)

    payload = AuthServices().decode_token(jwt_token)

    assert payload
    assert payload.get("user_id") == data.get("user_id")
