from typing import Protocol

from app.models.board import Board
from app.models.task import Task, TaskStatus


class BoardRepository(Protocol):
    def list_all(self) -> list[Board]: ...

    def get(self, board_id: int) -> Board | None: ...

    def create(self, name: str) -> Board: ...

    def delete(self, board: Board) -> None: ...


class TaskRepository(Protocol):
    def list_by_board(
        self, board_id: int, status: TaskStatus | None = None
    ) -> list[Task]: ...

    def get(self, task_id: int) -> Task | None: ...

    def create(
        self, board_id: int, title: str, description: str | None
    ) -> Task: ...

    def update_status(self, task: Task, status: TaskStatus) -> Task: ...

    def delete(self, task: Task) -> None: ...

