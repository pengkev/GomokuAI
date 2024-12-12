def is_empty(board):
    for row in board:
        for col in row:
            if col != " ":
                return False
    return True
    
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    max_y = len(board) - 1
    max_x = len(board[0]) - 1

    # Helper function to check if a position is within bounds
    def is_within_bounds(y, x):
        return 0 <= y <= max_y and 0 <= x <= max_x

    #vertically
    if (d_y, d_x) == (1, 0):
        above = is_within_bounds(y_end + 1, x_end) and board[y_end + 1][x_end] == " "
        below = is_within_bounds(y_end - length, x_end) and board[y_end - length][x_end] == " "
        if above and below:
            return "OPEN"
        elif above or below:
            return "SEMIOPEN"
        else:
            return "CLOSED"

    #sideways
    if (d_y, d_x) == (0, 1):
        right = is_within_bounds(y_end, x_end + 1) and board[y_end][x_end + 1] == " "
        left = is_within_bounds(y_end, x_end - length) and board[y_end][x_end - length] == " "
        if right and left:
            return "OPEN"
        elif right or left:
            return "SEMIOPEN"
        else:
            return "CLOSED"

    #rl diagonal /
    elif (d_y, d_x) == (1, -1):
        top_right = is_within_bounds(y_end + 1, x_end - 1) and board[y_end + 1][x_end - 1] == " "
        bottom_left = is_within_bounds(y_end - length, x_end + length) and board[y_end - length][x_end + length] == " "
        if top_right and bottom_left:
            return "OPEN"
        elif top_right or bottom_left:
            return "SEMIOPEN"
        else:
            return "CLOSED"

    #lr diagonal \
    elif (d_y, d_x) == (1, 1):
        bottom_right = is_within_bounds(y_end + 1, x_end + 1) and board[y_end + 1][x_end + 1] == " "
        top_left = is_within_bounds(y_end - length, x_end - length) and board[y_end - length][x_end - length] == " "
        if bottom_right and top_left:
            return "OPEN"
        elif bottom_right or top_left:
            return "SEMIOPEN"
        else:
            return "CLOSED"

    

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    y, x = y_start, x_start

    #go along direction
    while 0 <= y < len(board) and 0 <= x < len(board[0]):
        #extend sequence
        seq_len = 0
        while (0 <= y < len(board) and 0 <= x < len(board[0]) and 
               board[y][x] == col):
            seq_len += 1
            y += d_y
            x += d_x
            
        if seq_len == length:
            y_end = y - d_y
            x_end = x - d_x
            
            if is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                open_seq_count += 1
            elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                semi_open_seq_count += 1

        #goto next cell of colour col
        while (0 <= y < len(board) and 0 <= x < len(board[0]) and 
               board[y][x] != col):
            y += d_y
            x += d_x
            
    return (open_seq_count, semi_open_seq_count)

    
def detect_rows(board, col, length):
    open_count = 0
    semi_open_count = 0
    rows = len(board)
    cols = len(board[0])

    #horizontal
    for y in range(rows):
        open_seq, semi_open_seq = detect_row(board, col, y, 0, length, 0,1)
        open_count += open_seq
        semi_open_count += semi_open_seq
    #vertical
    for x in range(cols):
        open_seq, semi_open_seq = detect_row(board, col, 0, x, length, 1,0)
        open_count += open_seq
        semi_open_count += semi_open_seq
    #leftright
    for y in range(rows):
        open_seq, semi_open_seq = detect_row(board, col, y, 0, length, 1,1)
        open_count += open_seq
        semi_open_count += semi_open_seq
    for x in range(1, cols):
        open_seq, semi_open_seq = detect_row(board, col, 0, x, length, 1,1)
        open_count += open_seq
        semi_open_count += semi_open_seq
    #rightleft
    for y in range(rows):
        open_seq, semi_open_seq = detect_row(board, col, y, cols - 1, length, 1,-1)
        open_count += open_seq
        semi_open_count += semi_open_seq
    for x in range(cols - 1):
        open_seq, semi_open_seq = detect_row(board, col, 0, x, length, 1,-1)
        open_count += open_seq
        semi_open_count += semi_open_seq

    return open_count, semi_open_count

    
