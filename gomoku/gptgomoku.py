def is_bounded(board, y_end, x_end, length, d_y, d_x):
    """Determines if a sequence is open, semi-open, or closed."""
    y_start = y_end - (length - 1) * d_y
    x_start = x_end - (length - 1) * d_x
    board_size = len(board)
    
    # Check boundaries for the start and end of the sequence
    start_blocked = (
        y_start - d_y < 0 or y_start - d_y >= board_size or
        x_start - d_x < 0 or x_start - d_x >= board_size or
        board[y_start - d_y][x_start - d_x] != " "
    )
    
    end_blocked = (
        y_end + d_y < 0 or y_end + d_y >= board_size or
        x_end + d_x < 0 or x_end + d_x >= board_size or
        board[y_end + d_y][x_end + d_x] != " "
    )
    
    if not start_blocked and not end_blocked:
        return "OPEN"
    elif start_blocked ^ end_blocked:
        return "SEMIOPEN"
    else:
        return "CLOSED"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    """Detects open and semi-open rows of a given length starting from a position."""
    open_seq_count = 0
    semi_open_seq_count = 0
    board_size = len(board)
    
    y, x = y_start, x_start
    while 0 <= y < board_size and 0 <= x < board_size:
        # Check if there is a sequence of `length` with color `col`
        sequence_found = True
        for i in range(length):
            if not (0 <= y + i * d_y < board_size and 0 <= x + i * d_x < board_size):
                sequence_found = False
                break
            if board[y + i * d_y][x + i * d_x] != col:
                sequence_found = False
                break
        
        if sequence_found:
            y_end = y + (length - 1) * d_y
            x_end = x + (length - 1) * d_x
            bound_status = is_bounded(board, y_end, x_end, length, d_y, d_x)
            if bound_status == "OPEN":
                open_seq_count += 1
            elif bound_status == "SEMIOPEN":
                semi_open_seq_count += 1
            y += length * d_y
            x += length * d_x
        else:
            y += d_y
            x += d_x
    
    return open_seq_count, semi_open_seq_count

def detect_rows(board, col, length):
    """Detects rows with open and semi-open sequences of the given length across the entire board."""
    open_seq_count, semi_open_seq_count = 0, 0
    board_size = len(board)
    
    # Check all rows, columns, and diagonals
    for i in range(board_size):
        # Horizontal
        open_count, semi_count = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count += open_count
        semi_open_seq_count += semi_count
        # Vertical
        open_count, semi_count = detect_row(board, col, 0, i, length, 1, 0)
        open_seq_count += open_count
        semi_open_seq_count += semi_count
    
    # Diagonals
    for i in range(board_size):
        # Down-right diagonal
        open_count, semi_count = detect_row(board, col, i, 0, length, 1, 1)
        open_seq_count += open_count
        semi_open_seq_count += semi_count
        open_count, semi_count = detect_row(board, col, 0, i, length, 1, 1)
        open_seq_count += open_count
        semi_open_seq_count += semi_count
        # Down-left diagonal
        open_count, semi_count = detect_row(board, col, i, board_size - 1, length, 1, -1)
        open_seq_count += open_count
        semi_open_seq_count += semi_count
        open_count, semi_count = detect_row(board, col, 0, board_size - 1 - i, length, 1, -1)
        open_seq_count += open_count
        semi_open_seq_count += semi_count
    
    return open_seq_count, semi_open_seq_count

def is_win(board):
    """Checks if there is a winning sequence on the board."""
    for col in ['b', 'w']:
        for i in range(len(board)):
            for j in range(len(board)):
                # Check if there's a five-in-a-row in any direction
                if detect_row(board, col, i, j, 5, 0, 1)[0] > 0:
                    return f"{col.upper()} won"
                if detect_row(board, col, i, j, 5, 1, 0)[0] > 0:
                    return f"{col.upper()} won"
                if detect_row(board, col, i, j, 5, 1, 1)[0] > 0:
                    return f"{col.upper()} won"
                if detect_row(board, col, i, j, 5, 1, -1)[0] > 0:
                    return f"{col.upper()} won"
    
    # Check if the board is completely filled
    if all(board[i][j] != " " for i in range(len(board)) for j in range(len(board[0]))):
        return "Draw"
    
    return "Continue playing"

def is_empty(board):
    """Checks if the board is empty, assuming empty cells are represented by ' '."""
    return all(cell == " " for row in board for cell in row)

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
        
def search_max(board, ai_color="b"):
    """Finds the best move for the AI by maximizing the score function."""
    max_score = -float('inf')
    best_move = None
    
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == " ":
                # Try the move
                board[y][x] = ai_color
                current_score = score(board)
                # Undo the move
                board[y][x] = " "
                
                # Update if this move has a higher score
                if current_score > max_score:
                    max_score = current_score
                    best_move = (y, x)
    
    return best_move if best_move is not None else (0, 0)  # Fallback if no move is found


        
    
def play_gomoku(board_size):
    """Main game loop for Gomoku."""
    board = make_empty_board(board_size)
    
    while True:
        print_board(board)
        
        # AI move
        if is_empty(board):
            move_y, move_x = board_size // 2, board_size // 2
        else:
            move_y, move_x = search_max(board)
        
        print(f"Computer move: ({move_y}, {move_x})")
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["B won", "W won", "Draw"]:
            print(game_res)
            break
        
        # Player move
        while True:
            try:
                move_y = int(input("Enter y-coordinate: "))
                move_x = int(input("Enter x-coordinate: "))
                if board[move_y][move_x] == " ":
                    board[move_y][move_x] = "w"
                    break
                else:
                    print("Cell occupied! Choose another move.")
            except (ValueError, IndexError):
                print("Invalid input. Please enter valid coordinates.")
        
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["Black won", "White won", "Draw"]:
            print(game_res)
            break                    
          
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


  
            
if __name__ == '__main__':
    play_gomoku(8)
        