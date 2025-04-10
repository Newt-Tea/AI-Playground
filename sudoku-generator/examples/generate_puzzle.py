#!/usr/bin/env python
"""
Example script for generating a single Sudoku puzzle.

This script demonstrates the basic usage of the Sudoku generator to create
a puzzle with a specified size and number of clues.
"""

import sys
import os

# Add the parent directory to path so we can import the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sudoku.generator import SudokuGenerator
from src.sudoku.solver import SudokuSolver

def main():
    """Generate and display a Sudoku puzzle, then solve it."""
    print("Sudoku Generator - Basic Example")
    print("===============================\n")
    
    # Ask for board size
    size = 0
    while size not in [4, 9, 16]:
        try:
            size = int(input("Enter board size (4, 9, or 16): "))
            if size not in [4, 9, 16]:
                print("Board size must be 4, 9, or 16.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Ask for number of clues (optional)
    num_clues = None
    try:
        clue_input = input(f"Enter number of clues (leave empty for default, recommended: "
                          f"{12 if size == 4 else 40 if size == 9 else 'auto-calculated'}): ")
        if clue_input:
            num_clues = int(clue_input)
    except ValueError:
        print("Using default number of clues.")
    
    print("\nGenerating puzzle...")
    
    # Create a generator instance for the specified size
    generator = SudokuGenerator(size)
    
    # Generate a puzzle
    puzzle = generator.generate_puzzle(num_clues=num_clues)
    
    # Print the generated puzzle
    print("\nGenerated Puzzle:")
    puzzle.print_grid()
    
    # Print generation statistics
    stats = generator.get_stats()
    print("\nGeneration Statistics:")
    print(f"- Board size: {stats['size']}x{stats['size']}")
    print(f"- Number of clues: {stats['num_clues']}")
    print(f"- Total generation time: {stats['generation_time']:.3f} seconds")
    print(f"- Solution generation time: {stats['solution_generation_time']:.3f} seconds")
    print(f"- Clue removal time: {stats['clue_removal_time']:.3f} seconds")
    print(f"- Number of attempts: {stats['attempts']}")
    
    # Ask if the user wants to see the solution
    if input("\nDo you want to see the solution? (y/n): ").lower().startswith('y'):
        # Create a solver
        solver = SudokuSolver()
        
        # Solve the puzzle
        print("\nSolving puzzle...")
        result = solver.solve(puzzle)
        
        # Print the solution
        if result:
            print("\nSolution:")
            solver.board.print_grid()
            print(f"\nSolved in {solver.solve_time:.6f} seconds with {solver.iterations} iterations")
        else:
            print("\nFailed to find a solution. The puzzle may be invalid.")

if __name__ == "__main__":
    main()