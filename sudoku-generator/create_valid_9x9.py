#!/usr/bin/env python
"""
Create a valid 9x9 Sudoku puzzle with a guaranteed solution.
"""

from src.sudoku.board import Board
from src.sudoku.solver import SudokuSolver

def create_valid_9x9():
    """Create a valid 9x9 puzzle for testing."""
    # This is a famous easy Sudoku puzzle with a unique solution
    initial_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    # Create the board
    board = Board(9)
    
    # Fill in the initial values
    clues = []
    for r in range(9):
        for c in range(9):
            if initial_board[r][c] != 0:
                board.set_value(r, c, initial_board[r][c])
                clues.append((r, c, initial_board[r][c]))
    
    print("Initial board:")
    print(board)
    
    # Check if it has a solution using count_solutions
    board.update_possible_values()
    solutions = board.count_solutions()
    print(f"Number of solutions according to count_solutions: {solutions}")
    
    # Try to solve using SudokuSolver
    solver = SudokuSolver()
    result = solver.solve(board)
    print(f"Solver result: {result}")
    
    if result:
        print("Solution found:")
        print(solver.board)
        
        # Generate test code
        print("\nTest code:")
        print("```python")
        print("def test_solve_simple_9x9():")
        print('    """Test solving a simple 9×9 puzzle."""')
        print("    # Create a 9×9 board")
        print("    board = Board(9)")
        print("    ")
        print("    # Set up a simple puzzle with a unique solution")
        print("    clues = [")
        for r, c, v in clues:
            print(f"        ({r}, {c}, {v}),")
        print("    ]")
        print("    ")
        print("    for row, col, value in clues:")
        print("        board.set_value(row, col, value)")
        print("    ")
        print("    # Create a solver")
        print("    solver = SudokuSolver()")
        print("    ")
        print("    # Solve the puzzle")
        print("    result = solver.solve(board)")
        print("    ")
        print("    # Verify a solution was found")
        print("    assert result is True")
        print("    ")
        print("    # Verify the solution is valid")
        print("    assert solver.board.is_valid()")
        print("```")

if __name__ == "__main__":
    create_valid_9x9()