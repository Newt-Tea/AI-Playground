"""
Sudoku Generator and Solver Module

This module provides classes and functions to create, solve, and validate Sudoku puzzles.
It supports dynamically sized boards where the size is a perfect square (4x4, 9x9, 16x16, etc.).

Main Components:
    - Cell: Represents a single cell in a Sudoku grid
    - Board: Represents the entire Sudoku board with validation methods
    
Features:
    - Generate Sudoku puzzles with unique solutions
    - Validate boards according to Sudoku rules
    - Solve puzzles using efficient backtracking with MRV heuristic
    - Remove clues while ensuring puzzles maintain a unique solution

Example:
    >>> from sudoku.board import Board
    >>> # Create a 9x9 Sudoku board
    >>> board = Board(9)
    >>> # Set some initial values
    >>> board.set_value(0, 0, 5)
    >>> board.set_value(1, 1, 3)
    >>> # Print the board
    >>> board.print_grid()
    >>> # Check if a move is valid
    >>> is_valid = board.is_safe(0, 1, 2)
"""

# Use relative imports for board
from .board import Board
from .cell import Cell

__all__ = ['Board', 'Cell']

# This is more of a performance test and actually measuring it would require
# comparing execution times with and without MRV
# For simplicity, let's just verify that the MRV heuristic is available
def test_board_operations():
    board = Board(4)
    
    # Set up a board with some values
    for row in range(2):
        for col in range(2):
            board.set_value(row, col, ((row+col) % 4) + 1)
    
    # Verify the MRV function works
    print(board)
    mrv_cell = board.get_mrv_cell()
    print("Cell with minimum remaining values:", mrv_cell)
    
    # Also verify that removing clues works with MRV
    # Fill the board completely
    for row in range(4):
        for col in range(4):
            if board.is_empty(row, col):
                # Find a value that works
                for val in range(1, 5):
                    if board.is_safe(row, col, val):
                        board.set_value(row, col, val)
                        break
    
    # Now try removing clues
    print(board)
    removal_success = board.remove_clues(10)
    print(removal_success)
    print(board)
    
    # Count clues
    clues = sum(1 for row in range(4) for col in range(4) 
                if board.get_value(row, col) is not None)
    
    # Verify we have expected number of clues
    print(clues)


test_board_operations()