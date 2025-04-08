#!/usr/bin/env python
"""
Debug script for testing the Sudoku solver.
"""

from src.sudoku.board import Board
from src.sudoku.solver import SudokuSolver

def debug_4x4_puzzle():
    """Test the 4x4 puzzle from the failing test."""
    print("Testing 4x4 puzzle...")
    board = Board(4)
    
    # Set up the simple puzzle from the test
    board.set_value(0, 0, 1)
    board.set_value(0, 3, 4)
    board.set_value(1, 1, 3)
    board.set_value(2, 2, 2)
    board.set_value(3, 0, 4)
    board.set_value(3, 3, 1)
    
    print("Initial board:")
    print(board)
    
    # Update possible values
    board.update_possible_values()
    
    # Check if the puzzle has solutions
    solutions = board.count_solutions()
    print(f"Number of solutions: {solutions}")
    print(f"Is board valid: {board.is_valid()}")
    
    # Display possible values for empty cells
    print("\nPossible values for empty cells:")
    for r in range(4):
        for c in range(4):
            if board.is_empty(r, c):
                print(f"Cell ({r},{c}): {board.get_cell(r, c).possible_values}")
    
    # Try to solve the puzzle
    solver = SudokuSolver()
    result = solver.solve(board)
    
    print(f"\nSolver result: {result}")
    if result:
        print("Solved board:")
        print(solver.board)

def debug_9x9_puzzle():
    """Test the 9x9 puzzle from the failing test."""
    print("\nTesting 9x9 puzzle...")
    board = Board(9)
    
    # Set up the puzzle from the test
    clues = [
        (0, 0, 5), (0, 1, 3), (0, 4, 7),
        (1, 0, 6), (1, 3, 1), (1, 6, 9), (1, 7, 5),
        (2, 1, 9), (2, 2, 8), (2, 7, 6),
        (3, 0, 8), (3, 4, 6), (3, 8, 3),
        (4, 0, 4), (4, 3, 8), (4, 5, 3), (4, 8, 1),
        (5, 0, 7), (5, 4, 2), (5, 8, 6),
        (6, 1, 6), (6, 6, 2), (6, 7, 8),
        (7, 1, 2), (7, 2, 7), (7, 5, 4), (7, 8, 9),
        (8, 4, 8), (8, 7, 7), (8, 8, 5)
    ]
    
    for row, col, value in clues:
        board.set_value(row, col, value)
    
    print("Initial board:")
    print(board)
    
    # Update possible values
    board.update_possible_values()
    
    # Check if the puzzle has solutions
    solutions = board.count_solutions()
    print(f"Number of solutions: {solutions}")
    print(f"Is board valid: {board.is_valid()}")
    
    # Try to solve the puzzle
    solver = SudokuSolver()
    result = solver.solve(board)
    
    print(f"\nSolver result: {result}")
    if result:
        print("Solved board:")
        print(solver.board)

if __name__ == "__main__":
    debug_4x4_puzzle()
    debug_9x9_puzzle()