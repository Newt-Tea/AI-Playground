"""
Test suite for the Sudoku Generator project.

This package contains test modules for validating the functionality of the Sudoku
generator components. It uses pytest for test discovery and execution.

Test Modules:
    - test_cell.py: Tests for the Cell class functionality
    - test_board.py: Tests for the Board class functionality

Running Tests:
    Run all tests with pytest from the project root:
        pytest

    Run specific test modules:
        pytest tests/test_cell.py
        pytest tests/test_board.py

    Run with coverage:
        pytest --cov=src tests/

Test Organization:
    Tests are organized by component, with each test function focusing on
    a specific functionality or edge case. All tests are designed to be
    independent and should not rely on the state from other tests.
"""