from checkers.board import Board

class Checkers:

    def __init__(self) -> None:
        self.board = Board()
        self.remaining = [12, 12]
        self.promoted = [0, 0]
        self.selected = None

    def get_board(self) -> None:
        return self.board.get_board()
