import random
import logging
import os
from solver import SudokuSolver
from board import Board

# Configure logging to show info or debug messages:
level = logging.DEBUG
logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

class SudokuGenerator:
    """
    A class to generate and manipulate Sudoku puzzles.
    """

    def __init__(self, size=9):
        """
        Initialize the SudokuGenerator with a given grid size.

        Args:
            size (int): The size of the Sudoku grid. Default is 9.
        """
        self.size = size
        self.board = Board(size)
        self.solver = SudokuSolver()  # Create an instance of SudokuSolver
        logging.info(f"Initialized SudokuGenerator with size {size}x{size}")

    def generate_puzzle(self, num_clues):
        """
        Generate a Sudoku puzzle with a specified number of clues.

        Args:
            num_clues (int): The number of clues to be left in the puzzle.
        """
        logging.info(f"Generating puzzle with {num_clues} clues")
        self.fill_grid()
        self.remove_clues(num_clues)
        logging.info("Puzzle generation complete")
        return self.board

    def fill_grid(self):
        """
        Fill the Sudoku grid with a valid solution using a backtracking algorithm.
        """
        logging.info("Filling grid with a valid solution")
        self.board.update_possible_values()
        self._fill_grid_helper()

    def _fill_grid_helper(self):
        """
        Helper method to fill the grid using backtracking and MRV heuristic.

        Returns:
            bool: True if the grid is successfully filled, False otherwise.
        """
        cell = self.board.get_mrv_cell()
        if not cell:
            return True
        row, col = cell.getposition()

        possible_values = list(self.board[row][col].possible_values)
        random.shuffle(possible_values)  # Shuffle the possible values to add randomness

        for num in possible_values:
            if self.board.is_safe(row, col, num):
                self.board[row][col].value = num
                self.board.update_possible_values(row, col)
                if self._fill_grid_helper():
                    return True
                self.board[row][col].value = 0
                self.board.update_possible_values(row, col)

        return False

    def remove_clues(self, num_clues):
        """
        Remove clues from the filled grid to create the puzzle.

        Args:
            num_clues (int): The number of clues to be left in the puzzle.
        """
        logging.info(f"Removing clues to leave {num_clues} clues in the puzzle")
        clues_left = self.size * self.size - num_clues
        empty_cells = set()
        while clues_left > 0:
            row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            while (row, col) in empty_cells or self.board[row][col].value == 0:
                row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            empty_cells.add((row, col))
            backup = self.board.copy()
            self.board[row][col].value = 0
            self.board.update_possible_values(row, col)
            for r in range(self.size):
                for c in range(self.size):
                    if c!=col and r!=row and self.board[r][c].value == 0: 
                        self.board[r][c].possible_values.discard(backup[row][col].value)

            board_copy = self.board.copy()
            if not self.solver.solve(board_copy):
                self.board = backup.copy()
                logging.debug(f"Restored to backup after finding grid\n{backup}\nunsolvable")
                empty_cells.remove((row, col))
            else:
                clues_left -= 1
                logging.debug(f"Removed cell ({row}, {col}) successfully")
            logging.debug(f"Clues remaining: {clues_left}")
        logging.info("Clue removal complete")

    def print_grid(self):
        """
        Print the Sudoku grid.
        """
        print(self.board)