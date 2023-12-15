import pytest
from chess_puzzle import *

#process file tests
def test_process_file():
    lines = ['27', 'Ka1', 'Ke5, Rc4']
    with pytest.raises(ValueError):
        assert process_file(lines)

def test_process_file1():
    lines = ['-5', 'Ka1', 'Ke5, Rc4']
    with pytest.raises(ValueError):
        assert process_file(lines)

def test_process_file2():
    lines = ['5', 'Ka1', 'Ke5, Rc4']
    assert process_file(lines)

def test_process_file3():
    lines = ['5', 'Ka1, Ka3', 'Ke5, Rc4']
    with pytest.raises(ValueError):
        assert process_file(lines)

def test_process_file4():
    lines = ['5', 'Ra1', 'Ke5, Rc4']
    with pytest.raises(ValueError):
        assert process_file(lines)

def test_process_file5():
    lines = ['5', 'Ka1', 'Ke5']
    with pytest.raises(ValueError):
        assert process_file(lines)

def test_process_file6():
    lines = ['5', 'Ka1, Ka3', 'Re5']
    with pytest.raises(ValueError):
        assert process_file(lines)

def test_process_file7():
    lines = ['five', 'Ka1', 'Ke5, Rc4']
    with pytest.raises(ValueError):
        assert process_file(lines)

def test_process_file8():
    lines = ['5', 'Ka1, Ra1', 'Ke5, Rc4']
    with pytest.raises(ValueError):
        assert process_file(lines)

def test_process_file9():
    lines = ['10', 'Ka1, Ra2, Rb1, Rb3, Rb5, Rc7', 'Kf5, Rh4']
    assert process_file(lines)

def test_process_file10():
    with pytest.raises(ValueError):
        assert process_file(['2', 'Ka1', 'Kb2, Rc3'])

#same square tests
def test_same_square():
    lines = ['5', 'Ka1', 'Ke5, Rc4']
    b = process_file(lines)
    assert same_square(board_pieces(b)) is False

def test_same_square1():
    Ka1 = King(1,1,True)
    Ra1 = Rook(1,1,True)
    Ke5 = King(4,5,False)
    Rc4 = Rook(3,4,False)
    b = [Ka1, Ra1, Ke5, Rc4]
    assert same_square(b)

wb1 = Bishop(1, 1, True)
wr1 = Rook(1, 2, True)
wb2 = Bishop(5, 2, True)
bk = King(2, 3, False)
br1 = Rook(4, 3, False)
br2 = Rook(2, 4, False)
br3 = Rook(5, 4, False)
wr2 = Rook(1, 5, True)
wk = King(3, 5, True)
B1 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk])

#bishop move tests
def test_bishop_move():
    assert wb1.bishop_move(1, 2) is False
def test_bishop_move1():
    assert wb1.bishop_move(2, 2) is True
def test_bishop_move2():
    assert wb1.bishop_move(4, 4) is True
def test_bishop_move3():
    assert wb1.bishop_move(4, 5) is False
def test_bishop_move4():
    assert wb1.bishop_move(-1, -1) is True
def test_bishop_move5():
    assert wb1.bishop_move(100, 100) is True
def test_bishop_move6():
    assert wb2.bishop_move(4, 3) is True
def test_bishop_move7():
    assert wb2.bishop_move(6, 1) is True
def test_bishop_move8():
    assert wb2.bishop_move(2, 6) is False

#bishop range tests
def test_bishop_range():
    assert wb1.bishop_range(4, 4) == [(2, 2), (3, 3), (4, 4)]
def test_bishop_range1():
    assert wb2.bishop_range(2, 5) == [(4, 3), (3, 4), (2, 5)]
def test_bishop_range2():
    with pytest.raises(ValueError):
        wb2.bishop_range(2, 6)

#bishop can reach tests
def test_bishop_can_reach():
    assert wb1.can_reach(5, 5, B1) is True

def test_bishop_can_reach1():
    with pytest.raises(ValueError):
        wb1.can_reach(-5, -5, B1)

