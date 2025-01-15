from fastapi import HTTPException


class ProjectBaseException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(ProjectBaseException):
    detail = "Object not found"


class ObjectAlreadyExistException(ProjectBaseException):
    detail = "Object already exists"


class AllRoomsAreBookedException(ProjectBaseException):
    detail = "No free rooms"


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
