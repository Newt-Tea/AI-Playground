from board import Board
class SudokuSolver:
    """
    A class to solve Sudoku puzzles.
    """

    def __init__(self):
        """
        Initialize the SudokuSolver.
        """
        pass

    def solve(self, board):
        """
        Solve the Sudoku puzzle using a backtracking algorithm with MRV heuristic.

        Args:
            board (Board): The Sudoku board to be solved.

        Returns:
            bool: True if the puzzle is solved, False otherwise.
        """
        empty = board.get_mrv_cell()
        if not empty:
            return True  # Puzzle solved
        row, col = empty.getposition()

        for num in board[row][col].possible_values:
            if board.is_safe(row, col, num):
                board[row][col].value = num
                board.update_possible_values(row, col)
                if self.solve(board):
                    return True
                board[row][col].value = 0
                board.update_possible_values(row, col)

        return False

    def print_grid(self):
        """
        Print the Sudoku grid.
        """
        for row in self.grid:
            print(" ".join(str(num) for num in row))