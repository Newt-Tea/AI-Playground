"""
Tests for the Board class.
"""
import pytest
from src.sudoku.board import Board

def test_board_initialization_valid_sizes():
    """Test board initialization with valid sizes."""
    # Test with size 4 (2x2 subgrids)
    board_4 = Board(4)
    assert board_4.get_size() == 4
    assert board_4.get_subgrid_size() == 2
    
    # Test with size 9 (3x3 subgrids)
    board_9 = Board(9)
    assert board_9.get_size() == 9
    assert board_9.get_subgrid_size() == 3
    
    # Test with size 16 (4x4 subgrids)
    board_16 = Board(16)
    assert board_16.get_size() == 16
    assert board_16.get_subgrid_size() == 4
    
    # Test default constructor (size 9)
    board_default = Board()
    assert board_default.get_size() == 9
    assert board_default.get_subgrid_size() == 3

def test_board_initialization_invalid_sizes():
    """Test board initialization with invalid sizes."""
    # Test with non-perfect square sizes
    with pytest.raises(ValueError):
        Board(3)
    
    with pytest.raises(ValueError):
        Board(7)
    
    with pytest.raises(ValueError):
        Board(10)

def test_get_set_cell_values():
    """Test getting and setting cell values."""
    board = Board(9)
    
    # Test setting values
    board.set_value(0, 0, 5)
    board.set_value(1, 2, 7)
    board.set_value(8, 8, 9)
    
    # Test getting values
    assert board.get_value(0, 0) == 5
    assert board.get_value(1, 2) == 7
    assert board.get_value(8, 8) == 9
    assert board.get_value(3, 3) is None  # Unset cell
    
    # Test changing values
    board.set_value(0, 0, 6)
    assert board.get_value(0, 0) == 6
    
    # Test clearing values
    board.set_value(0, 0, None)
    assert board.get_value(0, 0) is None

def test_get_cell():
    """Test getting cell objects."""
    board = Board(9)
    board.set_value(1, 1, 5)
    
    cell = board.get_cell(1, 1)
    assert cell.get_value() == 5
    assert cell.get_position() == (1, 1)

def test_out_of_bounds_access():
    """Test error handling for out-of-bounds access."""
    board = Board(9)
    
    with pytest.raises(IndexError):
        board.get_value(-1, 5)
    
    with pytest.raises(IndexError):
        board.get_value(9, 5)
    
    with pytest.raises(IndexError):
        board.get_value(5, -1)
    
    with pytest.raises(IndexError):
        board.get_value(5, 9)
    
    with pytest.raises(IndexError):
        board.set_value(-1, 5, 6)
    
    with pytest.raises(IndexError):
        board.get_cell(9, 9)

def test_invalid_values():
    """Test error handling for invalid values."""
    board = Board(9)
    
    with pytest.raises(ValueError):
        board.set_value(0, 0, 0)  # Too small
    
    with pytest.raises(ValueError):
        board.set_value(0, 0, 10)  # Too large
    
    # None is valid (clears the cell)
    board.set_value(0, 0, None)
    assert board.get_value(0, 0) is None

def test_is_empty():
    """Test is_empty method."""
    board = Board(9)
    
    # All cells should be empty initially
    assert board.is_empty(0, 0) is True
    assert board.is_empty(3, 4) is True
    assert board.is_empty(8, 8) is True
    
    # Set some values and check again
    board.set_value(0, 0, 5)
    board.set_value(3, 4, 7)
    
    assert board.is_empty(0, 0) is False
    assert board.is_empty(3, 4) is False
    assert board.is_empty(8, 8) is True
    
    # Clear a value and check again
    board.set_value(0, 0, None)
    assert board.is_empty(0, 0) is True

def test_get_empty_positions():
    """Test get_empty_positions method."""
    board = Board(4)  # 4x4 board for simplicity
    
    # Initially all cells are empty
    empty_positions = board.get_empty_positions()
    assert len(empty_positions) == 16  # 4x4 = 16 cells
    
    # Fill some cells
    board.set_value(0, 0, 1)
    board.set_value(1, 1, 2)
    board.set_value(2, 2, 3)
    board.set_value(3, 3, 4)
    
    # Check empty positions after filling
    empty_positions = board.get_empty_positions()
    assert len(empty_positions) == 12  # 16 - 4 = 12 empty cells
    
    # Check specific positions are not in the empty positions list
    assert (0, 0) not in empty_positions
    assert (1, 1) not in empty_positions
    assert (2, 2) not in empty_positions
    assert (3, 3) not in empty_positions
    
    # But other positions are empty
    assert (0, 1) in empty_positions
    assert (1, 0) in empty_positions

