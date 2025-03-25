"""
Cell module for Sudoku generator.

This module contains the Cell class which represents a single cell in a Sudoku grid.
"""


class Cell:
    """
    Represents a single cell in a Sudoku grid.
    
    Each cell has a value (or None if empty), and a position (row, column).
    """
    
    def __init__(self, row, col, value=None):
        """
        Initialize a Cell object.
        
        Args:
            row (int): Row position (0-indexed)
            col (int): Column position (0-indexed)
            value (int, optional): Cell value. Defaults to None.
        """
        self.row = row
        self.col = col
        self.value = value
    
    def get_value(self):
        """
        Get the current value of the cell.
        
        Returns:
            int or None: The cell's value, or None if empty
        """
        return self.value
    
    def set_value(self, value):
        """
        Set the value of the cell.
        
        Args:
            value (int or None): The value to set, or None to clear
        """
        self.value = value
    
    def __str__(self):
        """
        String representation of the cell.
        
        Returns:
            str: String representation showing value or '.' if empty
        """
        return str(self.value) if self.value is not None else '.'
    
    def __repr__(self):
        """
        Detailed representation of the cell.
        
        Returns:
            str: Detailed string showing position and value
        """
        return f"Cell({self.row}, {self.col}, {self.value})"