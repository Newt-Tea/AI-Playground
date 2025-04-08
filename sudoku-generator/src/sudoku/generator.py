"""
Generator module for Sudoku puzzles.

This module contains the SudokuGenerator class which generates valid Sudoku puzzles.
"""
from .board import Board
from .solver import SudokuSolver
import random
import time
import gc

class SudokuGenerator:
    """Class for generating Sudoku puzzles with optimized algorithms."""
    
    def __init__(self, size=9):
        """
        Initialize a new Sudoku generator.
        
        Args:
            size (int): The size of the board to generate (default: 9)
        """
        self.size = size
        self.board = None
        self.solver = SudokuSolver()
        self.generation_time = 0
        self.removal_time = 0
        self.stats = {}
    
    def generate_solution(self):
        """
        Generate a complete valid Sudoku solution.
        
        Returns:
            Board: A completely filled valid Sudoku board
        """
        # Create an empty board
        self.board = Board(self.size)

        # Timer for generation
        generation_start = time.time()
        

        # Update possible values before solving
        self.board.update_possible_values()
        
        # Use the solver to complete the rest of the board
        solver = SudokuSolver()
        success = solver.solve(self.board)
        
        # Get the solved board from the solver
        if success:
            self.board = solver.board
        else:
            # If solving fails, try again with a fresh board
            return self.generate_solution()
        
        # Verify the board is valid and complete
        if not self.board.is_valid():
            # If not valid for some reason, try again
            return self.generate_solution()
        
        # Double check that all cells are filled
        for row in range(self.size):
            for col in range(self.size):
                if self.board.is_empty(row, col):
                    # If any empty cells remain, try again
                    return self.generate_solution()
        
        generation_time = time.time() - generation_start
        self.generation_time = generation_time

        return self.board.copy()
    
    def generate_puzzle(self, num_clues=None, symmetric=False, max_attempts=None):
        """
        Generate a Sudoku puzzle by removing clues from a complete solution.
        
        Args:
            num_clues (int, optional): The number of clues to leave in the puzzle.
                If None, will use a default based on board size.
            symmetric (bool): Whether to remove clues symmetrically (default: False)
            max_attempts (int): Maximum number of generation attempts
            
        Returns:
            Board: A Sudoku puzzle with the specified number of clues
        """
        # Start timing for the entire generation
        generation_start = time.time()
        
        # Default number of clues if not specified
        if num_clues is None:
            # Standard defaults based on board size
            if self.size == 4:
                num_clues = 7  # For 4x4 boards
            elif self.size == 9:
                num_clues = 25  # For 9x9 boards
            else:
                # For other sizes, aim for ~30% of cells filled
                num_clues = max(self.size * self.size // 3, self.size)
        
        if max_attempts is None:
            if self.size == 4:
                max_attempts = 3
            elif self.size == 9:
                max_attempts = 5
            else:
                max_attempts = 10
        
        # Try multiple times in case we get stuck
        for attempt in range(max_attempts):
            # If we don't already have a solved board, generate one
            if self.board is None or not self.board.is_valid():
                self.generate_solution()
            
            # Make a copy of the solution to work with
            puzzle = self.board.copy()
            
            # Start timing clue removal
            removal_start = time.time()
            
            # Use optimized removal strategy
            removal_success = self._remove_clues_optimized(puzzle, num_clues, symmetric)
            
            
            
            if removal_success:
                # Successful generation
                self.stats = {
                    "size": self.size,
                    "num_clues": num_clues,
                    "symmetric": symmetric,
                    "generation_time": time.time() - generation_start,
                    "solution_generation_time": self.generation_time,
                    "clue_removal_time": self.removal_time,
                    "attempts": attempt + 1
                }
                # Record removal time
                self.removal_time = time.time() - removal_start

                return puzzle
            
            # Force garbage collection to free memory
            gc.collect()
            
            # Try again with a fresh solution
            self.board = None
        
        # If we reach here, all attempts failed
        raise RuntimeError(f"Failed to generate puzzle after {max_attempts} attempts")
    
    def _remove_clues_optimized(self, board, num_clues, symmetric=False):
        """
        Optimized strategy for removing clues while maintaining uniqueness.
        
        Args:
            board (Board): The board to remove clues from
            num_clues (int): The target number of clues to leave
            symmetric (bool): Whether to remove clues symmetrically
            
        Returns:
            bool: True if successfully removed clues to reach target, False otherwise
        """
        # Get all filled positions
        positions = []
        for row in range(self.size):
            for col in range(self.size):
                if not board.is_empty(row, col):
                    positions.append((row, col))
        
        # Calculate target to remove
        current_clues = len(positions)
        target_to_remove = current_clues - num_clues
        
        if target_to_remove <= 0:
            # Already at or below target
            return True
        
        # Shuffle positions for random removal order
        random.shuffle(positions)
        
        # For 9x9 boards, we need a different approach - remove one cell at a time
        if self.size >= 9:
            return self._remove_clues_for_large_boards(board, positions, target_to_remove, symmetric)
        
        # For smaller boards, continue with the batch approach
        removed_count = 0
        attempted_positions = set()
        
        # Process positions one by one for smaller boards
        for row, col in positions:
            # Skip if we've already removed enough
            if removed_count >= target_to_remove:
                break
            
            # Skip if already tried or empty
            if (row, col) in attempted_positions or board.is_empty(row, col):
                continue
            
            # Mark as attempted
            attempted_positions.add((row, col))
            
            # Determine cells to remove (original and symmetric if needed)
            cells_to_remove = [(row, col)]
            if symmetric:
                sym_row, sym_col = self.size - 1 - row, self.size - 1 - col
                if (row, col) != (sym_row, sym_col) and not board.is_empty(sym_row, sym_col):
                    cells_to_remove.append((sym_row, sym_col))
                    attempted_positions.add((sym_row, sym_col))
            
            # Save values before removal
            values = [board.get_value(r, c) for r, c in cells_to_remove]
            
            # Remove clues
            for r, c in cells_to_remove:
                board.set_value(r, c, None)
            
            # Update constraints
            board.update_possible_values()
            
            # Check if still unique
            if board.count_solutions(max_count=2) == 1:
                removed_count += len(cells_to_remove)
            else:
                # Put back the clues
                for i, (r, c) in enumerate(cells_to_remove):
                    board.set_value(r, c, values[i])
                board.update_possible_values()
        
        return removed_count == target_to_remove

    def _remove_clues_for_large_boards(self, board, positions, target_to_remove, symmetric):
        """
        Specialized clue removal for large boards like 9x9.
        Uses a more efficient approach for uniqueness checking.
        
        Args:
            board (Board): The board to remove clues from
            positions (list): List of filled positions
            target_to_remove (int): Number of clues to remove
            symmetric (bool): Whether to remove symmetrically
            
        Returns:
            bool: True if successfully removed target number of clues
        """
        removed_count = 0
        attempted_positions = set()
        
        # First solve the board to get the solution
        solver = SudokuSolver()
        solution_board = board.copy()
        solver.solve(solution_board)
        
        for row, col in positions:
            # Skip if we've already removed enough
            if removed_count >= target_to_remove:
                break
            
            # Skip if already tried or empty
            if (row, col) in attempted_positions or board.is_empty(row, col):
                continue
            
            # Mark as attempted
            attempted_positions.add((row, col))
            
            # Determine cells to remove (original and symmetric if needed)
            cells_to_remove = [(row, col)]
            if symmetric:
                sym_row, sym_col = self.size - 1 - row, self.size - 1 - col
                if (row, col) != (sym_row, sym_col) and not board.is_empty(sym_row, sym_col):
                    cells_to_remove.append((sym_row, sym_col))
                    attempted_positions.add((sym_row, sym_col))
            
            # Save values before removal
            values = [board.get_value(r, c) for r, c in cells_to_remove]
            
            # Remove clues
            for r, c in cells_to_remove:
                board.set_value(r, c, None)
            
            # Update constraints
            board.update_possible_values()
            
            # Check uniqueness efficiently
            unique = self._verify_uniqueness(board, solution_board)
            
            if unique:
                removed_count += len(cells_to_remove)
            else:
                # Put back the clues
                for i, (r, c) in enumerate(cells_to_remove):
                    board.set_value(r, c, values[i])
                board.update_possible_values()
        
        return removed_count == target_to_remove

    def _verify_uniqueness(self, board, solution_board):
        """
        More efficient method to verify puzzle uniqueness for larger boards.
        
        Instead of counting all solutions, this method:
        1. Checks if the board is solvable
        2. Verifies the solution matches our known solution
        
        Args:
            board (Board): The board to check
            solution_board (Board): The known complete solution
            
        Returns:
            bool: True if the board likely has a unique solution
        """
        # Create a solver and copy of the board
        test_board = board.copy()
        solver = SudokuSolver()
        
        # Try to solve the puzzle
        if not solver.solve(test_board):
            return False  # Not even solvable
        
        # Check if the solution matches our known solution
        for row in range(self.size):
            for col in range(self.size):
                if test_board.get_value(row, col) != solution_board.get_value(row, col):
                    return False  # Found a different solution
        
        # The solution is the same as our known solution
        # Now check a few key cells to see if altering them allows another solution
        empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) 
                       if board.is_empty(r, c)]
        
        # Check a subset of empty cells for efficiency
        for _ in range(min(5, len(empty_cells))):
            if not empty_cells:
                break
            
            # Pick a random empty cell
            idx = random.randrange(len(empty_cells))
            row, col = empty_cells.pop(idx)
            
            solution_value = solution_board.get_value(row, col)
            
            # Try each alternative value
            for val in range(1, board.size + 1):
                if val != solution_value and board.is_safe(row, col, val):
                    # Make a new board with this alternative value
                    alt_board = board.copy()
                    alt_board.set_value(row, col, val)
                    alt_board.update_possible_values()
                    
                    # If this board can be solved, the original has multiple solutions
                    alt_solver = SudokuSolver()
                    if alt_solver.solve(alt_board):
                        return False
        
        # If we couldn't find any alternative solutions in our samples,
        # it's likely the puzzle has a unique solution
        return True
    
    def get_stats(self):
        """
        Get generation statistics.
        
        Returns:
            dict: Dictionary containing generation statistics
        """
        return self.stats