def search_max(board):
    (move_y,move_x) = (0,0)
    highest_score = 0
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == " ":
                board[y][x] = "b"
                if score(board) > highest_score:
                    highest_score = score(board)
                    (move_y,move_x) = (y,x)
                board[y][x] = " "
    return (move_y, move_x)
    
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
    for r in range(len(board)):
        for c in range(len(board[r])-4):
            #horizontal win
            if board[r][c] == "b" and board[r][c+1] == "b" and board[r][c+2] == "b" and board[r][c+3] == "b" and board[r][c+4] == "b":
                if (c > 0 and board[r][c-1] == "b") or (c + 5 < len(board[r]) and board[r][c+5] == "b"):
                    continue
                return "Black won"
            elif board[r][c] == "w" and board[r][c+1] == "w" and board[r][c+2] == "w" and board[r][c+3] == "w" and board[r][c+4] == "w":
                if (c > 0 and board[r][c-1] == "w") or (c + 5 < len(board[r]) and board[r][c+5] == "w"):
                    continue
                return "White won"
                    
    for r in range(len(board)-4):
        for c in range(len(board[r])):
            #vertical win
            if board[r][c] == "b" and board[r+1][c] == "b" and board[r+2][c] == "b" and board[r+3][c] == "b" and board[r+4][c] == "b":
                if (r > 0 and board[r-1][c] == "b") or (r + 5 < len(board) and board[r+5][c] == "b"):
                    continue
                return "Black won"
            elif board[r][c] == "w" and board[r+1][c] == "w" and board[r+2][c] == "w" and board[r+3][c] == "w" and board[r+4][c] == "w":
                if (r > 0 and board[r-1][c] == "w") or (r + 5 < len(board) and board[r+5][c] == "w"):
                    continue
                return "White won"
            
    # Check diagonal "\" wins
    for r in range(len(board) - 4):
        for c in range(len(board[r]) - 4):
            if board[r][c] == "b" and board[r+1][c+1] == "b" and board[r+2][c+2] == "b" and board[r+3][c+3] == "b" and board[r+4][c+4] == "b":
                if (r > 0 and c > 0 and board[r-1][c-1] == "b") or (r + 5 < len(board) and c + 5 < len(board[r]) and board[r+5][c+5] == "b"):
                    continue
                return "Black won"
            elif board[r][c] == "w" and board[r+1][c+1] == "w" and board[r+2][c+2] == "w" and board[r+3][c+3] == "w" and board[r+4][c+4] == "w":
                if (r > 0 and c > 0 and board[r-1][c-1] == "w") or (r + 5 < len(board) and c + 5 < len(board[r]) and board[r+5][c+5] == "w"):
                    continue
                return "White won"

    # Check diagonal "/" wins
    for r in range(4, len(board)):
        for c in range(len(board[r]) - 4):
            if board[r][c] == "b" and board[r-1][c+1] == "b" and board[r-2][c+2] == "b" and board[r-3][c+3] == "b" and board[r-4][c+4] == "b":
                if (r < len(board) - 1 and c > 0 and board[r+1][c-1] == "b") or (r - 5 >= 0 and c + 5 < len(board[r]) and board[r-5][c+5] == "b"):
                    continue
                return "Black won"
            elif board[r][c] == "w" and board[r-1][c+1] == "w" and board[r-2][c+2] == "w" and board[r-3][c+3] == "w" and board[r-4][c+4] == "w":
                if (r < len(board) - 1 and c > 0 and board[r+1][c-1] == "w") or (r - 5 >= 0 and c + 5 < len(board[r]) and board[r-5][c+5] == "w"):
                    continue
                return "White won"            
    #check if full
    fullornot = True
    for row in board:
        if " " in row:
            fullornot = False
            break
    if fullornot:
        return "Draw"
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
def run_corner_case_tests():
    print("Running corner case tests...\n")

    # Test `is_empty` function corner cases
    board = make_empty_board(8)
    board[0][0] = 'w'
    if not is_empty(board):
        print("CORNER CASE for is_empty PASSED (single stone)")
    else:
        print("CORNER CASE for is_empty FAILED (single stone)")

    # Test `is_bounded` function corner cases
    # Semi-open at edge
    board = make_empty_board(8)
    put_seq_on_board(board, 1, 0, 0, 1, 3, "w")
    if is_bounded(board, 1, 2, 3, 0, 1) == 'SEMIOPEN':
        print("CORNER CASE for is_bounded PASSED (semi-open at edge)")
    else:
        print("CORNER CASE for is_bounded FAILED (semi-open at edge)")

    # Closed at both edges
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 0, 0, 1, 8, "b")
    if is_bounded(board, 0, 7, 8, 0, 1) == 'CLOSED':
        print("CORNER CASE for is_bounded PASSED (closed at both edges)")
    else:
        print("CORNER CASE for is_bounded FAILED (closed at both edges)")

    # Single open stone
    board = make_empty_board(8)
    board[4][4] = 'b'
    if is_bounded(board, 4, 4, 1, 0, 1) == 'OPEN':
        print("CORNER CASE for is_bounded PASSED (single open stone)")
    else:
        print("CORNER CASE for is_bounded FAILED (single open stone)")

    # Test `detect_row` function corner cases
    # Sequence spanning multiple rows
    board = make_empty_board(8)
    put_seq_on_board(board, 6, 0, -1, 1, 4, "w")
    if detect_row(board, "w", 6, 0, 4, -1, 1) == (1, 0):
        print("CORNER CASE for detect_row PASSED (spanning rows)")
    else:
        print("CORNER CASE for detect_row FAILED (spanning rows)")

    # Adjacent sequences
    board = make_empty_board(8)
    put_seq_on_board(board, 2, 1, 0, 1, 3, "w")
    put_seq_on_board(board, 2, 5, 0, 1, 3, "w")
    if detect_row(board, "w", 2, 0, 3, 0, 1) == (2, 0):
        print("CORNER CASE for detect_row PASSED (adjacent sequences)")
    else:
        print("CORNER CASE for detect_row FAILED (adjacent sequences)")

    # Isolated stone
    board = make_empty_board(8)
    board[4][4] = 'w'
    if detect_row(board, "w", 4, 4, 2, 0, 1) == (0, 0):
        print("CORNER CASE for detect_row PASSED (isolated stone)")
    else:
        print("CORNER CASE for detect_row FAILED (isolated stone)")

    # Test `detect_rows` function corner cases
    # Mixed row lengths
    board = make_empty_board(8)
    put_seq_on_board(board, 1, 0, 0, 1, 3, "w")
    put_seq_on_board(board, 2, 0, 0, 1, 4, "w")
    if detect_rows(board, "w", 3) == (1, 0) and detect_rows(board, "w", 4) == (1, 0):
        print("CORNER CASE for detect_rows PASSED (mixed row lengths)")
    else:
        print("CORNER CASE for detect_rows FAILED (mixed row lengths)")

    # Corner edge sequence
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 4, 1, -1, 4, "b")
    if detect_rows(board, "b", 4) == (1, 0):
        print("CORNER CASE for detect_rows PASSED (corner edge)")
    else:
        print("CORNER CASE for detect_rows FAILED (corner edge)")

    # Test `search_max` function corner cases
    # Board with equal row lengths for both colors
    board = make_empty_board(8)
    put_seq_on_board(board, 1, 0, 0, 1, 3, "w")
    put_seq_on_board(board, 5, 0, 0, 1, 3, "b")
    if search_max(board) is not None:
        print("CORNER CASE for search_max PASSED (equal row lengths)")
    else:
        print("CORNER CASE for search_max FAILED (equal row lengths)")

    # No winning moves on the board
    board = make_empty_board(8)
    if search_max(board) is None:
        print("CORNER CASE for search_max PASSED (no winning moves)")
    else:
        print("CORNER CASE for search_max FAILED (no winning moves)")

    print("\nAll corner case tests completed.")

# Run all corner case tests
run_corner_case_tests()


  
            
#if __name__ == '__main__':
#    play_gomoku(8)
    
easy_testset_for_main_functions()
