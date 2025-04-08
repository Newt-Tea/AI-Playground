"""
Sudoku Generator and Solver Package

This package contains modules for creating, solving, and validating Sudoku puzzles.
It serves as the main entry point for the Sudoku generator project.

Structure:
    - sudoku: Core module containing the implementation of Sudoku components
        - cell: Contains the Cell class for representing individual Sudoku cells
        - board: Contains the Board class for representing the full Sudoku grid

The implementation supports dynamically sized boards where the size is a perfect square
(4x4, 9x9, 16x16, etc.), and ensures generated puzzles have unique solutions.

Example usage:
    >>> from src.sudoku.board import Board
    >>> # Create a 9x9 Sudoku board
    >>> board = Board(9)
    >>> # Set some initial values
    >>> board.set_value(0, 0, 5)
    >>> # Print the board
    >>> board.print_grid()
"""

# Import submodules for easier access
from src import sudoku