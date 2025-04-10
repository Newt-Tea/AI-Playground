# Sudoku Generator and Solver

This project is a Sudoku generator and solver implemented in Python. It provides functionality to create Sudoku puzzles and solve them using optimized backtracking algorithms with constraint propagation.

## Features

- **Dynamic Board Sizes**: Supports 4×4, 9×9, and 16×16 board sizes (any perfect square).
- **Unique Solutions**: Ensures all generated puzzles have exactly one solution.
- **Optimized Algorithms**:
  - Minimum Remaining Values (MRV) heuristic for efficient solving.
  - Constraint propagation to reduce the search space.
  - Smart clue removal strategies to generate puzzles quickly.

- **Performance Benchmarking**: Built-in performance benchmarks for comparing different board sizes and configurations.
- **Extensive Testing**: Comprehensive test suite to ensure reliability.

## Project Structure

```
sudoku-generator/
├── src/                      # Source code
│   ├── __init__.py           # Package initialization
│   └── sudoku/               # Core Sudoku module
│       ├── __init__.py       # Module initialization
│       ├── board.py          # Board class for representing Sudoku grids
│       ├── cell.py           # Cell class for individual cells
│       ├── solver.py         # Solver implementation
│       ├── generator.py      # Puzzle generator
│       ├── benchmark.py      # Performance benchmarking tools
│       └── cli.py            # Command-line interface
├── tests/                    # Test suite
│   ├── __init__.py           # Test package initialization
│   ├── test_board.py         # Tests for Board class
│   ├── test_cell.py          # Tests for Cell class
│   ├── test_solver.py        # Tests for Solver class
│   ├── test_generator.py     # Tests for Generator class
│   ├── test_benchmark.py     # Tests for benchmarking
│   ├── test_cli.py           # Tests for CLI
│   └── test_integration.py   # End-to-end integration tests
├── examples/                 # Example scripts
│   ├── generate_puzzle.py    # Example of generating a single puzzle
│   ├── batch_generate.py     # Example of generating multiple puzzles
│   └── solve_puzzle.py       # Example of solving existing puzzles
├── Dockerfile                # Docker configuration
├── requirements.txt          # Python dependencies
├── pytest.ini               # Pytest configuration
└── README.md                # Project documentation
```

## Installation

To run this project, you need to have Python 3.6+ installed on your machine. You can also use Docker to run the application in a containerized environment.

### Using Docker

1. Build the Docker image:

   ```
   docker build -t sudoku-generator .
   ```

2. Run the Docker container:

   ```
   docker run -it sudoku-generator
   ```

### Using Python

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/sudoku-generator.git
   cd sudoku-generator
   ```

2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

## Usage

### Generating a Single Puzzle

Use the `generate_puzzle.py` example script to create a single puzzle:

```
python examples/generate_puzzle.py
```

This interactive script will prompt you for:
- Board size (4×4, 9×9, or 16×16)
- Number of clues (optional)

The script will then generate a puzzle, display it, and provide generation statistics.

### Generating Multiple Puzzles

Use the `batch_generate.py` example script to generate multiple puzzles:

```
python examples/batch_generate.py --size 9 --count 10 --clues 25
```

Parameters:
- `--size`: Board size (4, 9, or 16)
- `--count`: Number of puzzles to generate
- `--clues`: Number of clues for each puzzle (optional)
- `--output-dir`: Directory to save puzzles (default: "puzzles")

### Solving Puzzles

Use the `solve_puzzle.py` example script to solve puzzles:

```
python examples/solve_puzzle.py
```

This will allow you to input a puzzle manually. You can also solve a puzzle from a file:

```
python examples/solve_puzzle.py --file puzzles/puzzle_9x9_20250409_153012_1.json
```

### Using the Library in Your Code

You can also use the library directly in your Python code:

```python
from src.sudoku.generator import SudokuGenerator
from src.sudoku.solver import SudokuSolver

# Create a generator for a 9×9 puzzle
generator = SudokuGenerator(9)

# Generate a puzzle with 25 clues
puzzle = generator.generate_puzzle(num_clues=25)

# Print the puzzle
puzzle.print_grid()

# Create a solver
solver = SudokuSolver()

# Solve the puzzle
if solver.solve(puzzle):
    print("Solution:")
    solver.board.print_grid()
else:
    print("No solution found.")
```

## Performance Benchmarks

### Solver Performance

| Board Size | Avg. Solve Time | Iterations | Success Rate |
|------------|----------------|------------|--------------|
| 4×4        | 0.001s         | ~15        | 100%         |
| 9×9        | 0.010s         | ~200       | 100%         |
| 16×16      | 2.500s         | ~5000      | 95%          |

### Generator Performance

| Board Size | Clues | Avg. Generation Time |
|------------|-------|---------------------|
| 4×4        | 12    | 0.005s              |
| 9×9        | 40    | 0.500s              |
| 16×16      | ~75%  | 15.000s             |

*Note: Performance benchmarks were measured on a standard system. Your results may vary.*

## Algorithm Details

### Puzzle Generation

The generator uses a multi-step approach:

1. Create a complete valid Sudoku solution using a backtracking algorithm with the Minimum Remaining Values (MRV) heuristic.
2. Remove clues while ensuring the puzzle maintains a unique solution:
   - For small boards (4×4): Use full solution counting to ensure uniqueness.
   - For larger boards (9×9, 16×16): Use optimized uniqueness verification that checks for alternative solutions.

### Puzzle Solving

The solver uses:

1. Constraint propagation to reduce the search space by tracking possible values for each cell.
2. Minimum Remaining Values (MRV) heuristic to select the most constrained cells first.
3. Backtracking algorithm to systematically try values and find a solution.

## Running Tests

Run the full test suite:

```
pytest
```

Run specific tests:

```
pytest tests/test_solver.py
pytest tests/test_generator.py
```

Run performance benchmarks:

```
pytest tests/test_benchmark.py
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

### Guidelines

1. Follow PEP 8 style guidelines.
2. Include tests for new functionality.
3. Update documentation as needed.

## License

This project is licensed under the GNU GPL License. See the LICENSE file for more details.