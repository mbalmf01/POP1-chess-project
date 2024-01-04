from board.board import Board
from moves import is_piece_at, piece_at, is_check
from copy import deepcopy
from pieces.piece import Piece

class King(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side: bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side)
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side
    
    def king_move(self, pos_X, pos_Y) -> bool:
        result_x = (pos_X - self.pos_x)**2
        result_y = (pos_Y - self.pos_y)**2
        if result_x == 0:
            if result_y == 0:
                return False
        if result_x == 0 or result_x == 1:
            if result_y == 0 or result_y == 1:
                return True
            else:
                return False
        else:
            return False
        
    def king_range(self, B) -> list[tuple[int, int]]:
        king_coords: list[tuple[int, int]]
        #eight possible positions a king can move to
        size = B.size()
        if self.pos_x == size:
            p3 = (self.pos_x, self.pos_y + 1)
            p4 = (self.pos_x, self.pos_y - 1)
            p5 = (self.pos_x - 1, self.pos_y - 1)
            p6 = (self.pos_x - 1, self.pos_y)
            p7 = (self.pos_x - 1, self.pos_y + 1)
            king_coords = [p3, p4, p5, p6, p7]

        if self.pos_y == size:
            p1 = (self.pos_x + 1, self.pos_y)
            p4 = (self.pos_x, self.pos_y -1)
            p5 = (self.pos_x -1, self.pos_y - 1)
            p6 = (self.pos_x - 1, self.pos_y)
            p8 = (self.pos_x + 1, self.pos_y - 1)
            king_coords = [p1, p4, p5, p6, p8]

        else:
            p1 = (self.pos_x + 1, self.pos_y)
            p2 = (self.pos_x + 1, self.pos_y + 1)
            p3 = (self.pos_x, self.pos_y + 1)
            p4 = (self.pos_x, self.pos_y - 1)
            p5 = (self.pos_x - 1, self.pos_y - 1)
            p6 = (self.pos_x - 1, self.pos_y)
            p7 = (self.pos_x - 1, self.pos_y + 1)
            p8 = (self.pos_x + 1, self.pos_y - 1)

            king_coords = [p1, p2, p3, p4, p5, p6, p7, p8]

        return king_coords
    
    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule3] and [Rule4]'''
        if pos_X > B.size() or pos_Y > B.size():
            raise ValueError('values are greater than the specified board size')

        if pos_X < 1 or pos_Y < 1:
            raise ValueError('chess coordinates must be greater than 0!')

        #king can move to eight positions, all within one x or y coord
        if self.king_move(pos_X, pos_Y):
            # check is_piece_at final position
            if is_piece_at(pos_X, pos_Y, B):
                # if there's a piece, check its side and make sure it is not the same colour
                p = piece_at(pos_X, pos_Y, B)
                if p.side == self.side:
                    return False
                else:
                    return True
            return True
        else:
            return False
        
    def get_king2(self, side: bool, B: Board) -> Piece: #DO I ACTUALLY NEED THIS, OR CAN I JUST USE SELF?
        '''This function seems a bit redundant - need to work out the logic of what it's doing here'''
        king = [piece for piece in B.pieces() if type(piece) == King if piece.side == side]
        return King(king[0].pos_x, king[0].pos_y, king[0].side)
    
    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
        if not self.can_reach(pos_X, pos_Y, B):
            return False
        else:
            test_board = deepcopy(B)

            king = get_king2(self.side, test_board)
            if is_piece_at(pos_X, pos_Y, test_board):
                piece_out = piece_at(pos_X, pos_Y, test_board)
                test_board.pieces().remove(piece_out)
            for piece in test_board.pieces():
                if piece.pos_x == king.pos_x:
                    if piece.pos_y == king.pos_y:
                        piece.pos_x = pos_X
                        piece.pos_y = pos_Y
            if is_check(self.side, test_board):
                return False
            else:
                return True
    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B
        assumes this move is valid according to chess rules
        '''
        # check can_move_to for legality of move
        # if True, update King(Piece) with new coordinates
        # if piece of other side has the same coordinates, remove/delete that piece from memory
        #check can_move_to for legality of move
        if self.can_move_to(pos_X, pos_Y, B):
            king = get_king2(self.side, B)
            if is_piece_at(pos_X, pos_Y, B):
                piece_out = piece_at(pos_X, pos_Y, B)
                B.pieces().remove(piece_out)
            for piece in B.pieces():
                if piece.pos_x == king.pos_x and piece.pos_y == king.pos_y:
                    piece.pos_x = pos_X
                    piece.pos_y = pos_Y
        else:
            raise ValueError('cannot move to that square - check self.can_move_to')

        return B
    
class Rook(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side: bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side)
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side
    def rook_move(self, pos_X: int, pos_Y: int) -> bool:
        '''returns True if the Rook move is physically possible'''
        if self.pos_x == pos_X or self.pos_y == pos_Y:
            return True
        else:
            return False
    def rook_range(self, pos_X: int, pos_Y: int) -> list[tuple[int, int]]:
        if self.pos_x == pos_X:
            y_ranges = [i for i in range(self.pos_y + 1, pos_Y + 1) if self.pos_y < pos_Y] or \
                       [i for i in range(self.pos_y - 1, pos_Y - 1, -1) if self.pos_y > pos_Y]
            x_ranges = [pos_X]*len(y_ranges)
            return list(zip(x_ranges, y_ranges))

        if self.pos_y == pos_Y:
            x_ranges = [i for i in range(self.pos_x + 1, pos_X + 1) if self.pos_x < pos_X] or \
                       [i for i in range(self.pos_x - 1, pos_X - 1, -1) if self.pos_x > pos_X]
            y_ranges = [pos_Y] * len(x_ranges)
            return list(zip(x_ranges, y_ranges))
    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y on board B
        [Rule2] A rook can move any number of squares along a row
        or column, but cannot leap over other pieces.
        [Rule4] A piece of side X (Black or White) cannot move to a location occupied by a piece of side X.
        Hint: use is_piece_at
        '''
        #slice self.pos_y and pos_Y to get a range of x values between desired spot and
        if pos_X > B.size() or pos_Y > B.size():
            raise ValueError('values are greater than the specified board size')

        if pos_X < 1 or pos_Y < 1:
            raise ValueError('chess coordinates must be greater than 0!')

        if self.rook_move(pos_X, pos_Y):
            ranges = self.rook_range(pos_X, pos_Y)
            if len(ranges) == 1:
                if is_piece_at(pos_X, pos_Y, B):
                    # if there's a piece, check its side and make sure it is not the same colour
                    p = piece_at(pos_X, pos_Y, B)
                    if p.side == self.side:
                        return False
                    else:
                        return True
            if len(ranges) > 1:
                for x, y in ranges[0:(len(ranges) - 1)]:
                    if is_piece_at(x, y, B):
                        return False
            # check is_piece_at final position
            if is_piece_at(pos_X, pos_Y, B):
                # if there's a piece, check its side and make sure it is not the same colour
                p = piece_at(pos_X, pos_Y, B)
                if p.side == self.side:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False
    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y on board B according to all chess rules
        [Rule5] A piece of side X cannot make a move, if the configuration resulting from this move is a check for X
        '''
        if not self.can_reach(pos_X, pos_Y, B):
            return False

        test_board = deepcopy(B)
        if is_check(self.side, B):
            #rewrite logic for if piece can move when is_check = True. Can move piece if is_check = False after move
            for piece in test_board.pieces():
                if piece.pos_x == self.pos_x:
                    if piece.pos_y == self.pos_y:
                        piece.pos_x = pos_X
                        piece.pos_y = pos_Y
            if is_check(self.side, test_board):
                return False

        #[Rule5] A piece of side X cannot make a move, if the configuration resulting from this move is a check for X
        #need to update coordinates temporarily then check if is_check is True for the same side
        #if after self.pos_x = pos_X and self.pos_y = pos_Y is check is true, return False

        for piece in test_board.pieces():
            if piece.pos_x == self.pos_x:
                if piece.pos_y == self.pos_y:
                    piece.pos_x = pos_X
                    piece.pos_y = pos_Y
        if is_check(self.side, test_board):
            return False
        else:
            return True
    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        '''
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B
        assumes this move is valid according to chess rules
        '''
        #check can_move_to for legality of move
        if self.can_move_to(pos_X, pos_Y, B):
            if is_piece_at(pos_X, pos_Y, B):
                piece_out = piece_at(pos_X, pos_Y, B)
                #if True, update Rook(Piece) with new coordinates
                self.pos_x = pos_X
                self.pos_y = pos_Y
                # if piece of other side has the same coordinates, remove/delete that piece from memory
                B.pieces().remove(piece_out)
            else:
                self.pos_x = pos_X
                self.pos_y = pos_Y
        else:
            raise ValueError('cannot move to that square - check self.can_move_to')

        return B
    
class Bishop(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side: bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side)
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side

        # subtracting cell coordinates for two possible bishop moves results in a pair of numbers that are equal when squared
    def bishop_move(self, pos_X: int, pos_Y: int) -> bool:
        '''returns True if the bishop move is physically possible'''
        # x,y coords will change in every scenario, otherwise move isn't legal
        rows = self.pos_x - pos_X
        columns = self.pos_y - pos_Y
        if columns ** 2 == rows ** 2:
            if columns != 0:
                return True
            else:
                return False
        else:
            return False
    def bishop_range(self, pos_X: int, pos_Y: int) -> list[tuple[int, int]]:
        # four possibilities - either x, y both increase, x, y both decrease,
        # x increases and y decreases, or x decreases and y increases
        x_ranges = [i for i in range(self.pos_x+1, pos_X+1) if pos_X > self.pos_x] or \
                   [i for i in range(self.pos_x-1, pos_X-1, -1) if pos_X < self.pos_x]
        y_ranges = [j for j in range(self.pos_y+1, pos_Y+1) if pos_Y > self.pos_y] or \
                   [j for j in range(self.pos_y-1, pos_Y-1, -1) if pos_Y < self.pos_y]
        if len(x_ranges) == len(y_ranges):
            return list(zip(x_ranges, y_ranges))
        else:
            raise ValueError('illegal bishop move!')
    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''checks if this bishop can move to coordinates pos_X, pos_Y on board B according to rule [Rule1] and [Rule4]'''
        #check along the range of legal moves in between pos_x, pos_y and pos_X, pos_Y along board B
        #if there is a piece in the way - using is_piece_at function, return false
        #check if move is legal
        if pos_X > B.size() or pos_Y > B.size():
            raise ValueError('values are greater than the specified board size')

        if pos_X < 1 or pos_Y < 1:
            raise ValueError('chess coordinates must be greater than 0!')

        if self.bishop_move(pos_X, pos_Y):
            #check if pieces are in the way
            ranges = self.bishop_range(pos_X, pos_Y)
            for x, y in ranges[0:(len(ranges)-1)]:
                if is_piece_at(x, y, B):
                    return False
            #is_piece_at final position
            if is_piece_at(pos_X, pos_Y, B):
                #if there's a piece, check its side and make sure it is not the same colour
                p = piece_at(pos_X, pos_Y, B)
                if p.side == self.side:
                    return False
                else:
                    return True
            else:
                return True
        else:
            return False
    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''checks if this bishop can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
        #[Rule5] A piece of side X cannot make a move, if the configuration resulting from this move is a check for X
        #work out logic for preventing self check by moving bishop
        #cannot move this piece if the King is in check
        if not self.can_reach(pos_X, pos_Y, B):
            return False
        else:
            test_board = deepcopy(B)
            if is_check(self.side, B):
                # rewrite logic for if piece can move when is_check = True. Can move piece if is_check = False after move
                for piece in test_board.pieces():
                    if piece.pos_x == self.pos_x:
                        if piece.pos_y == self.pos_y:
                            piece.pos_x = pos_X
                            piece.pos_y = pos_Y
                if is_check(self.side, test_board):
                    return False

            #[Rule5] A piece of side X cannot make a move, if the configuration resulting from this move is a check for X
            #need to update coordinates temporarily then check if is_check is True for the same side
            #if after self.pos_x = pos_X and self.pos_y = pos_Y is check is true, return False
            for piece in test_board.pieces():
                if piece.pos_x == self.pos_x:
                    if piece.pos_y == self.pos_y:
                        piece.pos_x = pos_X
                        piece.pos_y = pos_Y
            if is_check(self.side, test_board):
                return False
            else:
                return True
    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        '''
        returns new board resulting from move of this bishop to coordinates pos_X, pos_Y on board B
        assumes this move is valid according to chess rules
        '''
        #check can_move_to for legality of move
        if self.can_move_to(pos_X, pos_Y, B):
            if is_piece_at(pos_X, pos_Y, B):
                piece_out = piece_at(pos_X, pos_Y, B)
                # if True, update Bishop(Piece) with new coordinates
                self.pos_x = pos_X
                self.pos_y = pos_Y
                # if piece of other side has the same coordinates, remove/delete that piece from memory
                B.pieces().remove(piece_out)
            else:
                self.pos_x = pos_X
                self.pos_y = pos_Y
        else:
            raise ValueError('cannot move to that square - check self.can_move_to')

        return B