def test_string_representation():
    """Test string representation with grid lines."""
    board = Board(4)  # 4x4 board for clearer visualization
    
    # Set some values
    board.set_value(0, 0, 1)
    board.set_value(0, 3, 4)
    board.set_value(3, 0, 3)
    board.set_value(3, 3, 2)
    
    # Get the string representation
    board_str = str(board)
    
    # Verify the formatting includes separators
    assert "+" in board_str  # Should have horizontal separators
    assert "|" in board_str  # Should have vertical separators
    
    # Check grid contents (basic validation)
    lines = board_str.strip().split("\n")
    assert len(lines) > 4  # Should have more lines than just the board size due to separators
    
    # Verify grid lines appear at subgrid boundaries
    # For a 4x4 board, we should have a separator after row 1 (0-indexed)
    has_separator = False
    for line in lines:
        if "+" in line:
            has_separator = True
            break
    assert has_separator

def test_print_grid(capsys):
    """Test print_grid method."""
    board = Board(4)
    board.set_value(0, 0, 1)
    
    # Call the print method
    board.print_grid()
    
    # Capture the output
    captured = capsys.readouterr()
    
    # Verify something was printed
    assert len(captured.out) > 0
    
    # Should match the string representation
    assert captured.out.strip() == str(board).strip()

def test_is_safe_row_constraint():
    """Test is_safe method for row constraint."""
    board = Board(9)
    board.set_value(0, 0, 5)
    
    # Same row should fail
    assert board.is_safe(0, 1, 5) is False
    
def test_is_safe_column_constraint():
    """Test is_safe method for column constraint."""
    board = Board(9)
    board.set_value(0, 0, 5)
    
    # Same column should fail
    assert board.is_safe(1, 0, 5) is False
    
def test_is_safe_subgrid_constraint():
    """Test is_safe method for subgrid constraint."""
    board = Board(9)  # 3x3 subgrids
    board.set_value(0, 0, 5)
    
    # Same subgrid should fail
    assert board.is_safe(1, 1, 5) is False
    
    # Different subgrid should pass
    assert board.is_safe(3, 3, 5) is True

def test_is_safe_empty_position():
    """Test is_safe method on an empty board."""
    board = Board(9)
    
    # Empty board should allow any valid placement
    assert board.is_safe(4, 4, 5) is True
    assert board.is_safe(0, 0, 1) is True
    assert board.is_safe(8, 8, 9) is True

def test_is_safe_invalid_inputs():
    """Test is_safe method with invalid inputs."""
    board = Board(9)
    
    # Out of bounds positions
    with pytest.raises(IndexError):
        board.is_safe(-1, 5, 1)
    
    with pytest.raises(IndexError):
        board.is_safe(9, 5, 1)
    
    # Invalid numbers
    with pytest.raises(ValueError):
        board.is_safe(0, 0, 0)
    
    with pytest.raises(ValueError):
        board.is_safe(0, 0, 10)

def test_is_valid_empty_board():
    """Test is_valid method on an empty board."""
    board = Board(9)
    
    # Empty board should be valid
    assert board.is_valid() is True

def test_is_valid_valid_board():
    """Test is_valid method on a valid board."""
    board = Board(4)  # 4x4 board for simplicity
    
    # Create a valid board
    board.set_value(0, 0, 1)
    board.set_value(0, 1, 2)
    board.set_value(0, 2, 3)
    board.set_value(0, 3, 4)
    
    board.set_value(1, 0, 3)
    board.set_value(1, 1, 4)
    board.set_value(1, 2, 1)
    board.set_value(1, 3, 2)
    
    board.set_value(2, 0, 2)
    board.set_value(2, 1, 1)
    board.set_value(2, 2, 4)
    board.set_value(2, 3, 3)
    
    board.set_value(3, 0, 4)
    board.set_value(3, 1, 3)
    board.set_value(3, 2, 2)
    board.set_value(3, 3, 1)
    
    # This board should be valid
    assert board.is_valid() is True

def test_is_valid_row_violation():
    """Test is_valid method with row constraint violation."""
    board = Board(4)
    
    # Add a duplicate in a row
    board.set_value(0, 0, 1)
    board.set_value(0, 1, 1)  # Same value in the same row
    
    assert board.is_valid() is False

def test_is_valid_column_violation():
    """Test is_valid method with column constraint violation."""
    board = Board(4)
    
    # Add a duplicate in a column
    board.set_value(0, 0, 1)
    board.set_value(1, 0, 1)  # Same value in the same column
    
    assert board.is_valid() is False

