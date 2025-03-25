"""
Board module for Sudoku generator.

This module contains the Board class which represents a Sudoku grid.
"""
import math
from .cell import Cell

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

    def update_possible_values(self, row=None, col=None):
        """
        Update possible values for cells based on current board state.
        
        Args:
            row (int, optional): Specific row to update. If None, update all cells.
            col (int, optional): Specific column to update. If None, update all cells.
            
        Note:
            - If both row and col are provided, updates only that specific cell.
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
            if cell.get_value() is not None:
                # If cell has a value, possible values is just that value
                cell.possible_values = {cell.get_value()}
            else:
                # Otherwise, start with all values possible
                cell.possible_values = set(range(1, self.size + 1))
                
                # Remove values from same row
                for c in range(self.size):
                    val = self.get_value(row, c)
                    if val is not None and val in cell.possible_values:
                        cell.possible_values.remove(val)
                
                # Remove values from same column
                for r in range(self.size):
                    val = self.get_value(r, col)
                    if val is not None and val in cell.possible_values:
                        cell.possible_values.remove(val)
                
                # Remove values from same subgrid
                subgrid_row = (row // self.subgrid_size) * self.subgrid_size
                subgrid_col = (col // self.subgrid_size) * self.subgrid_size
                
                for r in range(subgrid_row, subgrid_row + self.subgrid_size):
                    for c in range(subgrid_col, subgrid_col + self.subgrid_size):
                        val = self.get_value(r, c)
                        if val is not None and val in cell.possible_values:
                            cell.possible_values.remove(val)
        else:
            # Update all cells
            for r in range(self.size):
                for c in range(self.size):
                    # Recursively call this method for each cell
                    self.update_possible_values(r, c)