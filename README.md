# Gomoku Game AI

## Overview

This project implements a Gomoku game with basic AI functionality. Gomoku, also known as Five in a Row, is a strategy board game where two players take turns placing stones (black and white) on a grid. The objective is to form an unbroken line of five stones horizontally, vertically, or diagonally.

The program includes:

1. Core game mechanics (winning conditions, board evaluation).
2. A simple AI that determines optimal moves.
3. Functions to analyze open and semi-open sequences of stones.

## How the Game Works

- **Board:** A 2D grid where each position can hold either a black stone ('b'), a white stone ('w'), or remain empty (' ').
- **Players:** The two players alternate turns, placing their stones to achieve the goal of aligning 5 stones in a row.
- **Winning Condition:** The first player to achieve a sequence of exactly 5 stones (without being blocked on both ends) wins.

## Key Features

### 1. Core Game Functions

- **`is_empty(board)`**: Checks if the board is completely empty.
- **`is_bounded(board, y_end, x_end, length, d_y, d_x)`**: Determines if a sequence of stones is "OPEN," "SEMIOPEN," or "CLOSED."
- **`detect_row(board, col, y_start, x_start, length, d_y, d_x)`**: Detects sequences of a specific length in a row or diagonal direction.
- **`detect_rows(board, col, length)`**: Summarizes all open and semi-open sequences of a specific length for a given color.

### 2. AI Move Search

- **`search_max(board)`**: Determines the best move for the AI by simulating placements and evaluating the resulting board's score.
- **`score(board)`**: Evaluates the board based on open and semi-open rows for both players, assigning points for various configurations.

### 3. Winning Condition

- **`is_win(board)`**: Checks if there is a winning configuration on the board for either black ('b') or white ('w').

## Scoring System

The scoring function prioritizes moves that create or block winning sequences:

- **Winning Moves:** Immediate wins have the highest score.
- **Blocking Opponent Wins:** The AI prioritizes preventing the opponent from winning.
- **Open and Semi-Open Rows:** Longer sequences of stones (4, 3, etc.) are valued based on their openness.

| Sequence Type | Points |
| ------------- | ------ |
| Open 5        | Wins   |
| Semi-open 5   | Wins   |
| Open 4        | +500   |
| Semi-open 4   | +50    |
| Open 3        | +50    |
| Semi-open 3   | +10    |

## Program Flow

1. **Initialization:** The board is set up as a 2D grid with empty cells (' ').
2. **Move Execution:** The AI searches for the best move using the `search_max` function.
3. **Evaluation:** After each move, the program checks for a winning condition using `is_win`.
4. **Game End:** If a player wins, the program returns the result ("Black won" or "White won").

## Running the Code

The program can be run in a Python environment. Ensure Python 3.x is installed.

### Example Usage

```python
board = [[' ' for _ in range(8)] for _ in range(8)]  # Initialize an 8x8 board
board[3][3] = 'b'
board[3][4] = 'b'
board[3][5] = 'b'
board[3][6] = 'b'

print(is_win(board))  # Checks for winning condition
move = search_max(board)
print("Best move for AI:", move)
```

### Output

The program will determine and print the best move for the AI and identify if there is a winning sequence on the board.

## Future Improvements

- Implement a more sophisticated AI using minimax or alpha-beta pruning.
- Add a graphical user interface (GUI) for interactive play.
- Enhance the scoring function for better move evaluations.

## Dependencies

- Python 3.x

## Author

- **Kevin Peng**

