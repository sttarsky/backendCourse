class ProjectBaseException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(ProjectBaseException):
    detail = "Object not found"


class AllRoomsAreBookedException(ProjectBaseException):
    detail = "No free rooms"


class UserNotExist(ProjectBaseException):
    detail = "No such user"
