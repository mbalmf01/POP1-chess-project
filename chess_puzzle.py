import string
import random
from copy import deepcopy
import re

class Piece:
    """
    Chess piece.
    """
    pos_x: int
    pos_y: int

    def __init__(self, pos_X: int, pos_Y: int, side: bool):
        '''sets initial values'''
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side
Board = tuple[int, list[Piece]]
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
        if pos_X > board_size(B) or pos_Y > board_size(B):
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
            for piece in board_pieces(test_board):
                if piece.pos_x == self.pos_x:
                    if piece.pos_y == self.pos_y:
                        piece.pos_x = pos_X
                        piece.pos_y = pos_Y
            if is_check(self.side, test_board):
                return False

        #[Rule5] A piece of side X cannot make a move, if the configuration resulting from this move is a check for X
        #need to update coordinates temporarily then check if is_check is True for the same side
        #if after self.pos_x = pos_X and self.pos_y = pos_Y is check is true, return False

        for piece in board_pieces(test_board):
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
                board_pieces(B).remove(piece_out)
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
        if pos_X > board_size(B) or pos_Y > board_size(B):
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
                for piece in board_pieces(test_board):
                    if piece.pos_x == self.pos_x:
                        if piece.pos_y == self.pos_y:
                            piece.pos_x = pos_X
                            piece.pos_y = pos_Y
                if is_check(self.side, test_board):
                    return False

            #[Rule5] A piece of side X cannot make a move, if the configuration resulting from this move is a check for X
            #need to update coordinates temporarily then check if is_check is True for the same side
            #if after self.pos_x = pos_X and self.pos_y = pos_Y is check is true, return False
            for piece in board_pieces(test_board):
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
                board_pieces(B).remove(piece_out)
            else:
                self.pos_x = pos_X
                self.pos_y = pos_Y
        else:
            raise ValueError('cannot move to that square - check self.can_move_to')

        return B
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
        size = board_size(B)
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
        if pos_X > board_size(B) or pos_Y > board_size(B):
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
    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
        if not self.can_reach(pos_X, pos_Y, B):
            return False
        else:
            test_board = deepcopy(B)

            king = get_king(self.side, test_board)
            if is_piece_at(pos_X, pos_Y, test_board):
                piece_out = piece_at(pos_X, pos_Y, test_board)
                board_pieces(test_board).remove(piece_out)
            for piece in board_pieces(test_board):
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
            king = get_king(self.side, B)
            if is_piece_at(pos_X, pos_Y, B):
                piece_out = piece_at(pos_X, pos_Y, B)
                board_pieces(B).remove(piece_out)
            for piece in board_pieces(B):
                if piece.pos_x == king.pos_x and piece.pos_y == king.pos_y:
                    piece.pos_x = pos_X
                    piece.pos_y = pos_Y
        else:
            raise ValueError('cannot move to that square - check self.can_move_to')

        return B

def same_square(pieces: list) -> bool:
    coords = [(p.pos_x, p.pos_y) for p in pieces]
    if len(set(coords)) == len(pieces):
        return False
    else:
        return True

def process_file(lines: list) -> Board:
    size = int(lines[0].strip('\n'))
    if size > 26 or size < 2:
        raise ValueError('board not within size range')
    else:
        white_pieces = (lines[1].strip('\n')).split(', ')
        black_pieces = (lines[2].strip('\n')).split(', ')
        pieces = []
        for wp in white_pieces:
            x, y = location2index(wp)
            z = wp[0]
            pieces.append(get_piece(pos_X=x, pos_Y=y, piece=z, side=True))

        for bp in black_pieces:
            x, y = location2index(bp)
            z = bp[0]
            pieces.append(get_piece(pos_X=x, pos_Y=y, piece=z, side=False))

        for p in pieces:
            if p.pos_x > size or p.pos_y > size:
                raise ValueError('piece coordinates outside scope of the board')

        kings = [k for k in pieces if type(k) == King]
        if same_square(pieces):
            raise ValueError('two pieces cannot occupy the same square')
        if len(kings) != 2:
            raise ValueError('there must be exactly two kings to play chess!')
        if kings[0].side == kings[1].side:
            raise ValueError('this game requires at least two kings from opposite sides and another piece to play')
        if len(pieces) == 2:
            raise ValueError('this game requires at least two kings from opposite sides and another piece to play')
        else:
            b = (size, pieces)

        return b

def read_board(filename: str) -> Board:
    """
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    Ba1, Ra2, Be2, Ra5, Kc5
    """
    # read chess_puzzle

    loop_statement = True
    while loop_statement:
        if filename == 'QUIT':
            quit()
        try:
            with open(filename) as chess:
                lines = chess.readlines()
                b = process_file(lines)
                return b

        except Exception as e:
            print(e)
            filename = input('This is not a valid file. File name for initial configuration: ')

def get_king(side: bool, B: Board) -> King:
    king = [piece for piece in board_pieces(B) if type(piece) == King if piece.side == side]
    return King(king[0].pos_x, king[0].pos_y, king[0].side)