def test_bishop_can_reach2():
    with pytest.raises(ValueError):
        wb1.can_reach(6, 6, B1)

def test_bishop_can_reach3():
    assert wb2.can_reach(3, 4, B1) is False

def test_bishop_can_reach4():
    assert wb2.can_reach(4, 3, B1) is True

wr1a = Rook(2, 2, True)
bka = King(3, 3, False)

B2 = (5, [wb1, wr1a, wb2, bka, br1, br2, br3, wr2, wk])

def test_bishop_can_reach5():
    assert wb1.can_reach(4, 4, B2) is False

#bishop can move to tests
def test_bishop_can_move_to():
    assert wb1.can_move_to(4, 4, B2) is False

def test_bishop_can_move_to1():
    assert wb1.can_move_to(4, 4, B1) is True

wkb = King(4, 5, True)
wb1b = Bishop(4, 4, True)
wb2b = Bishop(5, 2, True)
wr2b = Rook(1, 5, True)
wr1b = Rook(1, 2, True)
bkb = King(2, 3, False)
br1b = Rook(3, 4, False)
br2b = Rook(5, 4, False)
br3b = Rook(4, 1, False)

B3 = (5, [wkb, wb1b, wb2b, wr2b, wr1b, bkb, br1b, br2b, br3b])

def test_bishop_can_move_to2():
    assert wb1b.can_move_to(3, 3, B3) is False

def test_bishop_can_move_to3():
    assert wb1b.can_move_to(5, 5, B3) is False

def test_bishop_can_move_to4():
    assert is_check(True, B3) is False

def test_bishop_can_move_to5():
    B1 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk])
    assert wb1.can_move_to(4, 4, B1) is True

#king can move to test
def test_king_can_move_to():
    B5 = (5, [wr1b, bkb, wkb])
    assert bkb.can_move_to(3, 3, B5)

B10 = (5, [wb1, wr1a, wb2, bk, br1, br2, br3, wr2, wk])
def test_find_black_move():
    black_move = find_black_move(B10)
    assert black_move[1] == 3
    assert black_move[2] == 3

def test_get_piece():
    assert type(get_piece(5, 2, 'B', False)) == Bishop

#move piece tests

board_move_piece = (5, [Bishop(1, 1, True), Rook(1, 2, True), Bishop(5, 2, True), King(3, 3, False), Rook(4, 3, False), Rook(2, 4, False), Rook(5, 4, False), Rook(1, 3, True), King(3, 5, True)])


def test_move_piece():
    loc_dest = 'a2b2'
    assert move_piece(loc_dest, board_move_piece) == [(1, 2), (2 , 2)]

def test_move_piece1():
    loc_dest = 'a2b6'
    assert move_piece(loc_dest, board_move_piece) is None

def test_move_piece2():
    loc_dest = 'a6b2'
    assert move_piece(loc_dest, board_move_piece) is None

def test_move_piece3():
    loc_dest = 'aaa'
    assert move_piece(loc_dest, board_move_piece) is None

#board pieces tests
B4 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk])
def test_board_pieces1():
    b4 = (5, [King(4, 5, True), King(2, 3, False), Bishop(4, 4, True)])
    test_list = board_pieces(b4)
    test_piece = test_list[0]
    assert test_piece.pos_x == 4
    assert test_piece.pos_y == 5
    assert test_piece.side is True

def test_board_pieces2():
    pieces = board_pieces(B4)
    assert len(pieces) == 9
    assert type(pieces) == list
    assert type(pieces[0]) == Bishop

#location2index tests
def test_location2index1():
    assert location2index("e2") == (5, 2)

def test_location2index2():
    assert location2index("z26") == (26, 26)

def test_index2location1():
    assert index2location(5, 2) == "e2"

def test_index2location2():
    assert index2location(26, 1) == "z1"

#get letter test
def test_get_letter():
    assert get_letter(wk) == 'K'


def test_get_king():
    king = get_king(False, B1)
    assert king.side is False
    assert king.pos_x == 2
    assert king.pos_y == 3

