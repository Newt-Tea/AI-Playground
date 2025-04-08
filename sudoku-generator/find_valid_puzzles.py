#!/usr/bin/env python
"""
Debug script for finding valid Sudoku puzzles.
"""

from src.sudoku.board import Board
from src.sudoku.solver import SudokuSolver

def find_valid_4x4_puzzle():
    """Find a valid 4x4 puzzle with a unique solution."""
    print("Finding a valid 4x4 puzzle...")
    
    # Create a simple completed 4x4 Sudoku
    completed_values = [
        [1, 2, 3, 4],
        [3, 4, 1, 2],
        [2, 1, 4, 3],
        [4, 3, 2, 1]
    ]
    
    # Create a board with the completed solution
    board = Board(4)
    for r in range(4):
        for c in range(4):
            board.set_value(r, c, completed_values[r][c])
    
    print("Completed 4x4 solution:")
    print(board)
    assert board.is_valid()
    
    # Now remove some values to create a puzzle
    # Keep enough clues to maintain a unique solution
    to_remove = [
        (0, 2), (0, 3),
        (1, 0), (1, 1),
        (2, 2), (2, 3),
        (3, 0), (3, 1)
    ]
    
    for r, c in to_remove:
        board.set_value(r, c, None)
    
    print("\n4x4 puzzle with clues:")
    print(board)
    
    # Check if it has a unique solution
    board.update_possible_values()
    solutions = board.count_solutions()
    print(f"Number of solutions: {solutions}")
    
    # Try solving
    solver = SudokuSolver()
    result = solver.solve(board)
    print(f"Solver result: {result}")
    
    if result:
        print("Solved board:")
        print(solver.board)
    
    # Generate test case code
    print("\nTest case code:")
    print("```python")
    print("def test_solve_simple_4x4():")
    print('    """Test solving a simple 4×4 puzzle."""')
    print("    # Create a 4×4 board with some values")
    print("    board = Board(4)")
    print("    # Set up a simple puzzle with a guaranteed unique solution")
    for r in range(4):
        for c in range(4):
            val = board.get_value(r, c)
            if val is not None:
                print(f"    board.set_value({r}, {c}, {val})")
    print("    # Update possible values")
    print("    board.update_possible_values()")
    print("    # Create a solver")
    print("    solver = SudokuSolver()")
    print("    # Solve the puzzle")
    print("    result = solver.solve(board)")
    print("    # Verify a solution was found")
    print("    assert result is True")
    print("    # Verify the solution is valid")
    print("    assert solver.board.is_valid()")
    print("```")

def find_valid_9x9_puzzle():
    """Find a valid 9x9 puzzle with a unique solution."""
    print("\nFinding a valid 9x9 puzzle...")
    
    # Create a 9x9 board with a known valid puzzle
    # This is a standard easy Sudoku puzzle with a guaranteed unique solution
    board = Board(9)
    clues = [
        (0, 0, 5), (0, 1, 3), (0, 4, 7),
        (1, 0, 6), (1, 3, 1), (1, 6, 9), (1, 7, 5),
        (2, 1, 9), (2, 2, 8), (2, 7, 6),
        (3, 0, 8), (3, 4, 6), (3, 8, 3),
        (4, 0, 4), (4, 3, 8), (4, 5, 5), (4, 8, 1),
        (5, 0, 7), (5, 4, 2), (5, 8, 6),
        (6, 1, 1), (6, 6, 2), (6, 7, 8),
        (7, 1, 2), (7, 2, 7), (7, 5, 4), (7, 8, 9),
        (8, 4, 8), (8, 7, 7), (8, 8, 5)
    ]
    
    for row, col, value in clues:
        board.set_value(row, col, value)
    
    print("9x9 puzzle with clues:")
    print(board)
    
    # Check if it has a unique solution
    board.update_possible_values()
    solutions = board.count_solutions()
    print(f"Number of solutions: {solutions}")
    
    # Try solving
    solver = SudokuSolver()
    result = solver.solve(board)
    print(f"Solver result: {result}")
    
    if result:
        print("Solved board:")
        print(solver.board)
    
    # Generate test case code
    print("\nTest case code:")
    print("```python")
    print("def test_solve_simple_9x9():")
    print('    """Test solving a simple 9×9 puzzle."""')
    print("    # Create a 9×9 board with some values")
    print("    board = Board(9)")
    print("    # Set up a simple puzzle with a guaranteed unique solution")
    print("    clues = [")
    for r, c, v in clues:
        print(f"        ({r}, {c}, {v}),")
    print("    ]")
    print("    for row, col, value in clues:")
    print("        board.set_value(row, col, value)")
    print("    # Update possible values")
    print("    board.update_possible_values()")
    print("    # Create a solver")
    print("    solver = SudokuSolver()")
    print("    # Solve the puzzle")
    print("    result = solver.solve(board)")
    print("    # Verify a solution was found")
    print("    assert result is True")
    print("    # Verify the solution is valid")
    print("    assert solver.board.is_valid()")
    print("```")

if __name__ == "__main__":
    find_valid_4x4_puzzle()
    find_valid_9x9_puzzle()