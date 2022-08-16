from checkers.board import Board
from checkers.constants import BLACK, COLS, ROWS, WHITE
from checkers.piece import Piece

class Checkers:

    def __init__(self) -> None:
        self.board = Board()
        self.remaining = [12, 12]
        self.promoted = [0, 0]
        self.turn = BLACK
        self.selected = None
        self.legal_moves = {}

    def select(self, row, col) -> bool:
        square = self.board.get_piece(row, col)
        if (self.selected is None):
            if (square is not None and square.color == self.turn):
                # select one of the pieces and find its legal moves
                self.selected = square
                self.legal_moves = self.find_legal_moves(square)
                return True
        else:
            if (square is None and (row, col) in self.legal_moves):
                # moves to an empty square and may capture opponent's pieces
                self.move(self.selected, row, col)
                to_be_captured = self.legal_moves[(row, col)]
                if (to_be_captured):
                    # update number of remaining pieces
                    removed = self.board.remove(to_be_captured)
                    self.remaining = [a - b for a, b in zip(self.remaining, removed)]
                self.change_turn()
                return True
            else:
                # deselect
                self.selected = None
                self.legal_moves = {}
                # allow instant new selection
                self.select(row, col)
        return False
    
    def move(self, piece, row, col) -> None:
        board = self.board.get_board()
        # swap values to move
        board[piece.row][piece.col], board[row][col] = board[row][col], board[piece.row][piece.col]
        # update the piece position
        piece.move(row, col)
        # check if the piece should be promoted
        if (row == 0 or row == ROWS - 1):
            piece.promote()
            # update the number of promoted pieces of the piece color
            color_idx = 0 if (piece.color == BLACK) else 1
            self.promoted[color_idx] += 1

    def change_turn(self) -> None:
        self.selected = None
        self.legal_moves = {}
        self.turn = WHITE if (self.turn == BLACK) else BLACK

    def find_legal_moves(self, piece) -> dict:
        # return legal moves reachable within 1 move
        def get_neighbors(node) -> list:
            # return a boolean representing whether the square is empty or not
            def is_empty(square):
                return square is None
            # return left and right squares regardless of whether the square is empty or not
            def get_children(node, direction) -> list:
                row, col = node
                # set row constraint according to the direction
                row_out_of_bound = row - 1 < 0 if (direction == -1) else row + 1 >= ROWS
                # filter the result according to the column constraint
                return [] if (row_out_of_bound) else list(filter(
                    lambda pair: 0 <= pair[1] <= COLS - 1, 
                    [(row + direction, col - 1), (row + direction, col + 1)]
                ))
            # return legal moves reachable within 1 move
            def get_neighbors_helper(node, direction) -> list:
                square = self.board.get_piece(row, col)
                children = get_children(node, direction)
                if (is_empty(square)):
                    # check if it is a normal move or a capture
                    if (abs(piece.row - row) == 1):
                        return []
                    # only non-empty squares can be captured
                    children = list(filter(
                        lambda child: not is_empty(self.board.get_piece(child[0], child[1])), 
                        children
                    ))
                neighbors = []
                for child in children:
                    child_square = self.board.get_piece(child[0], child[1])
                    # check if it is a normal move or a capture
                    if (is_empty(child_square)):
                        neighbors.append(child)
                    else:
                        # only an oppoennt's piece can be captured
                        if (child_square.color != piece.color):
                            grand_children = get_children(child, direction)
                            for grand_child in grand_children:
                                grand_child_square = self.board.get_piece(grand_child[0], grand_child[1])
                                if (is_empty(grand_child_square) and grand_child[1] != col):
                                    # the neighbor is the empty square after capturing
                                    neighbors.append(grand_child)
                return neighbors
            row, col = node
            direction = -1 if (piece.color == BLACK) else 1
            neighbors = get_neighbors_helper(node, direction)
            # get neighbors from 2 directions if the piece is promoted
            return neighbors if (not piece.is_promoted) else neighbors + get_neighbors_helper(node, direction * (-1))
        # return parents dictionary so that each move can be traced back
        def dfs() -> dict:
            # let each legal move be a node and each to-be-captured piece be an edge
            # traverse the graph using DFS algorithm and construct parents dictionary
            root = (piece.row, piece.col)
            parents = {root: None}
            stack = [root]
            while (stack):
                node = stack.pop()
                neighbors = get_neighbors(node)
                for neighbor in neighbors:
                    if (neighbor not in parents.keys()):
                        stack.append(neighbor)
                        parents.update({neighbor: node})
            return parents
        # return a dictionary mappig a legal move to a list of pieces needed to be captured
        def find_legal_moves_helper() -> dict:
            # return an edge that connects u and v (i.e., a piece needed to be captured)
            def get_edge(u, v) -> tuple:
                return (int((u[0] + v[0]) / 2), int((u[1] + v[1]) / 2)) if (abs(u[0] - v[0]) != 1) else None
            # return a path from s to t (i.e., every piece needed to be captured)
            def get_path(s, t) -> list:           
                path = []
                # start from the destination
                current = t
                # trace back using parents dictionary
                while (current != s):
                    next = parents[current]
                    edge = get_edge(current, next)
                    path += [self.board.get_piece(edge[0], edge[1])] if (edge is not None) else []
                    current = next
                return path
            parents = dfs()
            # exclude the current position from the legal moves
            legal_squares = set(parents.keys()).difference({(piece.row, piece.col)})
            legal_moves = {}
            for square in legal_squares:
                # get path for each legal move
                legal_moves[square] = get_path((piece.row, piece.col), square)
            return legal_moves
        return find_legal_moves_helper()

    def get_legal_moves(self) -> dict:
        return self.legal_moves

    def get_board(self) -> Board:
        return self.board

    def get_piece(self, row, col) -> Piece:
        return self.board.get_piece(row, col)