def test_is_valid_subgrid_violation():
    """Test is_valid method with subgrid constraint violation."""
    board = Board(4)  # 2x2 subgrids
    
    # Add a duplicate in a subgrid
    board.set_value(0, 0, 1)
    board.set_value(1, 1, 1)  # Same value in the same subgrid
    
    assert board.is_valid() is False

def test_is_valid_multiple_violations():
    """Test is_valid method with multiple violations."""
    board = Board(4)
    
    # Add multiple constraint violations
    board.set_value(0, 0, 1)
    board.set_value(0, 1, 1)  # Row violation
    board.set_value(1, 0, 1)  # Column violation
    
    assert board.is_valid() is False

def test_update_possible_values_single_cell():
    """Test updating possible values for a single cell."""
    board = Board(4)  # 4x4 board for simplicity
    
    # Initially, cell (0,0) should have all values possible
    cell = board.get_cell(0, 0)
    assert cell.possible_values == {1, 2, 3, 4}
    
    # Set value in same row
    board.set_value(0, 1, 1)
    
    # Update possible values for cell (0,0)
    board.update_possible_values(0, 0)
    
    # Now cell (0,0) should not have 1 as a possible value
    assert cell.possible_values == {2, 3, 4}
    
    # Set value in same column
    board.set_value(1, 0, 2)
    
    # Update possible values for cell (0,0)
    board.update_possible_values(0, 0)
    
    # Now cell (0,0) should not have 1 or 2 as possible values
    assert cell.possible_values == {3, 4}
    
    # Set value in same subgrid (for 4x4 board, subgrids are 2x2)
    board.set_value(1, 1, 3)
    
    # Update possible values for cell (0,0)
    board.update_possible_values(0, 0)
    
    # Now cell (0,0) should only have 4 as possible value
    assert cell.possible_values == {4}

def test_update_possible_values_all_cells():
    """Test updating possible values for all cells."""
    board = Board(4)
    
    # Set some values
    board.set_value(0, 0, 1)
    board.set_value(0, 1, 2)
    board.set_value(1, 0, 3)
    
    # Update all cells
    board.update_possible_values()
    
    # Check a few cells
    # Cell (0,2) should not have 1 or 2 (same row)
    assert board.get_cell(0, 2).possible_values == {3, 4}
    
    # Cell (2,0) should not have 1 or 3 (same column)
    assert board.get_cell(2, 0).possible_values == {2, 4}
    
    # Cell (1,1) should not have 1 (subgrid), 2 (subgrid), or 3 (same row)
    assert board.get_cell(1, 1).possible_values == {4}

def test_update_possible_values_for_filled_cell():
    """Test updating possible values for a cell with a value already set."""
    board = Board(4)
    
    # Set a value
    board.set_value(0, 0, 1)
    
    # Update that cell's possible values
    board.update_possible_values(0, 0)
    
    # Cell should only have its own value as possible
    assert board.get_cell(0, 0).possible_values == {1}
    
    # Change the value
    board.set_value(0, 0, 2)
    board.update_possible_values(0, 0)
    
    # Possible values should update
    assert board.get_cell(0, 0).possible_values == {2}

def test_update_possible_values_propagation():
    """Test that constraint propagation properly cascades across the board."""
    board = Board(4)
    
    # Setting values should reduce options for other cells
    board.set_value(0, 0, 1)
    board.set_value(1, 1, 2)
    board.set_value(2, 2, 3)
    
    # Update all possible values
    board.update_possible_values()
    
    # Check that constraint propagation worked properly
    # Cell (0,1) can't have 1 (same row)
    assert 1 not in board.get_cell(0, 1).possible_values
    
    # Cell (1,0) can't have 1 (same subgrid) or 2 (same row)
    assert 1 not in board.get_cell(1, 0).possible_values
    assert 2 not in board.get_cell(1, 0).possible_values
    
    # Cell (2,0) can't have 1 (same column)
    assert 1 not in board.get_cell(2, 0).possible_values
    
    # Cell (3,3) can't have 3 (same column and row)
    assert 3 not in board.get_cell(3, 3).possible_values

def test_update_possible_values_reset():
    """Test resetting possible values when a cell value is removed."""
    board = Board(4)
    
    # Set a value
    board.set_value(0, 0, 1)
    
    # Update all cells
    board.update_possible_values()
    
    # Cell (0,1) should not have 1 as possible
    assert 1 not in board.get_cell(0, 1).possible_values
    
    # Now remove the value
    board.set_value(0, 0, None)
    
    # Update all cells
    board.update_possible_values()
    
    # Now cell (0,1) should have 1 as possible again
    assert 1 in board.get_cell(0, 1).possible_values
    
    # And cell (0,0) should have all values possible again
    assert board.get_cell(0, 0).possible_values == {1, 2, 3, 4}

