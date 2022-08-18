import pygame

from ai.minimax import Minimax
from .checkers import Checkers
from .constants import BLACK, BOARD_THEMES, COLS, DEFAULT_THEME, HEIGHT, ROWS, SQUARE_SIZE, WHITE, WIDTH
from .piece import Piece

class Game:

    # game title
    TITLE = "Checkers"
    # frame per second
    FPS = 60

    def __init__(self) -> None:
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.checkers = Checkers()
        self.theme = DEFAULT_THEME
        self.winner = None
        self.end = False
    
    def play(self) -> None:
        pygame.display.set_caption(Game.TITLE)
        clock = pygame.time.Clock()

        minimax_ai = Minimax(self)

        while not self.end:
            clock.tick(Game.FPS)

            turn = self.checkers.get_turn()

            if (self.no_legal_moves(turn, minimax_ai)):
                print("no legal moves allowed")
                winner = WHITE if (self.checkers.get_turn() == BLACK) else BLACK
                self.winner = self.checkers.set_winner(winner)
            if (turn == WHITE):
                minimax_ai.move(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    row, col = self.get_position_from_mouse(position)
                    self.checkers.select(row, col)
            
            self.winner = self.checkers.get_winner()
            self.end = self.winner is not None
            
            self.update()

        self.display_winner()
        pygame.quit()

    def no_legal_moves(self, color, ai):
        return not ai.get_possible_moves_by_color(self.checkers.get_board(), color)

    def display_winner(self) -> None:
        text = "BLACK" if (self.winner == BLACK) else "WHITE" if (self.winner == WHITE) else None
        print(text, "WON")
    
    def get_winner(self) -> tuple:
        return self.checkers.get_winner()

    def get_checkers(self) -> Checkers:
        return self.checkers

    def get_position_from_mouse(self, position) -> tuple:
        x, y = position
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col

    def update(self) -> None:
        self.draw(self.win)
        pygame.display.update()

    def draw(self, win) -> None:
        def draw_board():
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
        def draw_piece(piece) -> None:
            radius = SQUARE_SIZE // 2 - Piece.PADDING
            coordinates = piece.get_coordinates()
            pygame.draw.circle(win, piece.color, coordinates, radius)
            # draw a crown for a promoted piece
            crown = WHITE if (piece.color == BLACK) else BLACK
            if (piece.is_promoted):
                pygame.draw.circle(win, crown, coordinates, radius / 2)
                pygame.draw.circle(win, piece.color, coordinates, radius / 2 - Piece.OUTLINE)
        def draw_legal_moves(legal_moves) -> None:
            for legal_move in legal_moves:
                row, col = legal_move
                alpha = (100,)
                # define surface so that alpha level can be adjusted
                surface = pygame.Surface((win.get_width(), win.get_height()), pygame.SRCALPHA)
                pygame.draw.circle(surface, BLACK + alpha, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), radius = 20)
                self.win.blit(surface, (0, 0))
        draw_board()
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.checkers.get_piece(row, col)
                # check if there is a piece in the square
                if piece is not None:
                    draw_piece(piece)
        draw_legal_moves(self.checkers.get_legal_moves())
