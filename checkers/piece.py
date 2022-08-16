from checkers.constants import SQUARE_SIZE

class Piece:

    # padding and outline for drawing
    PADDING = 10
    OUTLINE = 5

    def __init__(self, row, col, color) -> None:
        self.row = row
        self.col = col
        self.color = color
        self.is_promoted = False

    def move(self, row, col) -> None:
        self.row = row
        self.col = col
        
    def get_coordinates(self):
        return [
            SQUARE_SIZE * self.col + SQUARE_SIZE // 2,
            SQUARE_SIZE * self.row + SQUARE_SIZE // 2
        ]
        