import random, string, re
from board.board import Board
from pieces.Pieces import King, Bishop, Rook
from pieces.piece import Piece

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
            b = Board(size, pieces)

        return b

def get_king(side: bool, B: Board) -> Piece:
    king = [piece for piece in B.pieces() if type(piece) == King if piece.side == side]
    return King(king[0].pos_x, king[0].pos_y, king[0].side)

def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules
    assumes there is at least one black piece that can move somewhere
    '''
    squares = B.squares()
    random.shuffle(squares)

    bk = get_king(False, B)
    #possible_move = [(x, y) for x, y in squares if bk.can_move_to(x,y,B)]
    if is_check(False, B):
        for x, y in squares:
            if bk.can_move_to(x, y, B):
                return bk, x, y

    black_pieces = [piece for piece in B.pieces() if piece.side is False]

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

def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    returns True if it is check
    '''
    king = get_king(side, B)
    enemy_side = not side
    enemy_pieces = [ep for ep in B.pieces() if ep.side == enemy_side]
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
        for x, y in B.squares():
            if king.can_move_to(x, y, B):
                return False
        else:
            return True
    else:
        return False


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
    for p in B.pieces():
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
        for p in B.pieces():
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
        if piece_location[0] > B.size() or piece_location[1] > B.size():
            raise ValueError('incorrect coordinates given')
        if piece_destination[0] > B.size() or piece_destination[1] > B.size():
            raise ValueError('incorrect coordinates given')
        else:
            return [piece_location, piece_destination]
    except ValueError as v:
        print(f'{v}, try again: ')
    except IndexError as i:
        print(f'Length of string too short. Must be at least 4 characters long! Further details: {i}')
    except TypeError as t:
        print(f'String not in correct format or too short. Must be in the format [a-z][0-9]+. Further details: {t}')
