from app.core.errors import NotFoundError, ValidationError
from app.models.task import Task, TaskStatus
from app.repositories.interfaces import BoardRepository, TaskRepository


class TaskService:
    def __init__(
        self,
        boards: BoardRepository,
        tasks: TaskRepository,
    ) -> None:
        self.boards = boards
        self.tasks = tasks

    def _require_board(self, board_id: int) -> None:
        if self.boards.get(board_id) is None:
            raise NotFoundError("Board", board_id)

    @staticmethod
    def _parse_status(status: str | None) -> TaskStatus | None:
        if status is None:
            return None
        try:
            return TaskStatus(status)
        except ValueError as exc:
            allowed = ", ".join(item.value for item in TaskStatus)
            raise ValidationError(
                f"status must be one of: {allowed}", "status"
            ) from exc

    def list_tasks(self, board_id: int, status: str | None = None) -> list[Task]:
        self._require_board(board_id)
        parsed_status = self._parse_status(status)
        return self.tasks.list_by_board(board_id, parsed_status)

    def create_task(
        self,
        board_id: int,
        title: str,
        description: str | None = None,
    ) -> Task:
        self._require_board(board_id)
        cleaned_title = title.strip()
        if not cleaned_title:
            raise ValidationError("title must not be empty", "title")
        cleaned_description = description.strip() if description else None
        return self.tasks.create(board_id, cleaned_title, cleaned_description or None)

    def update_status(self, task_id: int, status: str) -> Task:
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task", task_id)
        parsed_status = self._parse_status(status)
        assert parsed_status is not None
        return self.tasks.update_status(task, parsed_status)

    def delete_task(self, task_id: int) -> None:
        task = self.tasks.get(task_id)
        if task is None:
            raise NotFoundError("Task", task_id)
        self.tasks.delete(task)

