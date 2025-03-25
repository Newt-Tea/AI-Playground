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


def test_possible_values_initialization():
    """Test initialization of possible values."""
    # Default initialization for 9x9 board
    cell = Cell(0, 0)
    assert cell.possible_values == set(range(1, 10))
    
    # Initialization with a value
    cell = Cell(0, 0, value=5)
    assert cell.possible_values == {5}
    
    # Initialization with custom possible values
    cell = Cell(0, 0, possible_values={1, 3, 5})
    assert cell.possible_values == {1, 3, 5}
    
    # Initialization with different board size
    cell = Cell(0, 0, board_size=4)
    assert cell.possible_values == {1, 2, 3, 4}

def test_set_value_updates_possible_values():
    """Test that setting a value updates possible values."""
    cell = Cell(0, 0, board_size=9)
    assert cell.possible_values == set(range(1, 10))
    
    cell.set_value(5)
    assert cell.possible_values == {5}

def test_get_position():
    """Test getting cell position."""
    cell = Cell(3, 7)
    assert cell.get_position() == (3, 7)
    
    cell = Cell(0, 0)
    assert cell.get_position() == (0, 0)
    
    cell = Cell(8, 8)
    assert cell.get_position() == (8, 8)

def test_cell_copy():
    """Test deep copying of cells."""
    # Create original cell
    original = Cell(2, 4, value=7)
    
    # Create a copy
    copy = original.copy()
    
    # Verify all attributes are the same
    assert copy.row == original.row
    assert copy.col == original.col
    assert copy.value == original.value
    assert copy.possible_values == original.possible_values
    
    # Verify it's a deep copy by modifying the copy
    copy.set_value(9)
    assert original.value == 7
    assert copy.value == 9
    assert original.possible_values == {7}
    assert copy.possible_values == {9}

def test_cell_copy_with_no_value():
    """Test deep copying of cells with no value."""
    # Create original cell with no value
    original = Cell(2, 4, possible_values={1, 2, 3})
    
    # Create a copy
    copy = original.copy()
    
    # Verify attributes are the same
    assert copy.row == original.row
    assert copy.col == original.col
    assert copy.value == original.value
    assert copy.possible_values == original.possible_values
    
    # Verify it's a deep copy by modifying the copy
    copy.possible_values.remove(1)
    assert 1 in original.possible_values
    assert 1 not in copy.possible_values

def test_edge_cases():
    """Test edge cases for possible values."""
    # Empty possible values
    cell = Cell(0, 0, possible_values=set())
    assert cell.possible_values == set()
    
    # Large board size
    cell = Cell(0, 0, board_size=16)
    assert len(cell.possible_values) == 16
    assert all(v in cell.possible_values for v in range(1, 17))