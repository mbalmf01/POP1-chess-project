from board.board_layout import *
from board.board import Board
from moves import *

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
        if len(B.pieces()) == 2:
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