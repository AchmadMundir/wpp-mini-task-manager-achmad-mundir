from app.core.errors import NotFoundError, ValidationError
from app.models.board import Board
from app.repositories.interfaces import BoardRepository


class BoardService:
    def __init__(self, boards: BoardRepository) -> None:
        self.boards = boards

    def list_boards(self) -> list[Board]:
        return self.boards.list_all()

    def get_board(self, board_id: int) -> Board:
        board = self.boards.get(board_id)
        if board is None:
            raise NotFoundError("Board", board_id)
        return board

    def create_board(self, name: str) -> Board:
        cleaned = name.strip()
        if not cleaned:
            raise ValidationError("name must not be empty", "name")
        return self.boards.create(cleaned)

    def delete_board(self, board_id: int) -> None:
        board = self.get_board(board_id)
        self.boards.delete(board)

