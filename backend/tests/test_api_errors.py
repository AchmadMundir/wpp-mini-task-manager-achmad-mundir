from fastapi.testclient import TestClient

from app.api.dependencies import get_board_service, get_task_service
from app.main import app
from app.services.board_service import BoardService
from app.services.task_service import TaskService
from tests.fakes import FakeBoardRepository, FakeTaskRepository, make_board


def test_api_uses_consistent_validation_error_shape() -> None:
    app.dependency_overrides[get_board_service] = lambda: BoardService(
        FakeBoardRepository()
    )
    client = TestClient(app, raise_server_exceptions=False)

    response = client.post("/api/boards", json={"name": "   "})

    assert response.status_code == 422
    assert response.json()["error"] == "VALIDATION_FAILED"
    assert response.json()["field"] == "name"
    app.dependency_overrides.clear()


def test_api_returns_404_for_task_on_missing_board() -> None:
    app.dependency_overrides[get_task_service] = lambda: TaskService(
        FakeBoardRepository(), FakeTaskRepository()
    )
    client = TestClient(app, raise_server_exceptions=False)

    response = client.post("/api/boards/999/tasks", json={"title": "Task"})

    assert response.status_code == 404
    assert response.json() == {
        "error": "NOT_FOUND",
        "message": "Board with id 999 was not found",
    }
    app.dependency_overrides.clear()


def test_api_returns_201_and_default_status() -> None:
    boards = FakeBoardRepository([make_board()])
    app.dependency_overrides[get_task_service] = lambda: TaskService(
        boards, FakeTaskRepository()
    )
    client = TestClient(app, raise_server_exceptions=False)

    response = client.post("/api/boards/1/tasks", json={"title": "Task"})

    assert response.status_code == 201
    assert response.json()["status"] == "TODO"
    app.dependency_overrides.clear()

