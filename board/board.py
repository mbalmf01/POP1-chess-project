from pieces.piece import Piece
# Board = tuple[int, list[Piece]]

class Board:
    def __init__(self, size: int, pieces: list[Piece]):
        self.size = size
        self.pieces = pieces

        def size(self) -> int:
            return self.size
        
        def pieces(self) -> list[Piece]:
            return self.pieces
        
        def squares(self) -> list[tuple[int, int]]:
            x_ranges = range(1, self.size+1)
            y_ranges = range(size, 0, -1)
            squares = [(x, y) for y in y_ranges for x in x_ranges]
            return squares