def test_update_possible_values_invalid_inputs():
    """Test update_possible_values with invalid inputs."""
    board = Board(4)
    
    # Only one of row or col provided
    with pytest.raises(ValueError):
        board.update_possible_values(row=1)
    
    with pytest.raises(ValueError):
        board.update_possible_values(col=1)
    
    # Out of bounds
    with pytest.raises(IndexError):
        board.update_possible_values(4, 0)
    
    with pytest.raises(IndexError):
        board.update_possible_values(0, 4)

def test_board_copy_basic():
    """Test that copying a board creates an independent copy."""
    original = Board(9)
    
    # Set some values in the original
    original.set_value(0, 0, 1)
    original.set_value(1, 1, 2)
    original.set_value(2, 2, 3)
    
    # Create a copy
    copy = original.copy()
    
    # Verify the copy has the same values
    assert copy.get_value(0, 0) == 1
    assert copy.get_value(1, 1) == 2
    assert copy.get_value(2, 2) == 3
    
    # Verify the copy has the same size
    assert copy.get_size() == original.get_size()
    assert copy.get_subgrid_size() == original.get_subgrid_size()

def test_board_copy_independence():
    """Test that modifying the copy doesn't affect the original."""
    original = Board(4)
    original.set_value(0, 0, 1)
    
    # Create a copy
    copy = original.copy()
    
    # Modify the copy
    copy.set_value(0, 0, 2)
    copy.set_value(1, 1, 3)
    
    # Check that the original is unchanged
    assert original.get_value(0, 0) == 1
    assert original.get_value(1, 1) is None
    
    # Check that the copy was modified
    assert copy.get_value(0, 0) == 2
    assert copy.get_value(1, 1) == 3
    
    # Modify the original
    original.set_value(2, 2, 4)
    
    # Check that the copy is unchanged
    assert copy.get_value(2, 2) is None

def test_board_copy_deep():
    """Test that the copy includes deep copies of all cells."""
    original = Board(4)
    
    # Set a value and update possible values
    original.set_value(0, 0, 1)
    original.update_possible_values()
    
    # Create a copy
    copy = original.copy()
    
    # Get cells from both boards
    original_cell = original.get_cell(1, 1)
    copy_cell = copy.get_cell(1, 1)
    
    # Check that the cells have the same possible values
    assert copy_cell.possible_values == original_cell.possible_values
    
    # Modify possible values in the copy
    old_possible = set(copy_cell.possible_values)
    copy_cell.possible_values.clear()
    
    # Check that the original cell's possible values are unchanged
    assert original_cell.possible_values == old_possible
    assert copy_cell.possible_values != original_cell.possible_values

def test_board_copy_different_sizes():
    """Test that copying works for boards of different sizes."""
    # Test with 4x4 board
    board_4 = Board(4)
    board_4.set_value(0, 0, 1)
    copy_4 = board_4.copy()
    assert copy_4.get_size() == 4
    assert copy_4.get_value(0, 0) == 1
    
    # Test with 9x9 board
    board_9 = Board(9)
    board_9.set_value(0, 0, 1)
    copy_9 = board_9.copy()
    assert copy_9.get_size() == 9
    assert copy_9.get_value(0, 0) == 1
    
    # Test with 16x16 board
    board_16 = Board(16)
    board_16.set_value(0, 0, 1)
    copy_16 = board_16.copy()
    assert copy_16.get_size() == 16
    assert copy_16.get_value(0, 0) == 1

def test_board_copy_different_states():
    """Test that copying works for boards in different states."""
    # Empty board
    empty = Board(4)
    empty_copy = empty.copy()
    assert all(empty_copy.get_value(r, c) is None 
               for r in range(4) for c in range(4))
    
    # Partially filled board
    partial = Board(4)
    partial.set_value(0, 0, 1)
    partial.set_value(1, 1, 2)
    partial_copy = partial.copy()
    assert partial_copy.get_value(0, 0) == 1
    assert partial_copy.get_value(1, 1) == 2
    assert partial_copy.get_value(2, 2) is None
    
    # Completely filled board
    full = Board(4)
    for r in range(4):
        for c in range(4):
            full.set_value(r, c, ((r*2 + c) % 4) + 1)  # Simple pattern to fill board
    
    full_copy = full.copy()
    for r in range(4):
        for c in range(4):
            assert full_copy.get_value(r, c) == full.get_value(r, c)