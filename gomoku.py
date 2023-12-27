"""ESC180_Project 2: Gomoku Game and the A.I Engine (7%)

Author(s): Michael Guerzhoy, and Anusha Fatima Alam with tests contributed by Siavash Kazemian.

Last modified: Nov. 17, 2022
"""

def is_empty(board):
    '''Return True if the board is empty and false otherwise'''
    '''A board is an n by m matrix in the form list of lists'''

    for n in range (len(board)):
        for m in range (len(board[n])):
            if board[n][m] != " ":
                return False
    return True

def is_complete(board):
    '''Return True if the board is full and false otherwise'''
    '''A board is an n by m matrix in the form list of lists'''
    '''This function is used for analyzing whether there is a draw between both the players.'''

    for n in range (len(board)):
        for m in range (len(board[n])):
            if board[n][m] == " ":
                return False
    return True

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    '''For a complete and valid sequence in board board, return Open or Closed or Semiopen.'''

    # Compute the adjacent ends for the sequence
    y_begin = y_end - (d_y*length)
    x_begin = x_end - (d_x*length)
    y_finish = y_end + d_y
    x_finish = x_end + d_x

    # If both adjacent ends are outside of board (i.e. the sequence is bounded by the edge of the board) return closed.
    if (min(y_begin, x_begin))<0 and (max(y_finish, x_finish))>len(board)-1:
        return "CLOSED"
    elif (min(y_finish, x_finish))<0 and (max(y_begin, x_begin))>len(board)-1:
        return "CLOSED"
    elif (min(y_begin, x_begin))<0  and (min(y_finish, x_finish))<0:
        return "CLOSED"
    elif (max(y_begin, x_begin))>len(board)-1 and (max(y_finish, x_finish))>len(board)-1:
        return "CLOSED"

    # If either adjacent ends are outside the board, check the opposite end.
    elif (min(y_begin, x_begin))<0:
        if board[y_finish][x_finish] != " ":
            return "CLOSED"
        else:
            return "SEMIOPEN"
    elif (max(y_finish, x_finish)) > len(board)-1:
        if board[y_begin][x_begin] != " ":
            return "CLOSED"
        else:
            return "SEMIOPEN"
    elif (min(y_finish, x_finish)) < 0:
        if board[y_begin][x_begin] != " ":
            return "CLOSED"
        else:
            return "SEMIOPEN"
    elif (max(y_begin, x_begin)) > len(board)-1:
        if board[y_finish][x_finish] != " ":
            return "CLOSED"
        else:
            return "SEMIOPEN"

    # If the end adjacent to start of the sequence and end of the sequence are
    # blocked (not empty), return closed.
    elif board[y_begin][x_begin] != " " and board[y_finish][x_finish] != " ":
        return "CLOSED"
    # Otherwise if adjacent ends are both empty, return Open.
    elif board[y_begin][x_begin] == " " and board[y_finish][x_finish] == " ":
        return "OPEN"
    # If the sequence is neither open nor closed, return Semiopen.
    else:
        return "SEMIOPEN"

