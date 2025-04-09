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


__all__ = ['Board', 'Cell', 'SudokuSolver', 'SudokuGenerator', 'Benchmark', 'cli']



