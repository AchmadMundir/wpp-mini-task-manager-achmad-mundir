from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.sqlalchemy import (
    SQLAlchemyBoardRepository,
    SQLAlchemyTaskRepository,
)
from app.services.board_service import BoardService
from app.services.task_service import TaskService

DbSession = Annotated[Session, Depends(get_db)]


def get_board_service(db: DbSession) -> BoardService:
    return BoardService(SQLAlchemyBoardRepository(db))


def get_task_service(db: DbSession) -> TaskService:
    return TaskService(
        SQLAlchemyBoardRepository(db),
        SQLAlchemyTaskRepository(db),
    )

BoardServiceDependency = Annotated[BoardService, Depends(get_board_service)]
TaskServiceDependency = Annotated[TaskService, Depends(get_task_service)]

