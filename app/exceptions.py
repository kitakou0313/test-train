class AppError(Exception):
    pass


class NotFoundError(AppError):
    pass


class InvalidStatusTransitionError(AppError):
    pass


class InvalidDueDateError(AppError):
    pass


class CategoryInUseError(AppError):
    pass


class DuplicateNameError(AppError):
    pass


class InvalidColorError(AppError):
    pass
