# Sudoku Generator and Solver

This project is a Sudoku generator and solver implemented in Python. It provides functionality to create Sudoku puzzles and solve them using backtracking algorithms.

## Project Structure

```
sudoku-generator
├── src
│   ├── __init__.py
│   ├── generator.py
│   └── solver.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## Installation

To run this project, you need to have Python installed on your machine. You can also use Docker to run the application in a containerized environment.

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
   git clone https://github.com/Newt-Tea/AI-Playground.git
   cd sudoku-generator
   ```

2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

3. Run the application:

   ```
   python src/generator.py
   ```

## Usage

- The `SudokuGenerator` class in `generator.py` can be used to create Sudoku puzzles.
- The `SudokuSolver` class in `solver.py` can be used to solve Sudoku puzzles.
- The `Board` class in `board.py` can be used to create sudoku grids

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the project.

## License

This project is licensed under the GNU GPL License. See the LICENSE file for more details.