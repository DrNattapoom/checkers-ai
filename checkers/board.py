from checkers.constants import BLACK, COLS, ROWS, WHITE
from checkers.piece import Piece

class Board:

    def __init__(self) -> None:
        self.board = []
        self.init_board()

    def init_board(self) -> None:
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                # 3-rd and 4-th rows are space separating 2 colors/sides 
                # not allow pieces in light sqaures
                if (3 <= row <= 4 or col % 2 != (row + 1) % 2):
                    self.board[row].append(None)
                else:
                    color = WHITE if (row < 3) else BLACK
                    self.board[row].append(Piece(row, col, color))

    def remove(self, pieces) -> list:
        removed = [0, 0]
        for piece in pieces:
            # remove the piece by setting the square to None
            self.board[piece.row][piece.col] = None
            if (piece is not None):
                # update the number of remaining pieces of the piece color
                color_idx = 0 if (piece.color == BLACK) else 1
                removed[color_idx] += 1
        return removed
    
    def get_board(self) -> list[list]:
        return self.board

    def get_piece(self, row, col) -> Piece:
        return self.board[row][col]
