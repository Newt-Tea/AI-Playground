"""
Generator module for Sudoku puzzles.

This module contains the SudokuGenerator class which generates valid Sudoku puzzles.
"""
from src.sudoku.board import Board
from src.sudoku.solver import SudokuSolver
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
        
        # Seed with current time for randomness
        random.seed(time.time())
    
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
        
        # Add randomization by placing a few random values first
        # This helps ensure we get different puzzles each time
        num_initial_values = max(2, self.size // 3)  # More initial values for larger boards
        
        # Place random initial values
        for _ in range(num_initial_values):
            # Find an empty cell
            empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) 
                           if self.board.is_empty(r, c)]
            
            if not empty_cells:
                break
                
            # Choose a random empty cell
            row, col = random.choice(empty_cells)
            
            # Find valid values for this cell
            valid_values = [val for val in range(1, self.size + 1) 
                           if self.board.is_safe(row, col, val)]
            
            if valid_values:
                # Place a random valid value
                self.board.set_value(row, col, random.choice(valid_values))

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
    
    def generate_puzzle(self, num_clues=None, max_attempts=None, algorithm="optimized"):
        """
        Generate a Sudoku puzzle by removing clues from a complete solution.
        
        Args:
            num_clues (int, optional): The number of clues to leave in the puzzle.
                If None, will use a default based on board size.
            max_attempts (int): Maximum number of generation attempts
            algorithm (str): The clue removal algorithm to use: "optimized" (default) or "basic"
                             Note: "basic" is not recommended for boards larger than 9x9
            
        Returns:
            Board: A Sudoku puzzle with the specified number of clues
            
        Raises:
            RuntimeError: If failed to generate a puzzle after max_attempts
            ValueError: If an invalid algorithm is specified
        """
        # Start timing for the entire generation
        generation_start = time.time()
        
        # Simple time-based reseeding for randomization
        random.seed(time.time())
        
        # Validate algorithm choice
        if algorithm not in ["optimized", "basic"]:
            raise ValueError("Invalid algorithm. Must be 'optimized' or 'basic'.")
        
        
        # Default number of clues if not specified
        if num_clues is None:
            # Standard defaults based on board size
            if self.size == 4:
                num_clues = 12  # For 4x4 boards
            elif self.size == 9:
                num_clues = 40  # For 9x9 boards
            else:
                # 75% of the board for larger sizes
                num_clues = int(self.size * self.size * 0.75)
        
        # Set default max_attempts - Increased to ensure we find unique puzzles
        if max_attempts is None:
            if self.size == 4:
                max_attempts = 10  # For 4x4 boards
            elif self.size == 9:
                max_attempts = 25  # Increased from 10 to 25 for 9x9 boards 
            else:
                max_attempts = 40  # Increased from 15 to 40 for 16x16 boards
        
        # Try multiple times in case we get stuck
        for attempt in range(max_attempts):
            # Reset random seed for each attempt
            random.seed(time.time())
            
            # Generate a fresh solution for each attempt
            self.generate_solution()
            
            # Make a copy of the solution to work with
            puzzle = self.board.copy()
            
            # Start timing clue removal
            removal_start = time.time()
            
            # Use specified removal strategy
            if algorithm == "optimized":
                removal_success = self._remove_clues_optimized(puzzle, num_clues)
            else:  # algorithm == "basic"
                removal_success = self._remove_clues_basic(puzzle, num_clues)
            
            # Record removal time
            self.removal_time = max(time.time() - removal_start, 0.000001)  # minimum time of 1 microsecond
            
            if removal_success:
                # Final verification: Ensure the puzzle has exactly one solution
                solution_count = puzzle.count_solutions(max_count=2)
                if solution_count != 1:
                    # If not unique, try again with a fresh solution
                    self.board = None
                    continue
                    
                # Successful generation
                self.stats = {
                    "size": self.size,
                    "num_clues": num_clues,
                    "algorithm": algorithm,
                    "generation_time": time.time() - generation_start,
                    "solution_generation_time": self.generation_time,
                    "clue_removal_time": self.removal_time,
                    "attempts": attempt + 1
                }

                return puzzle
            
            # Force garbage collection to free memory
            gc.collect()
            
            # Try again with a fresh solution
            self.board = None
        
        # If we reach here, all attempts failed
        raise RuntimeError(f"Failed to generate puzzle after {max_attempts} attempts")
    
    def _remove_clues_optimized(self, board, num_clues):
        """
        Optimized strategy for removing clues while maintaining uniqueness.
        Uses a smart adaptive approach based on board size and position characteristics.
        Defers uniqueness checking until the end for better performance.
        
        Args:
            board (Board): The board to remove clues from
            num_clues (int): The target number of clues to leave
            
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
            
        # Create a reference solution for final uniqueness checking
        solution_board = board.copy()
        solver = SudokuSolver()
        solver.solve(solution_board)
            
        # First phase: Score and categorize positions by removal safety
        position_scores = self._score_removal_safety(board, positions)
        
        # Sort positions by safety score (highest scores first - most safe to remove)
        positions_by_safety = sorted(positions, key=lambda pos: position_scores[pos], reverse=True)
        
        # Track removal progress
        removed_count = 0
        removed_positions = []
        
        # Process positions by safety score, removing clues without checking uniqueness during removal
        for row, col in positions_by_safety:
            # Skip if we've already removed enough
            if removed_count >= target_to_remove:
                break
                
            # Skip if already empty
            if board.is_empty(row, col):
                continue
                
            # Save value before removal
            value = board.get_value(row, col)
            
            # Remove clue
            board.set_value(row, col, None)
            board.update_possible_values(row, col, affected_only=True)
            
            # Track removed positions and count
            removed_positions.append((row, col, value))
            removed_count += 1
        
        # Verify uniqueness only once at the end
        solutions = board.count_solutions(max_count=2)
        if solutions == 1:
            # Success! The puzzle has a unique solution
            return True
        else:
            # The puzzle has no solutions or multiple solutions
            # Try to recover by adding back some of the removed clues
            print(f"Puzzle with {num_clues} clues has {solutions} solutions, attempting recovery...")
            
            # Start adding back removed clues until we get a unique solution
            # Prioritize adding back clues that were removed later (they're more important)
            for row, col, value in reversed(removed_positions):
                # Put back the clue
                board.set_value(row, col, value)
                board.update_possible_values(row, col, affected_only=True)
                
                # Check uniqueness
                solutions = board.count_solutions(max_count=2)
                if solutions == 1:
                    # Found a unique solution by adding back some clues
                    current_clues = sum(1 for r in range(self.size) for c in range(self.size) 
                                      if not board.is_empty(r, c))
                    print(f"Recovered a unique solution with {current_clues} clues")
                    return True
            
            # If we couldn't recover a unique solution, generation failed
            return False

    def _score_removal_safety(self, board, positions):
        """
        Score positions based on how likely they are to maintain uniqueness when removed.
        Higher scores indicate safer removals.
        
        Args:
            board (Board): The board to analyze
            positions (list): List of filled positions to score
            
        Returns:
            dict: Dictionary mapping positions to safety scores
        """
        position_scores = {}
        
        for row, col in positions:
            # Base safety score starts with number of filled neighbors
            neighbors_filled = 0
            
            # Row neighbors
            for c in range(self.size):
                if c != col and not board.is_empty(row, c):
                    neighbors_filled += 1
            
            # Column neighbors
            for r in range(self.size):
                if r != row and not board.is_empty(r, col):
                    neighbors_filled += 1
            
            # Subgrid neighbors
            subgrid_row = (row // board.subgrid_size) * board.subgrid_size
            subgrid_col = (col // board.subgrid_size) * board.subgrid_size
            
            for r in range(subgrid_row, subgrid_row + board.subgrid_size):
                for c in range(subgrid_col, subgrid_col + board.subgrid_size):
                    if (r != row or c != col) and not board.is_empty(r, c):
                        neighbors_filled += 1
            
            # Add bonus points for cells with many filled neighbors in the same line
            row_sequence = col_sequence = 0
            for c in range(self.size):
                if not board.is_empty(row, c):
                    row_sequence += 1
                else:
                    row_sequence = 0
                    
            for r in range(self.size):
                if not board.is_empty(r, col):
                    col_sequence += 1
                else:
                    col_sequence = 0
            
            # A cell in a longer sequence of filled cells is more likely to be safely removable
            sequence_bonus = max(row_sequence, col_sequence) // 2
            
            # Final score is base score plus bonuses
            position_scores[(row, col)] = neighbors_filled + sequence_bonus
        
        return position_scores
    
    def _remove_clues_basic(self, board, num_clues):
        """
        Basic clue removal algorithm using MRV and backtracking.
        
        WARNING: This method should not be used on boards larger than 9x9
        as performance will degrade significantly.
        
        Args:
            board (Board): The board to remove clues from
            num_clues (int): The target number of clues to leave
            
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
        
        # Randomize the removal order for variety
        random.shuffle(positions)
        
        # Keep track of removed positions
        removed_positions = []
        
        # Try removing clues one by one
        for row, col in positions:
            # Skip if we've already removed enough clues
            if len(removed_positions) >= target_to_remove:
                break
            
            # Save the current value before removing
            value = board.get_value(row, col)
            
            # Remove the clue
            board.set_value(row, col, None)
            board.update_possible_values(row, col, affected_only=True)
            
            # Check if the puzzle still has a unique solution using MRV
            solutions = board.count_solutions(max_count=2)
            
            if solutions == 1:
                # Removal successful - puzzle still has a unique solution
                removed_positions.append((row, col))
            else:
                # Removal created 0 or multiple solutions - restore the clue
                board.set_value(row, col, value)
                board.update_possible_values(row, col, affected_only=True)
        
        # Return True if we successfully removed enough clues
        return len(removed_positions) == target_to_remove
    
    def _verify_uniqueness_optimized(self, board, solution_board):
        """
        Optimized method to verify puzzle uniqueness for larger boards.
        
        Uses a combination of techniques to efficiently check uniqueness:
        1. First verify the puzzle is solvable
        2. Check if the solution matches our known solution
        3. Try strategically selected alternative values to verify uniqueness
        
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
        
        # Determine how many cells to test based on board size
        # Larger boards need more test cells for reliable uniqueness verification
        if self.size <= 4:
            num_test_cells = 4
        elif self.size == 9:
            num_test_cells = 10  # Increased from 3 to 10 for 9x9 boards
        else:
            num_test_cells = 15  # Increased for 16x16 boards
        
        # The solution is the same as our known solution
        # Strategically test empty cells with focus on those most likely to have alternative solutions
        test_cells = []
        
        # Find cells with exactly 2 possible values first - these are most likely to have alternative solutions
        for row in range(self.size):
            for col in range(self.size):
                if board.is_empty(row, col):
                    # Update possible values for this cell
                    board.update_possible_values(row, col)
                    
                    # Check number of possibilities
                    possible_values = board.get_cell(row, col).possible_values
                    if len(possible_values) == 2:
                        test_cells.append((row, col, possible_values))
                        
                        # Once we have enough test cells, we can stop searching
                        if len(test_cells) >= num_test_cells:
                            break
            
            if len(test_cells) >= num_test_cells:
                break
        
        # If we didn't find enough cells with 2 possibilities, look for cells with 3 possibilities
        if len(test_cells) < num_test_cells:
            for row in range(self.size):
                for col in range(self.size):
                    if board.is_empty(row, col):
                        # Skip cells we've already added
                        if any(r == row and c == col for r, c, _ in test_cells):
                            continue
                            
                        possible_values = board.get_cell(row, col).possible_values
                        if len(possible_values) == 3:
                            test_cells.append((row, col, possible_values))
                            
                            if len(test_cells) >= num_test_cells:
                                break
                
                if len(test_cells) >= num_test_cells:
                    break
        
        # If we still don't have enough test cells, just add any empty cells
        if len(test_cells) < num_test_cells:
            empty_cells = []
            for row in range(self.size):
                for col in range(self.size):
                    if board.is_empty(row, col):
                        # Skip cells we've already added
                        if any(r == row and c == col for r, c, _ in test_cells):
                            continue
                            
                        empty_cells.append((row, col))
            
            # Shuffle to add randomness to the selection
            random.shuffle(empty_cells)
            
            # Add more cells up to our target
            for row, col in empty_cells:
                possible_values = board.get_cell(row, col).possible_values
                test_cells.append((row, col, possible_values))
                
                if len(test_cells) >= num_test_cells:
                    break
        
        # Test each cell for alternative solutions
        for row, col, possible_values in test_cells:
            solution_value = solution_board.get_value(row, col)
            
            # Try each possible alternative value
            for val in possible_values:
                if val != solution_value:
                    # Make a new board with this alternative value
                    alt_board = board.copy()
                    alt_board.set_value(row, col, val)
                    alt_board.update_possible_values(row, col, affected_only=True)
                    
                    # If this board can be solved, the original has multiple solutions
                    alt_solver = SudokuSolver()
                    if alt_solver.solve(alt_board):
                        return False
        
        # For 9x9 and 16x16 boards, do an extra check of random cells for greater confidence
        if self.size >= 9:
            # Pick a few random empty cells not already tested
            empty_positions = [(r, c) for r in range(self.size) for c in range(self.size) 
                              if board.is_empty(r, c) and not any(r == row and c == col for row, col, _ in test_cells)]
            
            # Test up to 5 additional random cells
            extra_test_count = min(5, len(empty_positions))
            if extra_test_count > 0:
                # Shuffle the positions
                random.shuffle(empty_positions)
                
                for i in range(extra_test_count):
                    row, col = empty_positions[i]
                    solution_value = solution_board.get_value(row, col)
                    
                    # Try each possible value except the solution value
                    for val in range(1, board.size + 1):
                        if val != solution_value and board.is_safe(row, col, val):
                            # Make a new board with this alternative value
                            alt_board = board.copy()
                            alt_board.set_value(row, col, val)
                            alt_board.update_possible_values(row, col, affected_only=True)
                            
                            # If this board can be solved, the original has multiple solutions
                            alt_solver = SudokuSolver()
                            if alt_solver.solve(alt_board):
                                return False
        
        # If we couldn't find any alternative solutions, the puzzle likely has a unique solution
        return True
    
    def get_stats(self):
        """
        Get generation statistics.
        
        Returns:
            dict: Dictionary containing generation statistics
        """
        return self.stats