import pygame

from checkers.constants import FPS, HEIGHT, TITLE, WIDTH

class Game:

    def __init__(self) -> None:
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
    
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

        pygame.quit()
