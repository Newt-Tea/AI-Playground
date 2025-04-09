# Sudoku Generator API Documentation

This document provides a detailed reference for all public classes and methods in the Sudoku Generator library.

## Table of Contents

- [Board Class](#board-class)
- [Cell Class](#cell-class)
- [SudokuSolver Class](#sudokusolver-class)
- [SudokuGenerator Class](#sudokugenerator-class)
- [Benchmark Module](#benchmark-module)

---

## Board Class

The `Board` class represents a Sudoku board and provides methods for manipulating and validating the grid.

### Constructor

```python
board = Board(size)
```

**Parameters:**
- `size` (int): The size of the board (must be a perfect square, e.g., 4, 9, 16)

**Raises:**
- `ValueError`: If the size is not a perfect square

### Methods

#### `get_value(row, col)`

Get the value at the specified position.

**Parameters:**
- `row` (int): Row index (0-based)
- `col` (int): Column index (0-based)

**Returns:**
- Value at the specified position or `None` if empty

#### `set_value(row, col, value)`

Set the value at the specified position.

**Parameters:**
- `row` (int): Row index (0-based)
- `col` (int): Column index (0-based)
- `value` (int or None): Value to set (None to clear the cell)

#### `get_cell(row, col)`

Get the Cell object at the specified position.

**Parameters:**
- `row` (int): Row index (0-based)
- `col` (int): Column index (0-based)

**Returns:**
- `Cell`: The Cell object at the specified position

#### `is_empty(row, col)`

Check if a cell is empty.

**Parameters:**
- `row` (int): Row index (0-based)
- `col` (int): Column index (0-based)

**Returns:**
- `bool`: True if the cell is empty, False otherwise

#### `get_empty_positions()`

Get a list of all empty positions on the board.

**Returns:**
- `list`: List of (row, col) tuples for empty cells

#### `is_safe(row, col, num)`

Check if it's safe to place a value at the specified position.

**Parameters:**
- `row` (int): Row index (0-based)
- `col` (int): Column index (0-based)
- `num` (int): Value to check

**Returns:**
- `bool`: True if the placement is valid, False otherwise

#### `is_valid()`

Check if the current board state is valid according to Sudoku rules.

**Returns:**
- `bool`: True if the board is valid, False otherwise

#### `update_possible_values(row=None, col=None, affected_only=False)`

Update the possible values for cells based on current constraints.

**Parameters:**
- `row` (int, optional): Row index to update
- `col` (int, optional): Column index to update
- `affected_only` (bool): If True, only update cells affected by the specified position

#### `get_mrv_cell()`

Find the cell with the minimum remaining values (MRV heuristic).

**Returns:**
- `tuple`: (row, col) of the cell with fewest possibilities, or None if no empty cells

#### `count_solutions(max_count=2)`

Count the number of solutions up to max_count.

**Parameters:**
- `max_count` (int): Maximum number of solutions to count

**Returns:**
- `int`: Number of solutions found, up to max_count

#### `copy()`

Create a deep copy of the board.

**Returns:**
- `Board`: A new Board object with the same state

#### `print_grid()`

Print the board to the console in a formatted grid.

#### `__str__()`

Return a string representation of the board.

**Returns:**
- `str`: String representation of the board

---

## Cell Class

The `Cell` class represents a single cell in a Sudoku grid.

### Constructor

```python
cell = Cell(row, col, value=None, possible_values=None)
```

**Parameters:**
- `row` (int): Row index of the cell
- `col` (int): Column index of the cell
- `value` (int, optional): Initial value of the cell
- `possible_values` (set, optional): Set of possible values for the cell

### Methods

#### `get_value()`

Get the cell's value.

**Returns:**
- Value of the cell or None if empty

#### `set_value(value)`

Set the cell's value.

**Parameters:**
- `value` (int or None): Value to set

#### `get_position()`

Get the cell's position.

**Returns:**
- `tuple`: (row, col)

#### `copy()`

Create a deep copy of the cell.

**Returns:**
- `Cell`: A new Cell object with the same state

#### `__str__()`

Return a string representation of the cell.

**Returns:**
- `str`: String representation of the cell

---

## SudokuSolver Class

The `SudokuSolver` class provides functionality for solving Sudoku puzzles.

### Constructor

```python
solver = SudokuSolver()
```

### Methods

#### `set_board(board)`

Set the board to solve.

**Parameters:**
- `board` (Board): The Sudoku board to solve

#### `solve(board=None, profile=False)`

Solve the Sudoku puzzle.

**Parameters:**
- `board` (Board, optional): The board to solve (if not already set)
- `profile` (bool): Whether to collect profiling data

**Returns:**
- `bool`: True if a solution was found, False otherwise

#### `print_solution()`

Print the solved board to the console.

**Raises:**
- `ValueError`: If no solution has been found

#### `get_stats()`

Get solving statistics.

**Returns:**
- `dict`: Dictionary containing solving statistics

---

## SudokuGenerator Class

The `SudokuGenerator` class provides functionality for generating Sudoku puzzles.

### Constructor

```python
generator = SudokuGenerator(size=9)
```

**Parameters:**
- `size` (int): Size of the board (default: 9)

### Methods

#### `generate_solution()`

Generate a complete valid Sudoku solution.

**Returns:**
- `Board`: A completely filled valid Sudoku board

#### `generate_puzzle(num_clues=None, symmetric=False, max_attempts=None)`

Generate a Sudoku puzzle by removing clues from a complete solution.

**Parameters:**
- `num_clues` (int, optional): Number of clues to leave in the puzzle
- `symmetric` (bool): Whether to remove clues symmetrically
- `max_attempts` (int, optional): Maximum number of generation attempts

**Returns:**
- `Board`: A Sudoku puzzle with the specified number of clues

**Raises:**
- `RuntimeError`: If failed to generate a puzzle after max_attempts

#### `get_stats()`

Get generation statistics.

**Returns:**
- `dict`: Dictionary containing generation statistics

---

## Benchmark Module

The `benchmark` module provides tools for benchmarking Sudoku generator and solver performance.

### Classes

#### `BenchmarkResult`

Container for benchmark results.

### Functions

#### `benchmark_solver(board_size=9, num_runs=5, profile=False)`

Benchmark the Sudoku solver on boards of specified size.

**Parameters:**
- `board_size` (int): Size of the board (default: 9)
- `num_runs` (int): Number of benchmark runs (default: 5)
- `profile` (bool): Whether to collect profiling data

**Returns:**
- `BenchmarkResult`: Object containing benchmark results and statistics

#### `benchmark_generator(board_size=9, num_clues=None, symmetric=False, num_runs=3)`

Benchmark the Sudoku puzzle generator.

**Parameters:**
- `board_size` (int): Size of the board (default: 9)
- `num_clues` (int, optional): Number of clues to leave in the puzzle
- `symmetric` (bool): Whether to generate symmetric puzzles
- `num_runs` (int): Number of benchmark runs (default: 3)

**Returns:**
- `BenchmarkResult`: Object containing benchmark results and statistics

#### `run_comprehensive_benchmarks()`

Run a comprehensive suite of benchmarks testing various board sizes and configurations.

**Returns:**
- `dict`: Dictionary of benchmark results organized by category and configuration