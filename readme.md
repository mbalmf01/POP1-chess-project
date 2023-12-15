
# Bishop, King and Rook Chess Puzzle 

## Intro

This coursework takes inspiration from chess, although it has significant differences with the standard [chess game](https://en.wikipedia.org/wiki/Chess). To reduce your workload, only the **bishop, king and rook** pieces will be involved in play.  The game will be played between **Black** and **White**, as usual. However, the board size will be `S x S`, where `S`  is a number between `2` and `26`, instead of the usual `8 x 8`. (We only set the limit `26`  to avoid visualisation/printing problems for large boards and denotation.) Also, rather unusually, each side (Black or White) may play with any number, including 0, of the allowed pieces in any positions, as long as they fit the board. E.g., there can be 5 black rooks and 15 white bishops on the board in a play. But, **each side has exactly one king**, as usual in chess. 

White starts the game, after which Black and White alternate by moving one of own pieces according to the usual chess rules, that are:

- *[Rule1]* A  bishop can move any number (1 or more) of squares diagonally, but cannot leap over other pieces.
- *[Rule2]* A  rook can move any number of squares along a row (also called rank in chess terminology) or column (also called file), but cannot leap over other pieces. Also, we disallow *castling* to simplify the coursework.
- *[Rule3]* The king moves one square in any direction, including diagonal, on the board. 

As usual, as a result of any move, the piece that is moved either occupies a previously empty board location, or captures the other side's piece. In that case, the former piece occupies the latter's position, while the latter piece is removed from the board. Clearly, we have the following:

- *[Rule4]* A piece of side X (Black or White) cannot move to a location occupied by a piece of side X.

**Check** for side X is a configuration of the board when X's king can be captured by a piece of the other side Y (in one move). Another chess rule we obey is:

- *[Rule5]* A piece of side X cannot make a move, if the configuration resulting from this move is a check for X. 

**Checkmate** is a configuration of the board when the king of a side X (Black or White)  is in *check* and there is no move available for X to eliminate the *check* situation. 



## Notation and Symbols

The columns will be designated by small letter characters from `a` to `z` and the rows by numbers from `1` to `26`. The leftmost column is `a` and the bottom row is `1`.

### Board configurations

We will need *plain board configurations* that are stored in files (on the PC) and *unicode board configurations* that are printed on the screen.

#### Plain board configurations

Each plain board configuration is determined by a sequence of of *piece locations*, where a piece location is a string of the form `Xcr` and  `X` is either equal 

- to `K`, to indicate  king, or 
- to `R` to indicate rook, or 
- to `B` to indicate bishop,

and `cr` indicates the column and row of a location of the piece. E.g., `Be14` says that there is a bishop in column `e` and row `14`.

Now, to store a configuration of the whole board in a file, we will use the following format:

- the **first line** of the file contains a single number representing the size of the board `S`
- the **second line** of the file contains piece locations of **White** pieces separated by `,`
- the **third line** of the file contains piece locations of **Black** pieces separated by `,`
- the last `,` on either line can be omitted and there may be arbitrarily many spaces before and after any `,`

See the file `board_examp.txt` for an example. A file is *valid* if it is syntactically correct as specified above, the configuration encoded in it has exactly one king for White and exactly one king for Black, there are no different pieces in the same location, and each location is within the `S x S` square.

#### Unicode board configurations


To designate the pieces, we will use the [chess unicode characters](https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode):
 
| piece |  character | escape sequence   |
|-------|------------|--------------|
|white king | ♔ | \u2654 |
|white rook | ♖ | \u2656 |
|white bishop | ♗| \u2657 |
|black king | ♚ | \u265A|
|black rook | ♜ | \u265C|
|black bishop | ♝ | \u265D|
|space of matching width | |\u2001|

> **Note** In Python code, you can use the characters "directly" by copy/pasting from the table above (except the space), or by the escape sequence. E.g., 
>```
>print("♔")
>```
>or 
>```
>print("\u2654")
>```
>will print  `♔` and 
>```
>"♔"=="\u2654"
>```
>will print `True`.

When outputting the configuration of an `S x S` board on the screen, we will use the format, where the output has `S` lines and each line is a string of the form `ln[0] ln[1] ... ln[S-1]` representing the correspoinding row. So, each `ln[i]` is either one of ♔, ♖, ♗, ♚, ♜, ♝, or the space of the matching width (\u2001). For example, the plain boad configuration stored in the file `board_examp.txt` corresponds to the following unicode board configuration:

~~~
♖ ♔  
 ♜  ♜
 ♚ ♜ 
♖   ♗
♗    
~~~

### Moves

It will be needed to specify moves of pieces.  To indicate the moves, we will use the strings of the form `crCR`,  where `cr` indicates the column and row of the origin of the move, and `CR` indicates the row and column of the destination of the move. For example, `a1b2` says that the piece located in the column `a` and row `1` moves to the column  `b` and row `2`. Note that the string `crCR` can have length between 4 and 6.

## Requirements

>**Note: the requirements below are mandatory to follow. You will lose marks if your implementation does not meet these requirements** 

In this coursework, you will implement a Python program, in which a human user will play the specific version of chess described above against the computer. **The human always plays with White and computer always plays with Black.**    

### Initiation

When the program is executed, it first promts the user to provide a file name that stores a plain board configuration:

```
File name for initial configuration: 
```
The user inputs the file name or types `QUIT` to terminate the program. If this file is not valid (see Plain board configurations), the program states that and prompts to provide a file name again:

```
This is not a valid file. File name for initial configuration: 
```
The user inputs the file name or types `QUIT` to terminate the program. This continues until the user provides a valid file or terminates the program. If a valid file is provided, the plain board configuration it contains, becomes the initial configuration of the play. This configuration is printed on the screen in unicode format. For example, 

```
The initial configuration is:
♖ ♔  
 ♜  ♜
 ♚ ♜ 
♖   ♗
♗    
```

### Play rounds

Each round is a move of White followed by a move of Black. In each round, the program prints:

```
Next move of White:
```

The user can indicate a move in the format described above (see Moves), e.g.

```
Next move of White: a1b2
```

Instead of making a move, White can print `QUIT` to indicate that they want to stop the game and save the current configuration in a file. If the user prints `QUIT`, the program prompts the user to provide a name of the file to store the current configuration:

```
File name to store the configuration:
```

After specifying the file name, the program saves the current configuration in the plain format. The program prints the confirmation:

```
The game configuration saved.
```
and terminates.

If the user inputed a move, the program checks if this move is valid chess move (see Intro). If this is not the case, the program prompts the user to provide another input:

```
This is not a valid move. Next move of White:
```

This continues until the user inputs a valid chess move or  `QUIT` to save the configuration and terminate the program. When a valid chess move is inputed, the program prints the next configuration of the game (after White's move), e.g.,

```
The configuration after White's move is:
♖ ♔  
 ♜  ♜
 ♚ ♜ 
♖♗  ♗
     
```
Now, the current configuration may or may not be a checkmate for Black. If it is (so Black has no valid moves) the program prints:
```
Game over. White wins.
```
and terminates. If it is not, the program computes the next valid move for Black, using any method you like, prints the move and the configuration after this move, e.g.:
```
Next move of Black is e3c3. The configuration after Black's move is:
♖ ♔  
 ♜♜  
 ♚ ♜ 
♖♗  ♗
     
```
The current configuration may or may not be a checkmate for White. If it is (so White has no valid moves) the program prints:
```
Game over. Black wins.
```
and terminates. If it is not, a new round of the game occurs. 

## Software Specification

>**Important notes:** 
>
> - The specification below, including class/function/method names and data types of arguments/return values,  is mandatory to follow. **You will lose marks** if your implementation does not adhere to the specification, **even in case your program runs with no errors**.
> - All the classes/functions/methods in the file `chess_puzzle.py` must be implemented according to the specification. You can use additional classes/functions/methods.
> - The tests initially present in the file `test_chess_puzzle.py` must pass, when `pytest test_chess_puzzle.py` is executed. Your additional tests (see section Validation) must pass as well.
> - You can use additional files for some parts of your code.
> - Instructions marked with Hint or Hints are not the part of the specification and may be ignored without effect on your mark.
> - Your implementation must be in Python 3.9 or later version.
> - Your code must be well-structured in terms of visual readability (use indentation, spacing, etc.) and non-redundancy (instead of duplicating long pieces of code, introduce your own functions). We do not require to follow any variable naming conventions. 
> - All the required functions and methods in the file `chess_puzzle.py` must pass any correct unit tests on them, particularly, unit tests that do not set up any global (or class-wide) variables. Thus, if you are using any global (or class-wide) variables in the implementation of the required functions and methods, make sure that this requirement is satisfied.   

It will be convenient, instead of using chess locations given by columns and rows, such as `e2`, to use the horizontal (i.e., x) and vertical (i.e., y) coordinates of a location ranging from `1` to `26`, such as, respectively, `5` and `2`. The column `a` corresponds to the horizontal coordinate `1`, the column `b` corresponds to the horizontal coordiate `2`, etc., while row `1` corresponds to the vertical coordinate `1`, row `2` corresponds to the vertical coordinate `2`, etc. We need a function that converts chess locations to coordinates, and another function that converts vice versa:
```
def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''
    
	
def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
```

To represent chess pieces, we will make use of the following class:
```
class Piece:
    pos_x : int	
    pos_y : int
    side : bool #True for White and False for Black
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values'''
```
and to represent a board configuration, we will use a pair (tuple) of an integer representing the size of the board `S` and a list of pieces, i.e.,
```
Board = tuple[int, list[Piece]]
```
The list of pieces contains all the pieces present on the board and the locations on the board with the coordinates not occupied by any piece in the list are considered empty. The following two functions are required:
```
def is_piece_at(pos_X : int, pos_Y : int, B: Board) -> bool:
    '''checks if there is piece at coordinates pox_X, pos_Y of board B''' 
	
def piece_at(pos_X : int, pos_Y : int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B 
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    '''
```

We introduce the three subclasses of `Piece`, one for each piece type involved in the play[^1]:
```
class Rook(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
	
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule2] and [Rule4] (see section Intro)
        Hint: use is_piece_at
        '''
    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''
        checks if this rook can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        
        Hints:
        - firstly, check [Rule2] and [Rule4] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule5], use is_check on new board
        '''
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''

class Bishop(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this bishop can move to coordinates pos_X, pos_Y on board B according to rule [Rule1] and [Rule4]'''
    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this bishop can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this bishop to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''


class King(Piece):
    def __init__(self, pos_X : int, pos_Y : int, side_ : bool):
        '''sets initial values by calling the constructor of Piece'''
    def can_reach(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule3] and [Rule4]'''
    def can_move_to(self, pos_X : int, pos_Y : int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
    def move_to(self, pos_X : int, pos_Y : int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
```
To check for *checks* and *checkmates*, we require the functions:
```
def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    '''

def is_checkmate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is checkmate for side

    Hints: 
    - use is_check
    - use can_reach 
    '''
``` 

To read the configuration from files (on PC) and save it, we will need the functions:
```
def read_board(filename: str) -> Board:
    '''
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    '''

def save_board(filename: str, B: Board) -> None:
    '''saves board configuration into file in current directory in plain format'''
```
To generate Black's moves by the computer player, we need:
```
def find_black_move(B: Board) -> tuple[Piece, int, int]:
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assuming there is at least one black piece that can move somewhere

    Hints: 
    - use can_move_to
    - possibly, use methods of random library
    '''
```
We suggest the following simplest approach to implement `find_black_move`.  For every Black piece on the board and piece coordinates `x,y`, where `x` and `y` are in the range `1..S`, check if the piece can move there. If so, return this piece and the coordinates. Further, to make the behaviour of the computer player less "predictable", you can pick the pieces on the board in a random order. Also, you can pick the coordinates randomly. This function will not be verified by unit tests (see next section) and you can use any approach to implement it that returns valid results.

For the screen output, we need:
```
def conf2unicode(B: Board) -> str: 
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''
```

Finally, we require the implementation of the play to be enclosed in the function:
```
def main() -> None:
    '''
    runs the play

    Hint: implementation of this could start as follows:
    filename = input("File name for initial configuration: ")
    ...
    '''    
```
[^1]: You may note that the methods `can_reach`, `can_move` and `move_to` as well as the constructor, could be naturally declared in the class `Piece`, because every piece in our program must have them. This would require the use of so called abstract classes, which are not naturally present in Python, but can be added using the `ABC` library. You can add this feature to your program, as an optional excercise not contributing to your mark.

## Validation

In the file `test_chess_puzzle.py`, you will find initial unit tests in pytest format for all the functions/methods provided in the specification, except for:

- constructors of classes
- `save_board`
- `find_black_move`
- `main`

Those functions/methods are exepmt from testing (due to their particular nature). 

You must add your own tests for all non-exempt functions and methods. There must be **at least five** test cases in pytest format for each such function/method. We do not mandate how the test cases are organised, i.e., implementation of the test cases related to a function/method can be placed in different test functions, or grouped together. Your tests must cover as many possible scenarios as possible. *The quality of your testing contributes to the mark.* You will lose marks if you have too few tests, your tests fail, or you did not provide tests for some important scenarios.

## Development and Submission

You are expected to work on the coursework in your assigned *GitHub* repository. You must create commits, with messages, that describe the history of the development of your project. We expect **at least one commit within any 14 days interval** from the date of the Topic 6 session to the date you submit your project (on Codio). *You will lose marks if you do not meet this requirement*. The use of other features of git, e.g., branches, is optional and does not contribute to your mark.

### Submission

The files of the final version of your project must be placed in the designated project on Codio. We require the following files (see section Software specification) in your submission directory:

- `chess_puzzle.py`
- `test_chess_puzzle.py`

and any other files or directories that are needed for them to run. To locate your submission directory for marking, we will look for a directory containing the two files above. If there is more than one such directory, one of them must be named `submission` and this is the one we will use for marking. (If you develop your project outside of Codio, you can simply clone it to the Codio project before the submission.)

> Note: by the deadline of coursework submission, you must have both:
> 
> - the GitHub repo with the final version of your coursework (and history)
> - the code in the project on Codio
> 
> Both entries contribute to your mark. 

You are required to check, in particular, if you develop your project outside of Codio, that your system works as you expect by running `python chess_puzzle.py` in your submission directory of the project on Codio.

### Additional Libraries

You can use *any standard Python libraries available via pip for Python 3.9* in your implementation. If you do, you must make sure they are installed in your Codio project and your implementation runs on Codio as expected. (You can install them using `pip3 install ...` command in Terminal. You can request admin permissions if necessary using `sudo` command; see Linux documentation.)

## Marking

Your mark will be determined according to the following rubric:

|Category| Weight | full | 3/4 | 1/2 | 1/4 | 0 |
|--|--|--|--|--|--|--|
| **Requirements** (*completeness* = system responds to all use scenarios; *correctness* = all responses are as expected) | 40% | Correct and complete | Correct and mostly complete | Mostly correct and mostly complete | Either mostly incorrect and mostly complete, or mostly incomplete and mostly correct | Either fully incorrect, or fully incomplete, or mostly incorrect and mostly incomplete |  
| **Specification** (*completeness* = all required parts (functions, classes, etc.) are present; *correctness* = their implementation is correct (including data types) | 35% |Correct and complete | Correct and mostly complete | Mostly correct and mostly complete | Either mostly incorrect and mostly complete, or mostly incomplete and mostly correct | Either fully incorrect, or fully incomplete, or mostly incorrect and mostly incomplete |
| **Validation** (*completeness* = appropriate variety of scenarios are verified; *correctness* = tests for them are correctly written) | 15% | Correct and complete | Correct and mostly complete | Mostly correct and mostly complete | Either mostly incorrect and mostly complete, or mostly incomplete and mostly correct | Either fully incorrect, or fully incomplete, or mostly incorrect and mostly incomplete |
| **Development style** (*well-structured code* = visual readability and non-redundancy (see Software Specification); *commit history* = commits on fortnightly basis (see Development and Submission)) | 10% | Well-structured code and regular commits | Well-stuctured code and one gap in commits | Nearly well-structured code and at most one gap | Not well-structured code or more than one gap | Not well-structured code and more than one gap |

> **Notes:** 
> - your submission will be marked 'as is' according to the rubric using the same Codio set up as your project. It is your responsibility to check that your submission runs on Codio as you expect it.
> - if you do not provide commits for longer than four weeks, it counts as two gaps
