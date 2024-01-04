from board.board import Board
from pieces.Pieces import King, Rook, Bishop
from moves import get_letter, index2location, process_file

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
    
def piece_location_dict(B: Board) -> dict[tuple[int, int], str]:
    # create dictionary of pieces
    white_dict = {King: '\u2654', Rook: '\u2656', Bishop: '\u2657'}
    black_dict = {King: '\u265A', Rook: '\u265C', Bishop: '\u265D'}

    squares = B.squares()

    piece_dict: dict[tuple[int, int], str] = {}
    for piece in B.pieces():
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
    first_line = B.size()
    white_pieces = [get_letter(p) + index2location(p.pos_x, p.pos_y) for p in B.pieces() if p.side is True]
    black_pieces = [get_letter(p) + index2location(p.pos_x, p.pos_y) for p in B.pieces() if p.side is False]
    second_line = ', '.join(white_pieces)
    third_line = ', '.join(black_pieces)
    f_out.write(f'{first_line}\n{second_line}\n{third_line}\n')
    print('The game configuration saved.')
    f_out.close()

def conf2unicode(B: Board) -> str:
    '''converts board configuration B to unicode format string'''

    squares = B.squares()
    piece_dict = piece_location_dict(B)
    piece_order = [piece_dict[j] for j in squares]
    piece_string = u''

    for i, j in enumerate(piece_order):
        if i % (B.size()) == 0:
            piece_string += f'\n{j}'
        else:
            piece_string += f'{j}'

    return str(piece_string[1:])