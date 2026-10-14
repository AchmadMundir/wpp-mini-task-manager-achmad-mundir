from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.board import Board
from app.models.task import Task, TaskStatus


class SQLAlchemyBoardRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[Board]:
        statement = select(Board).order_by(Board.created_at.asc(), Board.id.asc())
        return list(self.db.scalars(statement).all())

    def get(self, board_id: int) -> Board | None:
        return self.db.get(Board, board_id)

    def create(self, name: str) -> Board:
        board = Board(name=name)
        self.db.add(board)
        self.db.commit()
        self.db.refresh(board)
        return board

    def delete(self, board: Board) -> None:
        self.db.delete(board)
        self.db.commit()


class SQLAlchemyTaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_by_board(
        self, board_id: int, status: TaskStatus | None = None
    ) -> list[Task]:
        statement = select(Task).where(Task.board_id == board_id)
        if status is not None:
            statement = statement.where(Task.status == status.value)
        statement = statement.order_by(Task.created_at.asc(), Task.id.asc())
        return list(self.db.scalars(statement).all())

    def get(self, task_id: int) -> Task | None:
        return self.db.get(Task, task_id)

    def create(self, board_id: int, title: str, description: str | None) -> Task:
        task = Task(
            board_id=board_id,
            title=title,
            description=description,
            status=TaskStatus.TODO.value,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update_status(self, task: Task, status: TaskStatus) -> Task:
        task.status = status.value
        task.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()

