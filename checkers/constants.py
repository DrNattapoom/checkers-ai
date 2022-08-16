# game title
TITLE = "Checkers"
# frame per second
FPS = 60

# board dimensions
WIDTH = HEIGHT = 800
ROWS = COLS = 8
SQUARE_SIZE = WIDTH // COLS

# RGB colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# board themes: (dark, light)
BOARD_THEMES = [
    [(134, 166, 102), (218, 237, 207)],
    [(140, 162, 173), (222, 227, 230)]
]
# default theme: from 0 to len(BOARD_THEMES) - 1 inclusively
DEFAULT_THEME = 0