from datetime import datetime, timezone

from app.models.board import Board
from app.models.task import Task, TaskStatus


class FakeBoardRepository:
    def __init__(self, boards: list[Board] | None = None) -> None:
        self.items = {board.id: board for board in boards or []}
        self.next_id = max(self.items, default=0) + 1

    def list_all(self) -> list[Board]:
        return list(self.items.values())

    def get(self, board_id: int) -> Board | None:
        return self.items.get(board_id)

    def create(self, name: str) -> Board:
        board = Board(id=self.next_id, name=name, created_at=datetime.now(timezone.utc))
        self.items[board.id] = board
        self.next_id += 1
        return board

    def delete(self, board: Board) -> None:
        del self.items[board.id]


class FakeTaskRepository:
    def __init__(self, tasks: list[Task] | None = None) -> None:
        self.items = {task.id: task for task in tasks or []}
        self.next_id = max(self.items, default=0) + 1

    def list_by_board(
        self, board_id: int, status: TaskStatus | None = None
    ) -> list[Task]:
        tasks = [task for task in self.items.values() if task.board_id == board_id]
        if status is not None:
            tasks = [task for task in tasks if task.status == status.value]
        return tasks

    def get(self, task_id: int) -> Task | None:
        return self.items.get(task_id)

    def create(self, board_id: int, title: str, description: str | None) -> Task:
        now = datetime.now(timezone.utc)
        task = Task(
            id=self.next_id,
            board_id=board_id,
            title=title,
            description=description,
            status=TaskStatus.TODO.value,
            created_at=now,
            updated_at=now,
        )
        self.items[task.id] = task
        self.next_id += 1
        return task

    def update_status(self, task: Task, status: TaskStatus) -> Task:
        task.status = status.value
        task.updated_at = datetime.now(timezone.utc)
        return task

    def delete(self, task: Task) -> None:
        del self.items[task.id]


def make_board(board_id: int = 1, name: str = "Board") -> Board:
    return Board(id=board_id, name=name, created_at=datetime.now(timezone.utc))


def make_task(
    task_id: int = 1,
    board_id: int = 1,
    status: str = TaskStatus.TODO.value,
) -> Task:
    now = datetime.now(timezone.utc)
    return Task(
        id=task_id,
        board_id=board_id,
        title=f"Task {task_id}",
        description=None,
        status=status,
        created_at=now,
        updated_at=now,
    )