def test_initialising_piece_with_values():
    p = Piece(pos_X=1, pos_Y=2, side=True)
    assert p.pos_x == 1
    assert p.pos_y == 2
    assert p.side is True


def test_read_board1():
    filename = 'board_examp.txt'
    b = read_board(filename)
    pieces = board_pieces(b)
    kings = [k for k in pieces if type(k) == King]
    assert len(kings) == 2

def test_is_checkmate():
    wrc1 = Rook(2, 2, True)
    wrc2 = Rook(1, 3, True)
    bkc = King(3, 3, False)
    B7 = (5, [wb1, wrc1, wb2, bkc, br1, br2, br3, wrc2, wk])
    assert is_checkmate(False, B7) is True

wb1 = Bishop(1, 1, True)
wr1 = Rook(1, 2, True)
wb2 = Bishop(5, 2, True)
bk = King(2, 3, False)
br1 = Rook(4, 3, False)
br2 = Rook(2, 4, False)
br3 = Rook(5, 4, False)
wr2 = Rook(1, 5, True)
wk = King(3, 5, True)

wb1a = Bishop(4, 4, True)
wr1a = Rook(2, 2, True)
bka = King(3, 3, False)

def test_is_checkmate1():
    B2 = (5, [wb1a, wr1a, wb2, bka, br1, br2, br3, wr2, wk])
    assert is_checkmate(False, B2) is True

test_rook = Rook(1, 2, True)

def test_rook_range():
    assert len(test_rook.rook_range(1, 10)) == 8

def test_rook_range1():
    assert test_rook.rook_range(1, 4) == [(1, 3), (1, 4)]

def test_board_size():
    assert board_size(B1) == 5
def test_board_size1():
    assert type(board_size(B1)) == int
def test_board_pieces():
    assert board_pieces(B1) != [wb1, wr1, wb2, bk, wk]

def test_rook_move():
    assert test_rook.rook_move(1, 4) is True

def test_rook_move1():
    assert test_rook.rook_move(-5, 2) is True

def test_rook_move2():
    assert test_rook.rook_move(1, 100) is True

def test_rook_move3():
    assert test_rook.rook_move(1, -30) is True

def test_rook_move4():
    assert test_rook.rook_move(2, 3) is False

def test_rook_move5():
    assert test_rook.rook_move(2, 2) is True

b1 = Bishop(1,1,True)
b2 = Bishop(5,2,True)
r1 = Rook(1,5,True)
r2 = Rook(1,2,True)
k1 = King(3,5,True)
k2 = King(2,3,False)
r3 = Rook(4,3,False)
r4 = Rook(2,4,False)
r5 = Rook(5,4,False)

board = (5, [b1,b2,r1,r2,r3,r4,r5,k1,k2])

def test_rook_can_reach():
    assert r1.can_reach(1, 3, board)

def test_rook_move_to():
    assert r1.can_move_to(1, 3, board)

#is piece at tests
def test_is_piece_at1():
    assert is_piece_at(1, 4, board) is False

def test_is_piece_at2():
    assert is_piece_at(1, 5, board) is True

def test_is_piece_at3():
    assert is_piece_at(1, 3, board) is False

def test_is_piece_at4():
    assert is_piece_at(2, 2, B1) is False

#piece at tests
def test_piece_at4():
    assert type(piece_at(1, 5, board)) == Rook

def test_piece_at5():
    rook = piece_at(1, 5, board)
    assert rook.pos_x == 1
    assert rook.pos_y == 5
    assert rook.side

# wb1 = Bishop(1, 1, True)
# wr1 = Rook(1, 2, True)
# wb2 = Bishop(5, 2, True)
bkb = King(2, 3, False)
# br1 = Rook(4, 3, False)
# br2 = Rook(2, 4, False)
# br3 = Rook(5, 4, False)
# wr2 = Rook(1, 5, True)
wkb = King(3, 5, True)

wr1b = Rook(2, 2, True)

