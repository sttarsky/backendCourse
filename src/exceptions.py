from fastapi import HTTPException


class ProjectBaseException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(ProjectBaseException):
    detail = "Object not found"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Room not found"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Hotel not found"


class ObjectAlreadyExistException(ProjectBaseException):
    detail = "Object already exists"


class AllRoomsAreBookedException(ProjectBaseException):
    detail = "No free rooms"


class EmailNotRegisteredException(ProjectBaseException):
    detail = "Wrong email or pass"


class IncorrectPasswordException(ProjectBaseException):
    detail = "Wrong email or pass"


class IncorrectTokenException(ProjectBaseException):
    detail = "Incorrect token"


class DateMissmatchExeption(ProjectBaseException):
    detail = "Incorrect date"


class UserAlreadyExistException(ProjectBaseException):
    detail = "User already exist"


def check_dates(date_from, date_to) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Date from can't be date to")


class ProjectHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(ProjectHTTPException):
    status_code = 404
    detail = "Hotel not found"


class RoomNotFoundHTTPException(ProjectHTTPException):
    status_code = 404
    detail = "Room not found"


class EmailNotRegisteredHTTPException(ProjectHTTPException):
    status_code = 409
    detail = "Wrong email or password"


class AllRoomsAreBookedHTTPException(ProjectHTTPException):
    status_code = 409
    detail = "No free rooms"


class IncorrectPasswordHTTPException(ProjectHTTPException):
    status_code = 401
    detail = "Wrong email or password"


class UserEmailAlreadyExistHTTPException(ProjectHTTPException):
    status_code = 409
    detail = "User already exist"


class NoAccessTokenHTTPException(ProjectHTTPException):
    status_code = 401
    detail = "Unauthorized"


class IncorrectTokenHTTPException(ProjectHTTPException):
    status_code = 401
    detail = "Incorrect token"


class DateMissmatchHTTPExeption(ProjectHTTPException):
    status_code = 400
    detail = "Incorrect date"
