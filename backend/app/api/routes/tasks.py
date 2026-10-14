from fastapi import APIRouter, Response, status

from app.api.dependencies import TaskServiceDependency
from app.schemas.common import ErrorResponse
from app.schemas.task import TaskRead, TaskStatusUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

error_responses = {
    404: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
    500: {"model": ErrorResponse},
}


@router.patch(
    "/{task_id}",
    response_model=TaskRead,
    responses=error_responses,
)
def update_task_status(
    task_id: int,
    payload: TaskStatusUpdate,
    service: TaskServiceDependency,
) -> TaskRead:
    return service.update_status(task_id, payload.status)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=error_responses,
)
def delete_task(task_id: int, service: TaskServiceDependency) -> Response:
    service.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

