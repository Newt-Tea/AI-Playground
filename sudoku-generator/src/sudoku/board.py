"""
Board module for Sudoku generator.

This module contains the Board class which represents a Sudoku grid.
"""
import math
from src.sudoku.cell import Cell

class Board:
    """Represents a Sudoku board."""
    
    def __init__(self, size=9):
        """
        Initialize a Sudoku board.
        
        Args:
            size (int): Board size (n). Must be a perfect square. Defaults to 9.
            
        Raises:
            ValueError: If size is not a perfect square.
        """
        # Validate that size is a perfect square
        self.size = size
        self.subgrid_size = int(math.sqrt(size))
        
        # Check if size is a perfect square
        if self.subgrid_size * self.subgrid_size != size:
            raise ValueError(f"Board size must be a perfect square. Got {size}.")
            
        # Initialize the grid with empty cells
        self.grid = []
        for row in range(size):
            row_cells = []
            for col in range(size):
                row_cells.append(Cell(row, col, board_size=size))
            self.grid.append(row_cells)
    
    def get_cell(self, row, col):
        """
        Get the cell at the specified position.
        
        Args:
            row (int): Row index (0-based)
            col (int): Column index (0-based)
            
        Returns:
            Cell: The cell at the specified position
            
        Raises:
            IndexError: If row or col is out of bounds
        """
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise IndexError(f"Position ({row}, {col}) is out of bounds for board of size {self.size}")
        return self.grid[row][col]
    
    def set_value(self, row, col, value):
        """
        Set the value of the cell at the specified position.
        
        Args:
            row (int): Row index (0-based)
            col (int): Column index (0-based)
            value (int or None): The value to set
            
        Raises:
            IndexError: If row or col is out of bounds
            ValueError: If value is invalid for the board size
        """
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise IndexError(f"Position ({row}, {col}) is out of bounds for board of size {self.size}")
            
        if value is not None and not (1 <= value <= self.size):
            raise ValueError(f"Value must be between 1 and {self.size} or None. Got {value}")
            
        self.grid[row][col].set_value(value)
    
    def get_value(self, row, col):
        """
        Get the value of the cell at the specified position.
        
        Args:
            row (int): Row index (0-based)
            col (int): Column index (0-based)
            
        Returns:
            int or None: The value of the cell
            
        Raises:
            IndexError: If row or col is out of bounds
        """
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise IndexError(f"Position ({row}, {col}) is out of bounds for board of size {self.size}")
            
        return self.grid[row][col].get_value()
    
    def get_size(self):
        """
        Get the board size.
        
        Returns:
            int: The size of the board
        """
        return self.size
    
    def get_subgrid_size(self):
        """
        Get the subgrid size.
        
        Returns:
            int: The size of the subgrids
        """
        return self.subgrid_size

    def is_empty(self, row, col):
        """
        Check if the cell at the specified position is empty.
        
        Args:
            row (int): Row index (0-based)
            col (int): Column index (0-based)
            
        Returns:
            bool: True if the cell is empty (None value), False otherwise
            
        Raises:
            IndexError: If row or col is out of bounds
        """
        return self.get_value(row, col) is None
    
    def get_empty_positions(self):
        """
        Get all empty positions on the board.
        
        Returns:
            list: List of (row, col) tuples representing empty cell positions
        """
        empty_positions = []
        for row in range(self.size):
            for col in range(self.size):
                if self.is_empty(row, col):
                    empty_positions.append((row, col))
        return empty_positions
    
    def print_grid(self):
        """
        Print the board grid to the console.
        """
        print(str(self))
    
    def __str__(self):
        """
        String representation of the board with grid lines.
        
        Returns:
            str: Formatted string representation of the board
        """
        # Calculate the width needed for each cell based on board size
        # For example, a 16x16 board needs 2 characters per cell (for numbers 10-16)
        cell_width = len(str(self.size))
        
        # Create the horizontal separator line
        separator = self._create_horizontal_separator(cell_width)
        
        result = []
        for row in range(self.size):
            # Add separators between subgrids
            if row > 0 and row % self.subgrid_size == 0:
                result.append(separator)
            
            row_str = []
            for col in range(self.size):
                # Add separators between subgrids
                if col > 0 and col % self.subgrid_size == 0:
                    row_str.append("|")
                
                value = self.get_value(row, col)
                if value is None:
                    # Empty cell
                    row_str.append(" " * cell_width)
                else:
                    # Format the value with proper width
                    row_str.append(str(value).rjust(cell_width))
            
            result.append(" ".join(row_str))
        
        return "\n".join(result)
    
    def _create_horizontal_separator(self, cell_width):
        """
        Create a horizontal separator line for the board.
        
        Args:
            cell_width (int): The width of each cell in characters
        
        Returns:
            str: Horizontal separator line
        """
        # Calculate separator parts based on subgrid size and cell width
        # Each cell takes (cell_width + 1) characters (including space)
        # Except the last cell in each subgrid (no trailing space)
        subgrid_width = self.subgrid_size * (cell_width + 1) - 1
        separator_parts = ["-" * subgrid_width] * self.subgrid_size
        
        return "+" + "+".join(separator_parts) + "+"

    def is_safe(self, row, col, num):
        """
        Check if placing 'num' at position (row, col) is valid according to Sudoku rules.
        
        Args:
            row (int): Row index (0-based)
            col (int): Column index (0-based)
            num (int): Number to check
            
        Returns:
            bool: True if placing the number is valid, False otherwise
        
        Raises:
            IndexError: If row or col is out of bounds
            ValueError: If num is invalid for the board size
        """
        # Validate inputs
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise IndexError(f"Position ({row}, {col}) is out of bounds for board of size {self.size}")
            
        if not (1 <= num <= self.size):
            raise ValueError(f"Number must be between 1 and {self.size}. Got {num}")
        
        # Check row constraint
        for c in range(self.size):
            if self.get_value(row, c) == num:
                return False
        
        # Check column constraint
        for r in range(self.size):
            if self.get_value(r, col) == num:
                return False
        
        # Check subgrid constraint
        subgrid_row = (row // self.subgrid_size) * self.subgrid_size
        subgrid_col = (col // self.subgrid_size) * self.subgrid_size
        
        for r in range(subgrid_row, subgrid_row + self.subgrid_size):
            for c in range(subgrid_col, subgrid_col + self.subgrid_size):
                if self.get_value(r, c) == num:
                    return False
        
        # If we've passed all checks, the placement is valid
        return True

    def is_valid(self):
        """
        Check if the entire board is valid according to Sudoku rules.
        
        Returns:
            bool: True if the board is valid, False otherwise
        """
        # Check each row for duplicates
        for row in range(self.size):
            values = set()
            for col in range(self.size):
                val = self.get_value(row, col)
                if val is not None:
                    if val in values:
                        return False  # Duplicate found in row
                    values.add(val)
        
        # Check each column for duplicates
        for col in range(self.size):
            values = set()
            for row in range(self.size):
                val = self.get_value(row, col)
                if val is not None:
                    if val in values:
                        return False  # Duplicate found in column
                    values.add(val)
        
        # Check each subgrid for duplicates
        for subgrid_row in range(0, self.size, self.subgrid_size):
            for subgrid_col in range(0, self.size, self.subgrid_size):
                values = set()
                for row in range(subgrid_row, subgrid_row + self.subgrid_size):
                    for col in range(subgrid_col, subgrid_col + self.subgrid_size):
                        val = self.get_value(row, col)
                        if val is not None:
                            if val in values:
                                return False  # Duplicate found in subgrid
                            values.add(val)
        
        # If we've passed all checks, the board is valid
        return True

    def update_possible_values(self, row=None, col=None, affected_only=False):
        """
        Update possible values for cells based on current board state.
        
        Args:
            row (int, optional): Specific row to update. If None, update all cells.
            col (int, optional): Specific column to update. If None, update all cells.
            affected_only (bool): If True, only update cells affected by the cell at (row, col)
            
        Note:
            - If both row and col are provided, updates only that specific cell or affected cells.
            - If both row and col are None, updates all cells on the board.
            - If only one of row or col is provided, the other must also be provided.
        
        Raises:
            ValueError: If only one of row or col is provided.
            IndexError: If row or col is out of bounds.
        """
        # Validate inputs
        if (row is None) != (col is None) and (row is not None or col is not None):
            raise ValueError("Both row and col must be provided together or both must be None.")
            
        # If specific cell is provided
        if row is not None and col is not None:
            if not (0 <= row < self.size and 0 <= col < self.size):
                raise IndexError(f"Position ({row}, {col}) is out of bounds for board of size {self.size}")
                
            # Reset possible values for the cell based on board size
            cell = self.get_cell(row, col)
            
            if affected_only:
                # Update only cells affected by (row, col)
                self._update_affected_cells(row, col)
            else:
                # Update the specific cell
                if cell.get_value() is not None:
                    # If cell has a value, possible values is just that value
                    cell.possible_values = {cell.get_value()}
                else:
                    # Otherwise, start with all values possible
                    cell.possible_values = set(range(1, self.size + 1))
                    
                    # Use cached information about restricted values if possible
                    restricted_values = self._get_restricted_values(row, col)
                    
                    # Remove all restricted values at once (set difference operation)
                    cell.possible_values -= restricted_values
        else:
            # Update all cells
            if affected_only:
                # Not applicable when no specific cell is provided
                affected_only = False
                
            for r in range(self.size):
                for c in range(self.size):
                    # Update each cell individually
                    self.update_possible_values(r, c, affected_only=False)
    
    def _update_affected_cells(self, row, col):
        """
        Update possible values for cells affected by a change at (row, col).
        This is a more efficient approach than updating all cells.
        
        Args:
            row (int): Row of the cell that was changed
            col (int): Column of the cell that was changed
        """
        value = self.get_value(row, col)
        
        if value is None:
            # If cell is now empty, update its own possible values
            self.update_possible_values(row, col, affected_only=False)
            return
            
        # For filled cells, update all cells in same row, column, and subgrid
        # Row cells
        for c in range(self.size):
            if c != col and self.is_empty(row, c):
                cell = self.get_cell(row, c)
                if value in cell.possible_values:
                    cell.possible_values.remove(value)
        
        # Column cells
        for r in range(self.size):
            if r != row and self.is_empty(r, col):
                cell = self.get_cell(r, col)
                if value in cell.possible_values:
                    cell.possible_values.remove(value)
        
        # Subgrid cells
        subgrid_row = (row // self.subgrid_size) * self.subgrid_size
        subgrid_col = (col // self.subgrid_size) * self.subgrid_size
        
        for r in range(subgrid_row, subgrid_row + self.subgrid_size):
            for c in range(subgrid_col, subgrid_col + self.subgrid_size):
                if (r != row or c != col) and self.is_empty(r, c):
                    cell = self.get_cell(r, c)
                    if value in cell.possible_values:
                        cell.possible_values.remove(value)
    
    def _get_restricted_values(self, row, col):
        """
        Get a set of values that are restricted for a cell based on row, column, and subgrid.
        This is cached for performance.
        
        Args:
            row (int): Row of the cell
            col (int): Column of the cell
            
        Returns:
            set: Set of values that cannot be placed in this cell
        """
        # Create a set to hold restricted values
        restricted_values = set()
        
        # Add values from the same row
        for c in range(self.size):
            val = self.get_value(row, c)
            if val is not None:
                restricted_values.add(val)
        
        # Add values from the same column
        for r in range(self.size):
            val = self.get_value(r, col)
            if val is not None:
                restricted_values.add(val)
        
        # Add values from the same subgrid
        subgrid_row = (row // self.subgrid_size) * self.subgrid_size
        subgrid_col = (col // self.subgrid_size) * self.subgrid_size
        
        for r in range(subgrid_row, subgrid_row + self.subgrid_size):
            for c in range(subgrid_col, subgrid_col + self.subgrid_size):
                val = self.get_value(r, c)
                if val is not None:
                    restricted_values.add(val)
        
        return restricted_values

    def copy(self):
        """
        Create a deep copy of the board.
        
        Returns:
            Board: A new Board instance with the same state
        """
        # Create a new board with the same size
        new_board = Board(self.size)
        
        # Copy each cell individually
        for row in range(self.size):
            for col in range(self.size):
                # Get the original cell and its copy
                original_cell = self.get_cell(row, col)
                new_cell = new_board.get_cell(row, col)
                
                # Copy the value
                value = original_cell.get_value()
                if value is not None:
                    new_cell.set_value(value)
                
                # Copy the possible values (directly access the attribute for efficiency)
                new_cell.possible_values = set(original_cell.possible_values)
        
        return new_board

    def get_mrv_cell(self):
        """
        Find the empty cell with the fewest possible values (Minimum Remaining Values heuristic).
        
        Returns:
            tuple or None: (row, col) of the cell with fewest possible values, or None if no empty cells exist
        """
        min_possibilities = float('inf')  # Start with infinity
        mrv_cell = None
        
        # Search all cells on the board
        for row in range(self.size):
            for col in range(self.size):
                # Skip cells that are already filled
                if not self.is_empty(row, col):
                    continue
                
                # Make sure possible values are up to date for this cell
                self.update_possible_values(row, col)
                
                # Get the number of possible values for this cell
                num_possibilities = len(self.get_cell(row, col).possible_values)
                
                # If this cell has fewer possibilities, update our MRV cell
                if num_possibilities < min_possibilities:
                    min_possibilities = num_possibilities
                    mrv_cell = (row, col)
                    
                    # If we found a cell with only one possibility, we can return immediately
                    # as this is the minimum possible
                    if num_possibilities == 1:
                        return mrv_cell
        
        # Return the cell with the fewest possibilities, or None if board is filled
        return mrv_cell

    def count_solutions(self, max_count=2):
        """
        Count the number of valid solutions for the current board state.
        
        Args:
            max_count (int): Maximum number of solutions to count before stopping.
                            Default is 2, which is useful for checking uniqueness.
        
        Returns:
            int: The number of solutions found (up to max_count).
        """
        # Track solutions found
        solutions = [0]
        
        # Make a copy of the board to work with
        board_copy = self.copy()
        # Update all possible values before starting
        board_copy.update_possible_values()
        
        def backtrack():
            # If we've already found max_count solutions, stop
            if solutions[0] >= max_count:
                return
                
            # Find the most constrained empty cell using MRV
            mrv_cell = board_copy.get_mrv_cell()
            
            # If no empty cells, we found a solution
            if mrv_cell is None:
                solutions[0] += 1
                return
            
            # Get the row and column of the MRV cell
            row, col = mrv_cell
            
            # Save possible values before any modifications
            possible_values = set(board_copy.get_cell(row, col).possible_values)
            
            # Try each possible value for this cell
            for num in possible_values:
                # Place the value
                board_copy.set_value(row, col, num)
                
                # Verify the move is valid (important for checking board consistency)
                if board_copy.is_valid():
                    # Update constraints
                    board_copy.update_possible_values()
                    
                    # Recurse to next cell
                    backtrack()
                    
                    # If we've reached max_count, stop processing further
                    if solutions[0] >= max_count:
                        board_copy.set_value(row, col, None)
                        return
                
                # Backtrack - remove the value
                board_copy.set_value(row, col, None)
            
            # Reset constraints after trying all values
            board_copy.update_possible_values(row, col)
        
        # Start backtracking
        backtrack()
        
        # Return the number of solutions found
        return solutions[0]

    def remove_clues(self, num_clues):
        """
        Remove clues from the board while ensuring a unique solution remains.
        
        This method attempts to remove clues until the specified number remains,
        checking after each removal that the puzzle still has exactly one solution.
        
        Args:
            num_clues (int): The desired number of clues to remain on the board
            
        Returns:
            bool: True if successfully reduced to exactly num_clues, 
                  False if couldn't remove enough clues while maintaining uniqueness
                  
        Raises:
            ValueError: If num_clues is invalid (less than minimum required or more than board size²)
        """
        # Validate input
        if num_clues <= 0:
            raise ValueError(f"Number of clues must be positive. Got {num_clues}")
        if num_clues > self.size * self.size:
            raise ValueError(f"Number of clues cannot exceed board size² ({self.size * self.size}). Got {num_clues}")
        
        # Get all filled positions
        filled_positions = []
        for row in range(self.size):
            for col in range(self.size):
                if not self.is_empty(row, col):
                    filled_positions.append((row, col))
        
        # Count current filled cells
        current_clues = len(filled_positions)
        
        # If we already have fewer clues than requested, we can't add any more
        if current_clues <= num_clues:
            return current_clues == num_clues
        
        # Create a copy of the board to work with
        board_copy = self.copy()
        
        # Shuffle the filled positions for random removal order
        import random
        random.shuffle(filled_positions)
        
        # Keep track of removals
        removed_positions = []
        
        # Try removing clues
        clues_to_remove = current_clues - num_clues
        for row, col in filled_positions:
            # Skip if we've already removed enough clues
            if len(removed_positions) >= clues_to_remove:
                break
            
            # Save the current value before removing
            value = board_copy.get_value(row, col)
            
            # Try removing this clue
            board_copy.set_value(row, col, None)
            board_copy.update_possible_values()  # Update constraints after removal
            
            # Check if the board still has exactly one solution
            if board_copy.count_solutions() == 1:
                # Removal was successful, update the original board
                self.set_value(row, col, None)
                self.update_possible_values(row, col)  # Update constraints for the original board too
                removed_positions.append((row, col))
            else:
                # Removal resulted in 0 or multiple solutions, put it back
                board_copy.set_value(row, col, value)
                board_copy.update_possible_values(row, col)  # Restore constraints
        
        # Check if we successfully removed enough clues
        return len(removed_positions) == clues_to_remove