def test_king_can_move_to2():
    B5 = (5, [wr1b, bkb, wkb])
    assert bk.can_move_to(3, 3, B5)
    #assert find_black_move(B1) == (bk, 3, 3)

#rook move tests
def test_can_reach1():
    assert wr2.can_reach(4, 5, B1) is False

br2a = Rook(1, 5, False)
wr2a = Rook(2, 5, True)

def test_can_move_to1():
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2a, br3, wr2a, wk])
    assert wr2a.can_move_to(2, 4, B2) is False

def test_is_check1():
    wr2b = Rook(2, 4, True)
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2a, br3, wr2b, wk])
    assert is_check(True, B2) is True

def test_is_checkmate2():
    br2b = Rook(4, 5, False)
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2b, br3, wr2, wk])
    assert is_checkmate(True, B2) is True

wr2c = Rook(1, 3, True)
b = (5, [Bishop(1, 1, True), Rook(2, 2, True), Bishop(5, 2, True), King(3, 3, False), Rook(4, 3, False), Rook(2, 4, False), Rook(5, 4, False), Rook(1, 3, True), King(3, 5, True)])

def test_check1():
    assert is_check(False, b)

def test_checkmate1():
    assert is_checkmate(False, b)

#configuration 1
wb1 = Bishop(1, 1, True)
wr1 = Rook(1, 2, True)
wb2 = Bishop(5, 2, True)
bk = King(2, 3, False)
br1 = Rook(4, 3, False)
br2 = Rook(2, 4, False)
br3 = Rook(5, 4, False)
wr2 = Rook(1, 5, True)
wk = King(3, 5, True)

wb1a = Bishop(4, 4, True)
wr1a = Rook(2, 2, True)
bka = King(3, 3, False)

wkb = King(4, 5, True)
wb1b = Bishop(4, 4, True)
wb2b = Bishop(5, 2, True)
wr2b = Rook(1, 5, True)
wr1b = Rook(1, 2, True)
bkb = King(2, 3, False)
br1b = Rook(3, 4, False)
br2b = Rook(5, 4, False)
br3b = Rook(4, 1, False)

B1 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk])
B2 = (5, [wb1, wr1a, wb2, bk, br1, br2, br3, wr2, wk])
B3 = (5, [wkb, wb1b, wb2b, wr2b, wr1b, bkb, br1b, br2b, br3b])
B4 = (5, [wb1, wr1, wb2, bk, br1, br2, br3, wr2, wk])
B6 = (5, [wb1, wr1a, wb2, bka, br1, br2, br3, wr2, wk])

bkb = King(2, 3, False)
wkb = King(3, 5, True)

wr1b = Rook(2, 2, True)


def test_find_black_move2():
    B1 = (5, [wb1, wr1b, wb2, bk, br1, br2, br3, wr2, wk])
    with pytest.raises(ValueError):
        assert bk.move_to(2, 2, B1)

def test_piece_at1():
    assert piece_at(4, 3, B1) == br1

def test_piece_at2():
    with pytest.raises(IndexError):
        assert piece_at(4, 6, B1)

def test_can_reach2():
    assert wr2.can_reach(4, 5, B1) is False

def test_can_move_to2():
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2a, br3, wr2a, wk])
    assert not wr2a.can_move_to(2, 4, B2)

def test_can_move_to3():
    with pytest.raises(ValueError):
        assert wr2.can_move_to(-1, 5, B1)

def test_is_check2():
    wr2b = Rook(2, 4, True)
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2a, br3, wr2b, wk])
    assert is_check(True, B2) is True


def test_is_checkmate3():
    br2b = Rook(4, 5, False)
    B2 = (5, [wb1, wr1, wb2, bk, br1, br2b, br3, wr2, wk])
    assert is_checkmate(True, B2) is True


def test_read_board2():
    B = read_board("board_examp.txt")
    assert B[0] == 5

    for piece in B[1]:  # we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]:  # we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found


def test_conf2unicode1():
    assert conf2unicode(B1) == "♖ ♔  \n ♜  ♜\n ♚ ♜ \n♖   ♗\n♗    "