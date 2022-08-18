from copy import deepcopy

from checkers.board import Board
from checkers.constants import BLACK, WHITE

class Minimax:

    DEFAULT_DEPTH = 5    

    def __init__(self, game) -> None:
        self.game = game

    def move(self, color) -> None:
        _, new_board = self.algorithm(color)
        checkers = self.game.get_checkers()
        checkers.set_board(new_board)
        checkers.change_turn()

    def algorithm(self, to_maximize) -> tuple:
        def algorithm_helper(board, alpha, beta, depth, maximize) -> tuple:
            if (depth == 0 or board.get_winner() is not None):
                return self.evaluate(board), board
            if (maximize):
                color = WHITE
                new_alpha_beta = lambda alpha, beta, score: (max(alpha, score), beta)
                is_better = lambda new, old: new > old
                best_score = float("-inf")
            else:
                color = BLACK
                new_alpha_beta = lambda alpha, beta, score: (alpha, min(beta, score))
                is_better = lambda new, old: new < old
                best_score = float("inf")
            best_move = None
            for move in self.get_possible_moves_by_color(board, color):
                score = algorithm_helper(move, alpha, beta, depth - 1, not maximize)[0]
                if (is_better(score, best_score)):
                    best_score = score
                    best_move = move
                alpha, beta = new_alpha_beta(alpha, beta, score)
                if (beta <= alpha):
                    break
            return best_score, best_move
        maximize = True if (to_maximize == WHITE) else False
        return algorithm_helper(self.game.get_checkers().get_board(), float("-inf"), float("inf"), Minimax.DEFAULT_DEPTH, maximize)

    def get_possible_moves_by_color(self, board, color) -> list:
        moves = []
        for piece in self.get_pieces_by_color(board, color):
            legal_moves = board.find_legal_moves(piece)
            for move, path in legal_moves.items():
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate(temp_board, temp_piece, move, path)
                moves.append(new_board)
        return moves

    def get_pieces_by_color(self, board, color) -> list:
        pieces = sum(board.get_board(), [])
        return list(filter(
            lambda piece: piece is not None and piece.color == color,
            pieces
        ))
    
    def simulate(self, board, piece, move, path) -> Board:
        board.move(piece, move[0], move[1])
        if (path): 
            board.remove(path)
        return board

    def evaluate(self, board) -> float:        
        black, white = board.get_remaining()
        black_promoted, white_promoted = board.get_promoted()
        return white - black + (white_promoted - black_promoted) * 1.5
