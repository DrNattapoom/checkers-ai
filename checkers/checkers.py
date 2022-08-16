from checkers.board import Board
from checkers.constants import BLACK, ROWS
from checkers.piece import Piece

class Checkers:

    def __init__(self) -> None:
        self.board = Board()
        self.remaining = [12, 12]
        self.promoted = [0, 0]
        self.selected = None

    def move(self, piece, row, col) -> None:
        board = self.board.get_board()
        # swap values to move
        board[piece.row][piece.col], board[row][col] = board[row][col], board[piece.row][piece.col]
        # update the piece position
        piece.move(row, col)
        # check if the piece should be promoted
        if (row == 0 or row == ROWS - 1):
            piece.promotes()
            # update the number of promoted pieces of the piece color
            color_idx = 0 if (piece.color == BLACK) else 1
            self.promoted[color_idx] += 1

    def get_board(self) -> Board:
        return self.board

    def get_piece(self, row, col) -> Piece:
        return self.board.get_piece(row, col)
