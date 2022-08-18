from .board import Board
from .constants import BLACK, ROWS, WHITE
from .piece import Piece

class Checkers:

    def __init__(self, board = Board()) -> None:
        self.board = board
        self.turn = BLACK
        self.winner = None
        self.selected = None
        self.legal_moves = {}

    def select(self, row, col) -> bool:
        square = self.board.get_piece(row, col)
        if (self.selected is None):
            if (square is not None and square.color == self.turn):
                # select one of the pieces and find its legal moves
                self.selected = square
                self.legal_moves = self.board.find_legal_moves(square)
                return True
        else:
            if (square is None and (row, col) in self.legal_moves):
                # moves to an empty square and may capture opponent's pieces
                self.board.move(self.selected, row, col)
                to_be_captured = self.legal_moves[(row, col)]
                if (to_be_captured):
                    self.board.remove(to_be_captured)
                self.set_winner(self.board.get_winner())
                self.change_turn()
                return True
            else:
                # deselect
                self.selected = None
                self.legal_moves = {}
                # allow instant new selection
                self.select(row, col)
        return False

    def change_turn(self) -> None:
        self.selected = None
        self.legal_moves = {}
        self.turn = WHITE if (self.turn == BLACK) else BLACK

    def get_turn(self) -> tuple:
        return self.turn

    def get_legal_moves(self) -> dict:
        return self.legal_moves

    def get_board(self) -> Board:
        return self.board

    def get_piece(self, row, col) -> Piece:
        return self.board.get_piece(row, col)

    def get_winner(self) -> tuple:
        return self.winner

    def set_winner(self, winner) -> None:
        self.winner = winner

    def set_board(self, board) -> None:
        self.board = board
