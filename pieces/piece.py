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