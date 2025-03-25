# Sudoku Generator Specification

## Overview
The goal is to implement a Sudoku generator that:
1. Dynamically supports `n x n` boards (where `n` is a perfect square).
2. Ensures every generated puzzle has a **single unique solution**.
3. Allows the user to specify the number of clues remaining after generation.
4. Prioritizes **speed** while introducing a small amount of randomness.
5. Includes robust logging for debugging and analysis.

---

## Requirements

### Core Functionality
1. **Dynamic Board Size**:
   - Support `n x n` boards where `n` is a perfect square (e.g., 4x4, 9x9, 16x16).
   - Automatically calculate subgrid size (`sqrt(n)`).

2. **Puzzle Generation**:
   - Start with a blank board.
   - Generate a fully solved board using a **backtracking algorithm** with **forward checking**.
   - Remove clues until the specified number of clues remains, ensuring the puzzle has a **single unique solution**.

3. **Validation**:
   - Use the same backtracking algorithm to validate that the puzzle has a single unique solution.
   - Log feedback if the puzzle is unsolvable or has multiple solutions.

4. **Randomness**:
   - Introduce randomness by shuffling possible values during backtracking.
   - Randomize the order of clue removal.

5. **Logging**:
   - Support configurable log levels (`INFO`, `DEBUG`).
   - Default to `INFO` if no log level is specified.
   - Provide a summary at the end of generation:
     - Total attempts made.
     - Total time elapsed.
     - Average time per attempt.
   - Optionally log to a file with filenames based on datetime (e.g., `logs/sudoku_generator_YYYY-MM-DD_HH-MM-SS.log`).
   - Automatically create the `logs` directory if it doesn’t exist.

---

## Architecture

### Classes
1. **`Cell`**:
   - Represents a single cell in the Sudoku grid.
   - **Attributes**:
     - `value`: The current value of the cell.
     - `possible_values`: A set of possible values for the cell.
     - `row`, `col`: The cell's position in the grid.
   - **Methods**:
     - `get_position`: Returns the cell's position.
     - `copy`: Creates a deep copy of the cell.

2. **`Board`**:
   - Represents the Sudoku board.
   - **Attributes**:
     - `size`: The size of the board (`n x n`).
     - `grid`: A 2D list of `Cell` objects.
   - **Methods**:
     - `is_safe(row, col, num)`: Check if placing `num` in a cell is valid.
     - `update_possible_values(row=None, col=None)`: Update possible values for a specific cell or all cells.
     - `get_mrv_cell()`: Return the cell with the minimum remaining values (MRV).
     - `copy()`: Create a deep copy of the board.

3. **`SudokuGenerator`**:
   - Handles puzzle generation and clue removal.
   - **Attributes**:
     - `size`: The size of the board.
     - `board`: The `Board` object.
     - `solver`: An instance of `SudokuSolver`.
     - `log_level`: The logging level (`INFO`, `DEBUG`).
   - **Methods**:
     - `generate_puzzle(num_clues)`: Generate a puzzle with the specified number of clues.
     - `fill_grid()`: Generate a fully solved board using backtracking.
     - `_fill_grid_helper()`: Recursive helper for backtracking.
     - `remove_clues(num_clues)`: Remove clues while ensuring a unique solution.
     - `print_grid()`: Print the board to the console.

4. **`SudokuSolver`**:
   - Handles puzzle solving and validation.
   - **Methods**:
     - `solve(board)`: Solve the puzzle using backtracking.
     - `print_grid()`: Print the solved board.

---

## Data Handling

### Input
- **Board Size**: `n x n` (where `n` is a perfect square).
- **Number of Clues**: The number of clues to leave on the board.
- **Log Level**: Configurable (`INFO`, `DEBUG`).

### Output
- **Generated Puzzle**: A `Board` object representing the puzzle.
- **Logs**: Output to the console and/or a file.

### Error Handling
1. **Invalid Board Size**:
   - Raise a `ValueError` if `n` is not a perfect square.

2. **Invalid Clue Count**:
   - Raise a `ValueError` if `num_clues` is less than `n` or greater than `n^2`.

3. **Logging Errors**:
   - If logging to a file fails (e.g., due to permissions), fall back to console logging and log the error.

4. **Infinite Loop Prevention**:
   - If the generator fails to create a valid puzzle after a certain number of attempts (e.g., 1000), log an error and exit gracefully.

---

## Testing Plan

### Unit Tests
1. **`Cell` Class**:
   - Ensure `possible_values` updates correctly.
   - Validate `copy()` functionality.

2. **`Board` Class**:
   - Validate `is_safe()` logic.
   - Test `update_possible_values()` for specific cells and the entire board.
   - Ensure `get_mrv_cell()` returns the correct cell.

3. **`SudokuSolver` Class**:
   - Verify that puzzles are solved correctly.
   - Ensure the solver detects multiple solutions.

4. **`SudokuGenerator` Class**:
   - Validate that generated puzzles have the correct number of clues.
   - Ensure puzzles have a single unique solution.

### Integration Tests
- Generate puzzles of various sizes (e.g., 4x4, 9x9, 16x16) and validate their solutions.
- Test logging functionality (console and file).

### Performance Tests
- Measure the time taken to generate puzzles with different board sizes and clue counts.
- Ensure the generator performs efficiently under typical use cases.

### Edge Cases
- Minimum board size (e.g., 4x4).
- Maximum board size (e.g., 16x16 or larger).
- Very low or very high clue counts.

---

This specification provides a clear roadmap for implementing the Sudoku generator. Let me know if you need further clarification or adjustments!