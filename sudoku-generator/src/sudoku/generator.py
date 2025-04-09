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
                num_clues = 12  # For 4x4 boards
            elif self.size == 9:
                num_clues = 40  # For 9x9 boards
            else:
                # For other sizes, aim for ~75% of cells filled
                num_clues = int(self.size * self.size * 0.75)
        
        # Set default max_attempts - Increased to ensure we find unique puzzles
        if max_attempts is None:
            if self.size == 4:
                max_attempts = 10  # Increased from 3
            elif self.size == 9:
                max_attempts = 10  # Increased from 5
            else:
                max_attempts = 15  # Increased from 10
        
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
                    "symmetric": symmetric,
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
    
    def _remove_clues_optimized(self, board, num_clues, symmetric=False):
        """
        Optimized strategy for removing clues while maintaining uniqueness.
        Uses a smart two-phase approach with difficulty estimation.
        
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
            
        # First phase: Quickly remove clues that are definitely safe to remove
        # This avoids expensive uniqueness checks for obvious cases
        safe_positions, remaining_positions = self._identify_safe_removals(board, positions)
        
        # Shuffle positions for random removal order to increase variety
        random.shuffle(safe_positions)
        random.shuffle(remaining_positions)
        
        # Track removal progress
        removed_count = 0
        attempted_positions = set()
        
        # Remove safe positions first (much faster)
        for row, col in safe_positions:
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
            
            # Update constraints - only update affected cells
            for r, c in cells_to_remove:
                board.update_possible_values(r, c, affected_only=True)
            
            # Double-check uniqueness
            if self.size <= 4:
                # Check if still unique - for small boards full solution counting is fine
                if board.count_solutions(max_count=2) != 1:
                    # Put back the clues if not unique
                    for i, (r, c) in enumerate(cells_to_remove):
                        board.set_value(r, c, values[i])
                        board.update_possible_values(r, c, affected_only=True)
                    continue
            
            # Count successful removals
            removed_count += len(cells_to_remove)
        
        # If we haven't removed enough clues yet, continue with remaining positions
        if removed_count < target_to_remove:
            # Shuffle remaining again to ensure randomness
            random.shuffle(remaining_positions)
            
            # Use different strategies based on board size
            if self.size >= 9:
                success = self._remove_clues_for_large_boards(
                    board, 
                    remaining_positions, 
                    target_to_remove - removed_count, 
                    symmetric,
                    attempted_positions
                )
            else:
                success = self._remove_clues_for_small_boards(
                    board, 
                    remaining_positions,
                    target_to_remove - removed_count,
                    symmetric,
                    attempted_positions
                )
                
            return success and (removed_count + target_to_remove - removed_count == target_to_remove)
        
        return removed_count == target_to_remove
    
    def _identify_safe_removals(self, board, positions):
        """
        Identify positions that are likely safe to remove without affecting uniqueness.
        
        Args:
            board (Board): The board to analyze
            positions (list): List of filled positions to check
            
        Returns:
            tuple: (safe_positions, remaining_positions)
        """
        safe_positions = []
        remaining_positions = []
        
        # Create a "safety score" for each position
        # Higher score means more neighbors are filled in, making removal safer
        position_scores = {}
        
        for row, col in positions:
            # Count filled neighbors in row, column and subgrid
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
            
            # Calculate a safety score based on filled neighbors
            # We can consider it safe if most neighbors are filled
            position_scores[(row, col)] = neighbors_filled
        
        # Determine threshold for "safe" removals based on board size
        safety_threshold = max(self.size // 2, 4)  # Higher threshold for larger boards
        
        # Categorize positions
        for pos in positions:
            if position_scores[pos] >= safety_threshold:
                safe_positions.append(pos)
            else:
                remaining_positions.append(pos)
        
        return safe_positions, remaining_positions
    
    def _remove_clues_for_small_boards(self, board, positions, target_to_remove, symmetric, attempted_positions):
        """
        Specialized clue removal for smaller boards.
        
        Args:
            board (Board): The board to remove clues from
            positions (list): List of filled positions
            target_to_remove (int): Number of clues to remove
            symmetric (bool): Whether to remove symmetrically
            attempted_positions (set): Set of already attempted positions
            
        Returns:
            bool: True if successfully removed target number of clues
        """
        removed_count = 0
        
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
            
            # Update constraints efficiently - only update affected cells
            for r, c in cells_to_remove:
                board.update_possible_values(r, c, affected_only=True)
            
            # Check if still unique - for small boards full solution counting is fine
            if board.count_solutions(max_count=2) == 1:
                removed_count += len(cells_to_remove)
            else:
                # Put back the clues
                for i, (r, c) in enumerate(cells_to_remove):
                    board.set_value(r, c, values[i])
                    board.update_possible_values(r, c, affected_only=True)
        
        return removed_count == target_to_remove
    
    def _remove_clues_for_large_boards(self, board, positions, target_to_remove, symmetric, attempted_positions):
        """
        Specialized clue removal for large boards like 9x9.
        Uses a more efficient approach for uniqueness checking.
        
        Args:
            board (Board): The board to remove clues from
            positions (list): List of filled positions
            target_to_remove (int): Number of clues to remove
            symmetric (bool): Whether to remove symmetrically
            attempted_positions (set): Set of already attempted positions
            
        Returns:
            bool: True if successfully removed target number of clues
        """
        removed_count = 0
        
        # Use smarter uniqueness verification for large boards
        # First solve the board to get the solution
        solver = SudokuSolver()
        solution_board = board.copy()
        solver.solve(solution_board)
        
        # Keep track of critical cells (cells that if removed would create multiple solutions)
        critical_cells = set()
        
        # Process remaining positions
        for row, col in positions:
            # Skip if we've already removed enough
            if removed_count >= target_to_remove:
                break
            
            # Skip if already tried, empty, or known to be critical
            if ((row, col) in attempted_positions or 
                board.is_empty(row, col) or 
                (row, col) in critical_cells):
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
            
            # Check if any of the cells are critical
            if any((r, c) in critical_cells for r, c in cells_to_remove):
                continue
            
            # Save values before removal
            values = [board.get_value(r, c) for r, c in cells_to_remove]
            
            # Remove clues
            for r, c in cells_to_remove:
                board.set_value(r, c, None)
            
            # Update constraints - only affected cells for efficiency
            for r, c in cells_to_remove:
                board.update_possible_values(r, c, affected_only=True)
            
            # Check uniqueness efficiently
            unique = self._verify_uniqueness_optimized(board, solution_board)
            
            if unique:
                removed_count += len(cells_to_remove)
            else:
                # Mark these cells as critical to avoid retrying them
                for r, c in cells_to_remove:
                    critical_cells.add((r, c))
                
                # Put back the clues
                for i, (r, c) in enumerate(cells_to_remove):
                    board.set_value(r, c, values[i])
                    board.update_possible_values(r, c, affected_only=True)
        
        return removed_count == target_to_remove

    def _verify_uniqueness_optimized(self, board, solution_board):
        """
        Optimized method to verify puzzle uniqueness for larger boards.
        
        Uses a combination of techniques to efficiently check uniqueness:
        1. First verify the puzzle is solvable
        2. Check if the solution matches our known solution
        3. Try a few strategic alternative values to verify uniqueness
        
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
        # For larger boards, strategically test a few empty cells rather than random ones
        # Look for cells with exactly 2 possible values - these are most likely to have alternative solutions
        test_cells = []
        
        # First pass - find cells with exactly 2 possible values
        for row in range(self.size):
            for col in range(self.size):
                if board.is_empty(row, col):
                    # Update possible values for this cell
                    board.update_possible_values(row, col)
                    
                    # Check number of possibilities
                    if len(board.get_cell(row, col).possible_values) == 2:
                        test_cells.append((row, col))
                        
                        # We only need a few test cells
                        if len(test_cells) >= 3:
                            break
            
            if len(test_cells) >= 3:
                break
        
        # If we didn't find enough cells with 2 possibilities, find any empty cells
        if len(test_cells) < 3:
            empty_cells = [(r, c) for r in range(self.size) for c in range(self.size) 
                           if board.is_empty(r, c)]
            
            # Add more test cells up to 3 total
            for _ in range(min(3 - len(test_cells), len(empty_cells))):
                if not empty_cells:
                    break
                
                idx = random.randrange(len(empty_cells))
                test_cells.append(empty_cells.pop(idx))
        
        # Test each cell for alternative solutions
        for row, col in test_cells:
            solution_value = solution_board.get_value(row, col)
            
            # Create a list of possible alternative values
            alt_values = [val for val in range(1, board.size + 1) 
                        if val != solution_value and board.is_safe(row, col, val)]
            
            # Try each alternative value
            for val in alt_values:
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