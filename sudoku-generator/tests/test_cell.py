"""
Tests for the Cell class.
"""

import pytest
from src.sudoku.cell import Cell


def test_cell_initialization():
    """Test that a cell is initialized correctly."""
    # Create a cell with a value
    cell = Cell(1, 2, 5)
    assert cell.row == 1
    assert cell.col == 2
    assert cell.get_value() == 5
    
    # Create a cell without a value
    empty_cell = Cell(3, 4)
    assert empty_cell.row == 3
    assert empty_cell.col == 4
    assert empty_cell.get_value() is None


def test_cell_set_get_value():
    """Test setting and getting the cell value."""
    cell = Cell(0, 0)
    
    # Initially empty
    assert cell.get_value() is None
    
    # Set a value
    cell.set_value(7)
    assert cell.get_value() == 7
    
    # Change the value
    cell.set_value(9)
    assert cell.get_value() == 9
    
    # Clear the value
    cell.set_value(None)
    assert cell.get_value() is None


def test_cell_string_representation():
    """Test the string representation of a cell."""
    # Cell with value
    cell = Cell(0, 0, 3)
    assert str(cell) == '3'
    
    # Empty cell
    empty_cell = Cell(0, 0)
    assert str(empty_cell) == '.'
    
    # Representation should include position
    assert 'Cell(0, 0,' in repr(cell)
    assert '3)' in repr(cell)