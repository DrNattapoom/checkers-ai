from checkers.board import Board
from checkers.piece import Piece

class Checkers:

    def __init__(self) -> None:
        self.board = Board()
        self.remaining = [12, 12]
        self.promoted = [0, 0]
        self.selected = None

    def get_board(self) -> Board:
        return self.board

    def get_piece(self, row, col) -> Piece:
        return self.board.get_piece(row, col)
