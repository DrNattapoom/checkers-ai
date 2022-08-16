import pygame

from checkers.checkers import Checkers
from checkers.constants import BOARD_THEMES, COLS, DEFAULT_THEME, FPS, HEIGHT, ROWS, SQUARE_SIZE, TITLE, WIDTH

class Game:

    def __init__(self) -> None:
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.checkers = Checkers()
        self.theme = DEFAULT_THEME
    
    def play(self):
        pygame.display.set_caption(TITLE)
        clock = pygame.time.Clock()
        end = False

        while not end:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass
            self.update()

        pygame.quit()

    def update(self) -> None:
        self.draw(self.win)
        pygame.display.update()

    def draw(self, win) -> None:
        def draw_board(board):
            # fill the entire board with darker squares
            win.fill(BOARD_THEMES[self.theme][0])
            # draw lighter squares over to complete the checkered pattern
            for row in range(ROWS):
                for col in range(row % 2, COLS, 2):
                    pygame.draw.rect(
                        win, 
                        BOARD_THEMES[self.theme][1], 
                        (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                    )
        draw_board(win)