def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules
    assumes there is at least one black piece that can move somewhere
    '''
    squares = board_squares(B)
    random.shuffle(squares)

    bk = get_king(False, B)
    #possible_move = [(x, y) for x, y in squares if bk.can_move_to(x,y,B)]
    if is_check(False, B):
        for x, y in squares:
            if bk.can_move_to(x, y, B):
                return bk, x, y

    black_pieces = [piece for piece in board_pieces(B) if piece.side is False]

    if len(black_pieces) == 1:
        for x, y in squares:
            if bk.can_move_to(x, y, B):
                return bk, x, y
        else:
            print('Stalemate! Game over.')
            quit()

    black_piece = random.choice(black_pieces)

    if type(black_piece) == King:
        for x, y in squares:
            if black_piece.can_move_to(x, y, B):
                return black_piece, x, y
        else:
            black_piece = random.choice(black_pieces)

    if type(black_piece) == Rook:
        for x, y in squares:
            if black_piece.can_move_to(x, y, B):
                return black_piece, x, y
            else:
                black_piece = random.choice(black_pieces)
    if type(black_piece) == Bishop:
        for x, y in squares:
            if black_piece.can_move_to(x, y, B):
                return black_piece, x, y
            else:
                black_piece = random.choice(black_pieces)
def board_size(B: Board):
    return B[0]
def board_pieces(B: Board):
    return B[1]
def board_squares(B: Board) -> list[tuple[int, int]]:
    size = board_size(B)
    x_ranges = range(1, size+1)
    y_ranges = range(size, 0, -1)
    squares = [(x, y) for y in y_ranges for x in x_ranges]
    return squares
def piece_location_dict(B: Board) -> dict[tuple[int, int], str]:
    # create dictionary of pieces
    white_dict = {King: '\u2654', Rook: '\u2656', Bishop: '\u2657'}
    black_dict = {King: '\u265A', Rook: '\u265C', Bishop: '\u265D'}

    squares = board_squares(B)

    piece_dict: dict[tuple[int, int], str] = {}
    for piece in board_pieces(B):
        if piece.side is True:
            p = white_dict[type(piece)]
            piece_dict[(piece.pos_x, piece.pos_y)] = p
        if piece.side is False:
            p = black_dict[type(piece)]
            piece_dict[(piece.pos_x, piece.pos_y)] = p

    for s in squares:
        if s not in piece_dict:
            piece_dict[s] = '\u2001'

    return piece_dict
def save_board(filename: str, B: Board) -> None:
    '''saves board configuration into file in current directory in plain format'''
    f_out = open(filename, 'w')
    first_line = board_size(B)
    white_pieces = [get_letter(p) + index2location(p.pos_x, p.pos_y) for p in board_pieces(B) if p.side is True]
    black_pieces = [get_letter(p) + index2location(p.pos_x, p.pos_y) for p in board_pieces(B) if p.side is False]
    second_line = ', '.join(white_pieces)
    third_line = ', '.join(black_pieces)
    f_out.write(f'{first_line}\n{second_line}\n{third_line}\n')
    print('The game configuration saved.')
    f_out.close()
def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    returns True if it is check
    '''
    king = get_king(side, B)
    enemy_side = not side
    enemy_pieces = [ep for ep in board_pieces(B) if ep.side == enemy_side]
    enemy_bishops = [Bishop(eb.pos_x, eb.pos_y, eb.side) for eb in enemy_pieces if type(eb) == Bishop]
    enemy_rooks = [Rook(er.pos_x, er.pos_y, er.side) for er in enemy_pieces if type(er) == Rook]
    enemy_king = get_king(enemy_side, B)

    for bishop in enemy_bishops:
        if bishop.can_reach(king.pos_x, king.pos_y, B):
            return True

    for rook in enemy_rooks:
        if rook.can_reach(king.pos_x, king.pos_y, B):
            return True

    if enemy_king.can_reach(king.pos_x, king.pos_y, B):
        return True
    else:
        return False
def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side
    '''
    king = get_king(side, B)
    if is_check(side, B):
        for x, y in board_squares(B):
            if king.can_move_to(x, y, B):
                return False
        else:
            return True
    else:
        return False

def conf2unicode(B: Board) -> str:
    '''converts board configuration B to unicode format string'''

    squares = board_squares(B)
    piece_dict = piece_location_dict(B)
    piece_order = [piece_dict[j] for j in squares]
    piece_string = u''

    for i, j in enumerate(piece_order):
        if i % (board_size(B)) == 0:
            piece_string += f'\n{j}'
        else:
            piece_string += f'{j}'

    return str(piece_string[1:])
def location2index(loc: str) -> tuple[int, int]:
    '''
    converts chess location to corresponding x and y coordinates
    Be2
    '''
    # create dictionary of alphabet
    column_names = list(string.ascii_lowercase)
    row_names = list(range(1, 27))
    alpha_dict = dict(zip(column_names, row_names))
    string_pattern = re.compile(r'[a-z][0-9]+')
    matches = string_pattern.findall(loc)
    loc = matches[0]
    row = int(loc[1:])
    column = alpha_dict[loc[0]]
    return column, row
def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location - COMPLETED'''
    # create dictionary of alphabet
    column_names = list(string.ascii_lowercase)
    row_names = list(range(1, 27))
    alpha_dict = dict(zip(row_names, column_names))

    column = alpha_dict[x]

    return column + str(y)
