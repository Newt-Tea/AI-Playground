#!/usr/bin/env python
"""
Example script for solving Sudoku puzzles from files or manual input.

This script demonstrates how to load and solve Sudoku puzzles using
the SudokuSolver class.
"""

import sys
import os
import json
import argparse
import time

# Add the parent directory to path so we can import the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sudoku.board import Board
from src.sudoku.solver import SudokuSolver

def solve_from_file(filename):
    """
    Load a puzzle from a JSON file and solve it.
    
    Args:
        filename (str): Path to the JSON file containing the puzzle
    """
    print(f"Loading puzzle from {filename}...")
    
    # Load the puzzle data
    with open(filename, 'r') as f:
        puzzle_data = json.load(f)
    
    # Extract puzzle details
    size = puzzle_data.get('size', 9)
    grid = puzzle_data.get('grid', [])
    
    # Create a board and load the puzzle data
    board = Board(size)
    for row in range(size):
        for col in range(size):
            if row < len(grid) and col < len(grid[row]) and grid[row][col] is not None:
                board.set_value(row, col, grid[row][col])
    
    # Initialize the possible values for the board's cells
    board.update_possible_values()
    
    # Display the loaded puzzle
    print("\nLoaded puzzle:")
    board.print_grid()
    
    # Print clue count
    clue_count = sum(1 for row in range(size) for col in range(size) 
                     if board.get_value(row, col) is not None)
    print(f"Number of clues: {clue_count}")
    
    # Create a solver
    solver = SudokuSolver()
    
    # Solve the puzzle
    print("\nSolving puzzle...")
    start_time = time.time()
    result = solver.solve(board)
    solve_time = time.time() - start_time
    
    # Print the result
    if result:
        print("\nSolution found!")
        solver.board.print_grid()
        print(f"\nSolved in {solve_time:.6f} seconds with {solver.iterations} iterations")
        
        # Verify the solution is valid
        if solver.board.is_valid():
            print("Solution is valid!")
        else:
            print("Warning: Solution may not be valid. Please check for errors.")
    else:
        print("\nFailed to solve the puzzle. It may be unsolvable or invalid.")

def solve_manual_input():
    """Allow the user to input a puzzle manually and solve it."""
    print("\nManual Puzzle Input")
    print("==================")
    
    # Ask for board size
    size = 0
    while size not in [4, 9, 16]:
        try:
            size = int(input("Enter board size (4, 9, or 16): "))
            if size not in [4, 9, 16]:
                print("Board size must be 4, 9, or 16.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Create a blank board
    board = Board(size)
    
    print(f"\nEnter the {size}x{size} puzzle row by row, using 0 for empty cells.")
    print("For example: '5 3 0 0 7 0 0 0 0' for the first row of a 9x9 puzzle.")
    
    # Input each row
    for row in range(size):
        while True:
            try:
                values = input(f"Row {row+1}: ").split()
                
                # Validate input length
                if len(values) != size:
                    print(f"Please enter exactly {size} values.")
                    continue
                
                # Add values to board
                for col, value in enumerate(values):
                    val = int(value)
                    if val > 0 and val <= size:
                        board.set_value(row, col, val)
                
                # If we got here, the input was valid
                break
            
            except ValueError:
                print("Invalid input. Please enter numbers only.")
    
    # Initialize the possible values for the board's cells
    board.update_possible_values()
    
    # Display the entered puzzle
    print("\nEntered puzzle:")
    board.print_grid()
    
    # Print clue count
    clue_count = sum(1 for row in range(size) for col in range(size) 
                     if board.get_value(row, col) is not None)
    print(f"Number of clues: {clue_count}")
    
    # Validate the puzzle before solving
    if not board.is_valid():
        print("\nWarning: The puzzle contains inconsistencies.")
        if input("Do you still want to attempt to solve it? (y/n): ").lower() != 'y':
            return
    
    # Create a solver
    solver = SudokuSolver()
    
    # Solve the puzzle
    print("\nSolving puzzle...")
    start_time = time.time()
    result = solver.solve(board)
    solve_time = time.time() - start_time
    
    # Print the result
    if result:
        print("\nSolution found!")
        solver.board.print_grid()
        print(f"\nSolved in {solve_time:.6f} seconds with {solver.iterations} iterations")
        
        # Verify the solution is valid
        if solver.board.is_valid():
            print("Solution is valid!")
        else:
            print("Warning: Solution may not be valid. Please check for errors.")
    else:
        print("\nFailed to solve the puzzle. It may be unsolvable or invalid.")

def main():
    """Parse arguments and solve puzzles."""
    parser = argparse.ArgumentParser(description="Solve Sudoku puzzles.")
    parser.add_argument("--file", type=str, help="Path to a JSON file containing a puzzle")
    
    args = parser.parse_args()
    
    # If a file is specified, solve from file
    if args.file:
        solve_from_file(args.file)
    # Otherwise, get manual input
    else:
        solve_manual_input()

if __name__ == "__main__":
    main()