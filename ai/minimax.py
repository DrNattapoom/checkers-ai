from copy import deepcopy

from checkers.constants import BLACK, WHITE

class Minimax:

    DEFAULT_DEPTH = 3

    def __init__(self, game) -> None:
        self.game = game
        self.depth = Minimax.DEFAULT_DEPTH
        self.best_move = None

    def move(self, color) -> None:
        _, new_checkers = self.algorithm(color)
        checkers = self.game.get_checkers()
        checkers.set_board(new_checkers.get_board())
        checkers.change_turn()

    def algorithm(self, to_maximize) -> tuple:
        def algorithm_helper(checkers, depth, maximize) -> tuple:
            if (depth == 0 or checkers.get_winner() is not None):
                return self.evaluate(checkers), checkers
            if (maximize):
                max_score = float("-inf")
                best_move = None
                for move in self.get_possible_moves_by_color(checkers, WHITE):
                    self.depth -= 1
                    score = algorithm_helper(move, depth - 1, False)[0]
                    if (score > max_score):
                        max_score = score
                        best_move = move
                return max_score, best_move
            else:
                min_score = float("inf")
                best_move = None
                for move in self.get_possible_moves_by_color(checkers, BLACK):
                    score = algorithm_helper(move, depth - 1, True)[0]
                    if (score < min_score):
                        min_score = score
                        best_move = move
                return min_score, best_move
        maximize = True if (to_maximize == WHITE) else False
        return algorithm_helper(self.game.get_checkers(), self.DEFAULT_DEPTH, maximize)

    def get_possible_moves_by_color(self, checkers, color):
        moves = []
        for piece in self.get_pieces_by_color(checkers, color):
            legal_moves = checkers.get_board().find_legal_moves(piece)
            for move, path in legal_moves.items():
                temp = deepcopy(checkers)
                new_board = self.simulate(temp, temp.get_piece(piece.row, piece.col), move, path)
                moves.append(new_board)
        return moves

    def get_pieces_by_color(self, checkers, color):
        board = checkers.get_board()
        pieces = sum(board.get_board(), [])
        return list(filter(
            lambda piece: piece is not None and piece.color == color,
            pieces
        ))

    def simulate(self, checkers, piece, move, path):
        checkers.move(piece, move[0], move[1])
        if (path): 
            checkers.get_board().remove(path)
        return checkers

    def evaluate(self, checkers) -> float:
        board = checkers.get_board()
        black, white = board.get_remaining()
        black_promoted, white_promoted = board.get_promoted()
        return white - black + (white_promoted * 0.5 - black_promoted * 0.5)