def is_piece_at(pos_X: int, pos_Y: int, B: Board) -> bool:
    '''checks if a piece is at coordinates pos_X, pos_Y of board B'''
    coords = []
    for p in board_pieces(B):
        if p.pos_x == pos_X and p.pos_y == pos_Y:
            coords.append((pos_X, pos_Y))
    if len(coords) > 0:
        return True
    else:
        return False

def piece_at(pos_X: int, pos_Y: int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pos_X, pos_Y of board B
    assumes some piece at coordinates pos_X, pos_Y of board B is present
    '''
    if is_piece_at(pos_X, pos_Y, B):
        for p in board_pieces(B):
            if p.pos_x == pos_X:
                if p.pos_y == pos_Y:
                    return p
    else:
        raise IndexError('no piece at these coordinates!')

def get_piece(pos_X, pos_Y, piece, side):
    if piece == 'B':
        return Bishop(pos_X, pos_Y, side)
    if piece == 'R':
        return Rook(pos_X, pos_Y, side)
    if piece == 'K':
        return King(pos_X, pos_Y, side)
def get_letter(piece: Piece) -> str:
    if type(piece) == Rook:
        return 'R'
    if type(piece) == Bishop:
        return 'B'
    if type(piece) == King:
        return 'K'
def move_piece(location_destination: str, B: Board) -> list[tuple[int, int]]:
    # crCR with no piece definition, 4-6 letters e.g a1b1 or a20b1 or a1b20 or a20b20
    try:
        chess_regex = re.compile(r'[a-z][0-9]+')
        matches = chess_regex.findall(location_destination)
        matches = ['P' + p for p in matches]
        piece_location = location2index(matches[0])
        piece_destination = location2index(matches[1])
        if piece_location[0] > board_size(B) or piece_location[1] > board_size(B):
            raise ValueError('incorrect coordinates given')
        if piece_destination[0] > board_size(B) or piece_destination[1] > board_size(B):
            raise ValueError('incorrect coordinates given')
        else:
            return [piece_location, piece_destination]
    except ValueError as v:
        print(f'{v}, try again: ')
    except IndexError as i:
        print(f'Length of string too short. Must be at least 4 characters long! Further details: {i}')
    except TypeError as t:
        print(f'String not in correct format or too short. Must be in the format [a-z][0-9]+. Further details: {t}')

def main() -> None:
    '''
    runs the play
    '''
    filename = input("File name for initial configuration: ")
    B = read_board(filename)
    #print board
    print('''The initial configuration is: ''')
    print(conf2unicode(B))
    while not is_checkmate(True, B):
        loop_statement = False
        loc = ''
        while not loop_statement:
            loc = input('Next move for White: ')
            if loc == 'QUIT':
                fn = input('enter filename to save the board position: ')
                save_board(fn, B)
                print(f'file saved as {fn}, program ended by user')
                quit()
                break
            if move_piece(loc, B) is None:
                continue
            if len(move_piece(loc, B)) == 2:
                (v, w), (x, y) = move_piece(loc, B)
                if is_piece_at(v, w, B):
                    if (piece_at(v, w, B)).side:
                        if ((piece_at(v, w, B)).can_move_to(x, y, B)):
                            break
                        else:
                            print('this is an illegal move. You must select a legal move.')
                    else:
                        print('this piece is black, you must select a white piece.')
                else:
                    print('no piece there.. Select different coordinates.')
            else:
                print('incorrect coordinates given, length is less than 4 or greater than six! Try again.')

        (v, w), (x, y) = move_piece(loc, B)

        p = piece_at(v, w, B)

        print('new configuration, black to move...')
        print(conf2unicode(p.move_to(x, y, B)))
        if is_checkmate(False, B):
            print('Game over. White wins.')
            quit()
            break
        if len(board_pieces(B)) == 2:
            print('Only kings left on the board. Stalemate.')
            quit()
            break
        else:
            black_piece, pos_X, pos_Y = find_black_move(B)
            bp_start_coords = index2location(black_piece.pos_x, black_piece.pos_y)
            bp_end_coords = index2location(pos_X, pos_Y)
            print(f'''Next move of Black is {bp_start_coords}{bp_end_coords}.''')
            print('''The configuration after Black's move is:''')
            print(conf2unicode(black_piece.move_to(pos_X, pos_Y, B)))


    if is_checkmate(True, B):
        print('Game over. Black wins.')
        quit()

if __name__ == '__main__':  # keep this in
    main()
