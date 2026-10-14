from fastapi import APIRouter, Query, Response, status

from app.api.dependencies import BoardServiceDependency, TaskServiceDependency
from app.schemas.board import BoardCreate, BoardRead
from app.schemas.common import ErrorResponse
from app.schemas.task import TaskCreate, TaskRead

router = APIRouter(prefix="/api/boards", tags=["boards"])

error_responses = {
    404: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
}


@router.get("", response_model=list[BoardRead], responses={500: {"model": ErrorResponse}})
def list_boards(service: BoardServiceDependency) -> list[BoardRead]:
    return service.list_boards()


@router.post(
    "",
    response_model=BoardRead,
    status_code=status.HTTP_201_CREATED,
    responses={422: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
def create_board(payload: BoardCreate, service: BoardServiceDependency) -> BoardRead:
    return service.create_board(payload.name)


@router.delete(
    "/{board_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=error_responses,
)
def delete_board(board_id: int, service: BoardServiceDependency) -> Response:
    service.delete_board(board_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{board_id}/tasks",
    response_model=list[TaskRead],
    responses=error_responses,
)
def list_tasks(
    board_id: int,
    service: TaskServiceDependency,
    task_status: str | None = Query(default=None, alias="status"),
) -> list[TaskRead]:
    return service.list_tasks(board_id, task_status)


@router.post(
    "/{board_id}/tasks",
    response_model=TaskRead,
    status_code=status.HTTP_201_CREATED,
    responses=error_responses,
)
def create_task(
    board_id: int,
    payload: TaskCreate,
    service: TaskServiceDependency,
) -> TaskRead:
    return service.create_task(board_id, payload.title, payload.description)

