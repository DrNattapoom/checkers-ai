from .constants import BLACK, COLS, ROWS, WHITE
from .piece import Piece

class Board:

    def __init__(self) -> None:
        self.board = []
        self.remaining = [12, 12]
        self.promoted = [0, 0]
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
                square = self.get_piece(row, col)
                children = get_children(node, direction)
                if (is_empty(square)):
                    # check if it is a normal move or a capture
                    if (abs(piece.row - row) == 1):
                        return []
                    # only non-empty squares can be captured
                    children = list(filter(
                        lambda child: not is_empty(self.get_piece(child[0], child[1])), 
                        children
                    ))
                neighbors = []
                for child in children:
                    child_square = self.get_piece(child[0], child[1])
                    # check if it is a normal move or a capture
                    if (is_empty(child_square)):
                        neighbors.append(child)
                    else:
                        # only an oppoennt's piece can be captured
                        if (child_square.color != piece.color):
                            grand_children = get_children(child, direction)
                            for grand_child in grand_children:
                                grand_child_square = self.get_piece(grand_child[0], grand_child[1])
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
                    path += [self.get_piece(edge[0], edge[1])] if (edge is not None) else []
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

    def move(self, piece, row, col) -> None:
        # swap values to move
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        # update the piece position
        piece.move(row, col)
        # check if the piece should be promoted
        if (row == 0 or row == ROWS - 1):
            self.promote(piece)

    def promote(self, piece) -> None:
        piece.promote()
        # update the number of promoted pieces of the piece color
        color_idx = 0 if (piece.color == BLACK) else 1
        self.promoted[color_idx] += 1
    
    def remove(self, pieces) -> list:
        for piece in pieces:
            # remove the piece by setting the square to None
            self.board[piece.row][piece.col] = None
            if (piece is not None):
                # update the number of remaining pieces of the piece color
                color_idx = 0 if (piece.color == BLACK) else 1
                self.remaining[color_idx] -= 1
    
    def get_board(self) -> list[list]:
        return self.board

    def get_piece(self, row, col) -> Piece:
        return self.board[row][col]

    def get_remaining(self) -> list:
        return self.remaining

    def get_promoted(self) -> list:
        return self.promoted

    def get_winner(self) -> tuple:
        black, white = self.get_remaining()
        return WHITE if (black <= 0) else BLACK if (white <= 0) else None
