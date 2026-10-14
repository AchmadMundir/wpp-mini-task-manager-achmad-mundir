class AppError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int,
        field: str | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.field = field


class ValidationError(AppError):
    def __init__(self, message: str, field: str | None = None) -> None:
        super().__init__("VALIDATION_FAILED", message, 422, field)


class NotFoundError(AppError):
    def __init__(self, resource: str, resource_id: int) -> None:
        super().__init__(
            "NOT_FOUND",
            f"{resource} with id {resource_id} was not found",
            404,
        )

