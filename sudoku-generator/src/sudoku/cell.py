"""
Cell module for Sudoku generator.

This module contains the Cell class which represents a single cell in a Sudoku grid.
"""


class Cell:
    """Represents a single cell in a Sudoku puzzle."""
    
    def __init__(self, row, col, value=None, possible_values=None, board_size=9):
        """
        Initialize a Sudoku cell.
        
        Args:
            row (int): Row index (0-based)
            col (int): Column index (0-based)
            value (int, optional): Cell value. Defaults to None (empty cell).
            possible_values (set, optional): Set of possible values for this cell.
                                           If None, will be initialized based on board size.
            board_size (int, optional): Size of the Sudoku board. Defaults to 9.
        """
        self.row = row
        self.col = col
        self.value = value
        
        # Initialize possible values if not provided
        if possible_values is not None:
            self.possible_values = set(possible_values)
        else:
            # If cell has a value, possible values is just that value
            if value is not None:
                self.possible_values = {value}
            else:
                # Otherwise, all values from 1 to board_size are possible
                self.possible_values = set(range(1, board_size + 1))
    
    def get_value(self):
        """Get the current value of the cell."""
        return self.value
    
    def set_value(self, value):
        """
        Set the value of the cell.
        
        Args:
            value (int or None): The new value for the cell.
        """
        self.value = value
        if value is not None:
            # When setting a value, update possible values to only that value
            self.possible_values = {value}
    
    def get_position(self):
        """
        Get the position of the cell as (row, col).
        
        Returns:
            tuple: (row, column) position
        """
        return (self.row, self.col)
    
    def copy(self):
        """
        Create a deep copy of this cell.
        
        Returns:
            Cell: A new Cell instance with the same attributes
        """
        # Create a new cell with the same row, col and value
        new_cell = Cell(self.row, self.col, self.value)
        # Explicitly copy the possible values to ensure deep copy
        new_cell.possible_values = set(self.possible_values)
        return new_cell
    
    def __str__(self):
        """String representation of the cell."""
        if self.value is None:
            return "."
        return str(self.value)
    
    def __repr__(self):
        """
        Detailed representation of the cell.
        
        Returns:
            str: Detailed string showing position and value
        """
        return f"Cell({self.row}, {self.col}, {self.value})"