def find_length(board, col, y_start, x_start, d_y, d_x):
    '''Compute the length of sequence of colour starting at (y_start, x_start)'''

    # If y_start or x_start are outside of the range of board, return 0.
    if y_start > (len(board)-1) or x_start > (len(board)-1) or x_start < 0 or y_start < 0:
        length = 0
        return length
    elif board[y_start][x_start] != col:
        length = 0
        return length
    else:
        length = 1
        y_start += d_y
        x_start += d_x
        for i in range(len(board)):
            if (min(y_start, x_start) < 0) or (max(y_start, x_start) > (len(board)-1)):
                return length
            elif board[y_start][x_start] != col:
                return length
            else :
                length += 1
            y_start += d_y
            x_start += d_x

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    ''' Return the count of the number of open and semiopen sequences in a row of board. '''
    ''' Assume length is greater than 2 and (y_start, x_start) is the edge of the board. '''
    ''' A row is either a vertical or horizontal or diagonal sequence of squares in the board. '''

    open_seq_count = 0
    semi_open_seq_count = 0

    for i in range (len(board)):
        # Compute the length of the sequence at (y_start, x_start) proceeding in the direction (d_y, d_x).
        present_length = find_length(board, col, y_start, x_start, d_y, d_x)
        if y_start > len(board) or x_start > len(board) or x_start < 0 or y_start < 0:
            break
        elif present_length == 0:
            y_start += d_y
            x_start += d_x
        elif present_length < length:
            y_start += d_y
            x_start += d_x
        elif present_length == length:
            y_end = y_start + (d_y*(length-1))
            x_end = x_start + (d_x*(length-1))
            if is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                open_seq_count += 1
            elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                semi_open_seq_count += 1
            y_start = y_end + d_y
            x_start = x_end + d_x
        else:
            y_start += ((present_length)*d_y)
            x_start += ((present_length)*d_x)
    return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length):
    '''Return a tuple of the number of open and semi open sequences of length length and colour col in the board board.'''

    open_seq_count, semi_open_seq_count = 0, 0

    for i in range (len(board)):
        res1 = detect_row(board, col, i, 0, length, 0, 1) # Check for Horizontal Rows
        res2 = detect_row(board, col, 0, i, length, 1, 0) # Check for Vertical Rows
        open_seq_count += res1[0] + res2[0]
        semi_open_seq_count += res1[1] + res2[1]

    # Check for Diagonal Rows from Left to Right [in direction (1, 1)]
    for n in range (len(board)):
        res3 = detect_row(board, col, n, 0, length, 1, 1) # Check for diagonals below (0, 0) to (7,7) inclusive
        open_seq_count += res3[0]
        semi_open_seq_count += res3[1]
    for m in range (1,len(board)): # Check for diagonals above the (0, 0) to (7,7) diagonal
        res4 = detect_row(board, col, 0, m, length, 1, 1)
        open_seq_count += res4[0]
        semi_open_seq_count += res4[1]

    # Check for Diagonal Rows from Right to Left [in direction (1, -1)]
    for k in range (len(board)):
        res5 = detect_row(board, col, 0, k, length, 1, -1) # Check for diagonals above (7,0) to (0,7) inclusive
        open_seq_count += res5[0]
        semi_open_seq_count += res5[1]
    for l in range (1,len(board)): # Check for diagonals below the (7,0) to (0,7) diagonal
        res6 = detect_row(board, col, l, len(board) - 1, length, 1, -1)
        open_seq_count += res6[0]
        semi_open_seq_count += res6[1]

    return open_seq_count, semi_open_seq_count

def check_row(board, col, y_start, x_start, length, d_y, d_x):
    '''Count the number of open, semi-open and closed sequences in row proeceeding in direction d_y, d_x'''

    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0

    for i in range (len(board)):
        # Compute the length of the sequence at (y_start, x_start) proceeding in the direction (d_y, d_x).
        present_length = find_length(board, col, y_start, x_start, d_y, d_x)
        if y_start > len(board) or x_start > len(board) or x_start < 0 or y_start < 0:
            break
        elif present_length == 0:
            y_start += d_y
            x_start += d_x
        elif present_length < length:
            y_start += d_y
            x_start += d_x
        elif present_length == length:
            y_end = y_start + (d_y*(length-1))
            x_end = x_start + (d_x*(length-1))
            if is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                open_seq_count += 1
            elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                semi_open_seq_count += 1
            elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                closed_seq_count += 1
            y_start = y_end + d_y
            x_start = x_end + d_x
        else:
            y_start += ((present_length)*d_y)
            x_start += ((present_length)*d_x)
    return open_seq_count, semi_open_seq_count, closed_seq_count

