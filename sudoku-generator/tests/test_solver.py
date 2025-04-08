"""
Tests for the Solver class.
"""
import pytest
from src.sudoku.board import Board
from src.sudoku.solver import SudokuSolver

def test_solver_initialization():
    """Test solver initialization."""
    solver = SudokuSolver()
    assert solver is not None
    assert solver.board is None
    assert solver.solution_count == 0

def test_set_board():
    """Test setting a board to solve."""
    # Create a board
    board = Board(4)
    
    # Set some values
    board.set_value(0, 0, 1)
    board.set_value(1, 1, 2)
    
    # Create a solver
    solver = SudokuSolver()
    
    # Set the board
    solver.set_board(board)
    
    # Verify the board was set (as a deep copy)
    assert solver.board is not None
    assert solver.board is not board  # Should be a different object
    assert solver.board.get_value(0, 0) == 1
    assert solver.board.get_value(1, 1) == 2

def test_solve_no_board():
    """Test solving with no board set."""
    solver = SudokuSolver()
    
    # Attempt to solve with no board set
    with pytest.raises(ValueError) as e:
        solver.solve()
    
    assert "No board set" in str(e.value)

def test_print_solution_no_board():
    """Test printing solution with no board set."""
    solver = SudokuSolver()
    
    # Attempt to print solution with no board set
    with pytest.raises(ValueError) as e:
        solver.print_solution()
    
    assert "No board set" in str(e.value)

def test_print_solution_no_solution():
    """Test printing solution when no solution has been found."""
    # Create a board
    board = Board(4)
    
    # Create a solver and set the board
    solver = SudokuSolver()
    solver.set_board(board)
    
    # Attempt to print solution before solving
    with pytest.raises(ValueError) as e:
        solver.print_solution()
    
    assert "No solution found" in str(e.value)

def test_solve_simple_4x4():
    """Test solving a simple 4×4 puzzle."""
    # Create a 4×4 board with some values
    board = Board(4)
    
    # Set up a simple puzzle with a guaranteed solution
    # This configuration is known to be solvable (verified in find_valid_puzzles.py)
    board.set_value(0, 0, 1)
    board.set_value(0, 1, 2)
    board.set_value(1, 2, 1)
    board.set_value(1, 3, 2)
    board.set_value(2, 0, 2)
    board.set_value(2, 1, 1)
    board.set_value(3, 2, 2)
    board.set_value(3, 3, 1)
    
    # Update possible values
    board.update_possible_values()
    
    # Create a solver
    solver = SudokuSolver()
    
    # Solve the puzzle
    result = solver.solve(board)
    
    # Verify a solution was found
    assert result is True
    
    # Verify the solution is valid
    assert solver.board.is_valid()

def test_solve_simple_9x9():
    """Test solving a simple 9×9 puzzle."""
    # Create a 9×9 board
    board = Board(9)
    
    # Set up a simple puzzle with a unique solution
    clues = [
        (0, 0, 5), (0, 1, 3), (0, 4, 7),
        (1, 0, 6), (1, 3, 1), (1, 4, 9), (1, 5, 5),
        (2, 1, 9), (2, 2, 8), (2, 7, 6),
        (3, 0, 8), (3, 4, 6), (3, 8, 3),
        (4, 0, 4), (4, 3, 8), (4, 5, 3), (4, 8, 1),
        (5, 0, 7), (5, 4, 2), (5, 8, 6),
        (6, 1, 6), (6, 6, 2), (6, 7, 8),
        (7, 3, 4), (7, 4, 1), (7, 5, 9), (7, 8, 5),
        (8, 4, 8), (8, 7, 7), (8, 8, 9)
    ]
    
    for row, col, value in clues:
        board.set_value(row, col, value)
    
    # Update possible values
    board.update_possible_values()
    
    # Create a solver
    solver = SudokuSolver()
    
    # Solve the puzzle
    result = solver.solve(board)
    
    # Verify a solution was found
    assert result is True
    
    # Verify the solution is valid
    assert solver.board.is_valid()
    
    # Verify some of the original clues are preserved
    for row, col, value in clues[:5]:  # Check first 5 clues
        assert solver.board.get_value(row, col) == value

def test_unsolvable_puzzle():
    """Test that the solver correctly identifies unsolvable puzzles."""
    # Create a board with contradictory constraints
    board = Board(4)
    
    # Set up an unsolvable puzzle (contradictory values in the same row)
    board.set_value(0, 0, 1)
    board.set_value(0, 1, 1)  # Duplicates 1 in the first row
    
    # Update possible values
    board.update_possible_values()
    
    # Create a solver
    solver = SudokuSolver()
    
    # Try to solve the puzzle
    result = solver.solve(board)
    
    # Verify no solution was found
    assert result is False
    assert solver.solution_count == 0

def test_print_solution(capsys):
    """Test printing a solution."""
    # Create a simple puzzle and solve it
    board = Board(4)
    board.set_value(0, 0, 1)
    
    solver = SudokuSolver()
    result = solver.solve(board)
    
    # Verify it was solved
    assert result is True
    
    # Call print_solution
    solver.print_solution()
    
    # Capture the output and verify it contains "Solution:"
    captured = capsys.readouterr()
    assert "Solution:" in captured.out