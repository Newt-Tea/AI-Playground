"""
Integration tests for the Sudoku generator project.

These tests verify the complete pipeline from puzzle generation to solving,
as well as test the example scripts.
"""

import pytest
import sys
import os
import io
from contextlib import redirect_stdout
import tempfile
import json

# Add the parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sudoku.generator import SudokuGenerator
from src.sudoku.solver import SudokuSolver
from src.sudoku.board import Board
from src.sudoku.benchmark import benchmark_solver, benchmark_generator

# Import example scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'examples')))
import generate_puzzle
import batch_generate
import solve_puzzle

def test_end_to_end_pipeline():
    """Test the complete pipeline from generation to solving."""
    # Use small board size for faster testing
    board_size = 4
    
    # Create a generator
    generator = SudokuGenerator(board_size)
    
    # Generate a puzzle
    puzzle = generator.generate_puzzle()
    
    # Verify the puzzle has a valid structure
    assert puzzle.size == board_size
    assert puzzle.is_valid()
    
    # Count the number of clues
    clue_count = sum(1 for row in range(board_size) for col in range(board_size) 
                     if puzzle.get_value(row, col) is not None)
    
    # For a 4x4 board, default should be 12 clues
    assert clue_count == 12
    
    # Verify the puzzle has exactly one solution
    assert puzzle.count_solutions() == 1
    
    # Create a solver
    solver = SudokuSolver()
    
    # Solve the puzzle
    result = solver.solve(puzzle)
    
    # Verify the puzzle was solved
    assert result is True
    
    # Verify the solution is valid
    assert solver.board.is_valid()
    
    # Verify all cells are filled
    assert len(solver.board.get_empty_positions()) == 0

def test_performance_benchmarks():
    """Test performance benchmarks meet requirements."""
    # Use small board size for faster testing
    board_size = 4
    
    # Benchmark the solver
    solver_results = benchmark_solver(board_size, num_runs=2)
    
    # Verify the solver benchmark returns results
    assert solver_results is not None
    assert solver_results.get_summary() is not None
    assert 'time' in solver_results.get_summary()
    assert 'iterations' in solver_results.get_summary()
    assert solver_results.get_summary()['board_size'] == board_size
    
    # Benchmark the generator
    generator_results = benchmark_generator(board_size, num_runs=2)
    
    # Verify the generator benchmark returns results
    assert generator_results is not None
    assert generator_results.get_summary() is not None
    assert 'time' in generator_results.get_summary()
    assert generator_results.get_summary()['board_size'] == board_size

def test_example_scripts_imports():
    """Test that example scripts can be imported correctly."""
    # If we got here, the imports worked fine
    assert hasattr(generate_puzzle, 'main')
    assert hasattr(batch_generate, 'generate_puzzles')
    assert hasattr(solve_puzzle, 'solve_from_file')

@pytest.mark.parametrize("size,num_clues", [(4, 8), (4, 10), (4, None)])
def test_batch_generate_functionality(size, num_clues):
    """Test the batch generate functionality with different parameters."""
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate a small batch of puzzles
        batch_generate.generate_puzzles(size, 2, num_clues, tmpdir)
        
        # Check if batch statistics file was created
        batch_files = [f for f in os.listdir(tmpdir) if f.startswith('batch_')]
        assert len(batch_files) == 1
        
        # Check if puzzle files were created
        puzzle_files = [f for f in os.listdir(tmpdir) if f.startswith('puzzle_')]
        assert len(puzzle_files) == 2
        
        # Load one puzzle file and check its structure
        with open(os.path.join(tmpdir, puzzle_files[0]), 'r') as f:
            puzzle_data = json.load(f)
            
            assert 'id' in puzzle_data
            assert 'size' in puzzle_data
            assert puzzle_data['size'] == size
            assert 'grid' in puzzle_data
            assert len(puzzle_data['grid']) == size
            assert len(puzzle_data['grid'][0]) == size

def test_solve_functionality():
    """Test the solve functionality with a generated puzzle."""
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate a simple puzzle
        generator = SudokuGenerator(4)
        puzzle = generator.generate_puzzle(num_clues=10)
        
        # Save it to a file
        puzzle_file = os.path.join(tmpdir, 'test_puzzle.json')
        puzzle_data = {
            'size': 4,
            'grid': [[puzzle.get_value(row, col) for col in range(4)] for row in range(4)]
        }
        
        with open(puzzle_file, 'w') as f:
            json.dump(puzzle_data, f)
        
        # Redirect stdout to capture output
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            # Solve the puzzle from file
            solve_puzzle.solve_from_file(puzzle_file)
        
        # Check output for success indicators
        output = buffer.getvalue()
        assert "Solution found!" in output
        assert "Solution is valid!" in output