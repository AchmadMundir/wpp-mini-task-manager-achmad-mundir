import pytest

from app.core.errors import NotFoundError, ValidationError
from app.services.board_service import BoardService
from tests.fakes import FakeBoardRepository, make_board


def test_create_board_trims_name() -> None:
    repository = FakeBoardRepository()
    service = BoardService(repository)

    board = service.create_board("  Onboarding  ")

    assert board.name == "Onboarding"
    assert repository.get(board.id) is board


@pytest.mark.parametrize("name", ["", "   ", "\t\n"])
def test_create_board_rejects_empty_or_whitespace_name(name: str) -> None:
    service = BoardService(FakeBoardRepository())

    with pytest.raises(ValidationError) as error:
        service.create_board(name)

    assert error.value.code == "VALIDATION_FAILED"
    assert error.value.field == "name"


def test_delete_board_removes_existing_board() -> None:
    board = make_board()
    repository = FakeBoardRepository([board])
    service = BoardService(repository)

    service.delete_board(board.id)

    assert repository.get(board.id) is None


def test_delete_board_rejects_unknown_id() -> None:
    service = BoardService(FakeBoardRepository())

    with pytest.raises(NotFoundError) as error:
        service.delete_board(999)

    assert error.value.status_code == 404