def check_rows(board, col):
    '''Return a tuple of the number of open and semi open and closed sequences of length 5 and colour col in the board board to determine whether white or black has won.'''

    open_seq_count, semi_open_seq_count, closed_seq_count = 0, 0, 0

    for i in range (len(board)):
        res1 = check_row(board, col, i, 0, 5, 0, 1) # Check for Horizontal Rows
        res2 = check_row(board, col, 0, i, 5, 1, 0) # Check for Vertical Rows
        open_seq_count += res1[0] + res2[0]
        semi_open_seq_count += res1[1] + res2[1]
        closed_seq_count += res1[2] + res2[2]

    # Check for Diagonal Rows from Left to Right [in direction (1, 1)]
    for n in range (len(board)):
        res3 = check_row(board, col, n, 0, 5, 1, 1) # Check for diagonals below (0, 0) to (7,7) inclusive
        open_seq_count += res3[0]
        semi_open_seq_count += res3[1]
        closed_seq_count += res3[2]

    for m in range (1,len(board)): # Check for diagonals above the (0, 0) to (7,7) diagonal
        res4 = check_row(board, col, 0, m, 5, 1, 1)
        open_seq_count += res4[0]
        semi_open_seq_count += res4[1]
        closed_seq_count += res4[2]

    # Check for Diagonal Rows from Right to Left [in direction (1, -1)]
    for k in range (len(board)):
        res5 = check_row(board, col, 0, k, 5, 1, -1) # Check for diagonals above (7,0) to (0,7) inclusive
        open_seq_count += res5[0]
        semi_open_seq_count += res5[1]
        closed_seq_count += res5[2]

    for l in range (1,len(board)): # Check for diagonals below the (7,0) to (0,7) diagonal
        res6 = check_row(board, col, l, len(board) - 1, 5, 1, -1)
        open_seq_count += res6[0]
        semi_open_seq_count += res6[1]
        closed_seq_count += res6[2]

    return open_seq_count, semi_open_seq_count, closed_seq_count

def search_max(board):
    '''Return the optimum move (move_y, move_x) for "b" that maximizes the score of the board'''

    duplicate_board = []
    present_score = score(board)
    move_y, move_x = -1,-1

    # Create a deep copy of the board to prevent from modifying the contents of the board.
    for sublist in board:
        duplicate_board.append(sublist[:])

    # Find move_y, move_x for "b" that maximizes the score of the board.
    for i in range(len(duplicate_board)):
        for m in range(len(duplicate_board[0])):
            # If the current block on the board is empty compute the score of board if a black stone is placed.
            if duplicate_board[i][m] == " ":
                duplicate_board[i][m] = "b"
                check_score = score(duplicate_board)
                # If the new score of the board with is greater than present score, modify the optimum move.
                if check_score > present_score:
                    present_score = check_score
                    move_y, move_x = i, m
                # Revert to the original duplicate board
                duplicate_board[i][m] = " "
            # If the current block of the board is not empty, proceed to the next iteration.
            else:
                continue

    # If such a move exists, return move_y, move_x
    if move_y != -1 and move_x != -1:
        return move_y, move_x
    # If no such move exists, return any empty square in the board (i.e. the first empty square in board).
    else:
        for k in range(len(duplicate_board)):
            for l in range(len(duplicate_board[0])):
                if duplicate_board[k][l] == " ":
                    return k, l

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    '''If there exists rows of length 5 and colour "w" or "b" return the result of game. Else if board is full, return Draw. Otherwise if neither player has won or draw continue playing.'''

    # Compute the number of open, semi-open and closed sequences of length 5 for colour "b" and "w".
    res1 = check_rows(board, "w")
    res2 = check_rows(board, "b")

    # If a sequence of length 5 and colour col exists, return the winner.
    if res2[0]>0 or res2[1]>0 or res2[2]>0:
        return "Black won"
    elif res1[0]>0 or res1[1]>0 or res1[2]>0:
        return "White won"
    elif is_complete(board) == True:
        return "Draw"
    else:
        return "Continue playing"

def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x

### SAMPLE TEST CASES (USE AS REFERENCE)

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


if __name__ == '__main__':
    # board = make_empty_board(8)
    # board[4][0] = "w"
    # board[3][1] = "w"
    # board[2][2] = "w"
    # board[1][3] = "w"
    # board[0][4] = "w"
    # board[0][2] = "w"
    # board[1][2] = "w"
    # board[3][2] = "w"
    # board[4][2] = "w"
    # board[7][1] = "w"
    # board[6][2] = "w"
    # board[5][3] = "w"
    # board[4][4] = "w"
    # board[3][5] = "w"
    # board[4][5] = "w"
    # board[5][5] = "w"
    # board[6][5] = "w"
    # board[7][5] = "w"
    # print_board(board)
    # print(check_rows(board, "w"))
    # print(search_max(board))
    # print(is_win(board))
    # print(score(board))
    easy_testset_for_main_functions()
    some_tests()
    # play_gomoku(8)
