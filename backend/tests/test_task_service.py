import pytest

from app.core.errors import NotFoundError, ValidationError
from app.models.task import TaskStatus
from app.services.task_service import TaskService
from tests.fakes import (
    FakeBoardRepository,
    FakeTaskRepository,
    make_board,
    make_task,
)


def create_service(tasks=None) -> TaskService:
    return TaskService(
        FakeBoardRepository([make_board()]),
        FakeTaskRepository(tasks),
    )


def test_create_task_on_existing_board_defaults_to_todo() -> None:
    service = create_service()

    task = service.create_task(1, "  Draft report  ", "  Q3 results  ")

    assert task.board_id == 1
    assert task.title == "Draft report"
    assert task.description == "Q3 results"
    assert task.status == TaskStatus.TODO.value


@pytest.mark.parametrize("title", ["", "   ", "\t\n"])
def test_create_task_rejects_empty_or_whitespace_title(title: str) -> None:
    service = create_service()

    with pytest.raises(ValidationError) as error:
        service.create_task(1, title)

    assert error.value.field == "title"


def test_create_task_rejects_unknown_board() -> None:
    service = TaskService(FakeBoardRepository(), FakeTaskRepository())

    with pytest.raises(NotFoundError) as error:
        service.create_task(999, "Task")

    assert error.value.message == "Board with id 999 was not found"


def test_filter_tasks_by_status() -> None:
    tasks = [
        make_task(1, status=TaskStatus.TODO.value),
        make_task(2, status=TaskStatus.DONE.value),
        make_task(3, status=TaskStatus.DONE.value),
    ]
    service = create_service(tasks)

    result = service.list_tasks(1, TaskStatus.DONE.value)

    assert [task.id for task in result] == [2, 3]
    assert all(task.status == TaskStatus.DONE.value for task in result)


def test_filter_tasks_rejects_invalid_status() -> None:
    service = create_service()

    with pytest.raises(ValidationError) as error:
        service.list_tasks(1, "BLOCKED")

    assert error.value.field == "status"


def test_update_task_status() -> None:
    task = make_task()
    service = create_service([task])

    updated = service.update_status(task.id, TaskStatus.IN_PROGRESS.value)

    assert updated.status == TaskStatus.IN_PROGRESS.value


def test_update_task_rejects_invalid_status() -> None:
    service = create_service([make_task()])

    with pytest.raises(ValidationError) as error:
        service.update_status(1, "BLOCKED")

    assert error.value.code == "VALIDATION_FAILED"
    assert error.value.field == "status"


def test_update_unknown_task_returns_not_found() -> None:
    service = create_service()

    with pytest.raises(NotFoundError) as error:
        service.update_status(999, TaskStatus.DONE.value)

    assert error.value.status_code == 404


def test_delete_task() -> None:
    task = make_task()
    task_repository = FakeTaskRepository([task])
    service = TaskService(FakeBoardRepository([make_board()]), task_repository)

    service.delete_task(task.id)

    assert task_repository.get(task.id) is None


def test_delete_unknown_task_returns_not_found() -> None:
    service = create_service()

    with pytest.raises(NotFoundError) as error:
        service.delete_task(999)

    assert error.value.status_code == 404

