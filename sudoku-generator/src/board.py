class Cell:
    """
    A class to represent a cell in the Sudoku grid.
    """

    def __init__(self, value=0, row=None, col=None):
        """
        Initialize the Cell with a given value.

        Args:
            value (int): The value of the cell. Default is 0.
        """
        self.value = value
        self.possible_values = set(range(1, 10)) if value == 0 else set()
        self.row = row
        self.col = col

    def __repr__(self):
        """
        Return a string representation of the cell.
        """
        return str(self.value)
    
    def getposition(self):
        """
        Get the position of the cell in the grid.

        Returns:
            tuple: The row and column index of the cell.
        """
        return self.row, self.col


class Board:
    """
    A class to represent the Sudoku board.
    """

    def __init__(self, size=9):
        """
        Initialize the Board with a given size.

        Args:
            size (int): The size of the Sudoku grid. Default is 9.
        """
        self.size = size
        self.grid = [[Cell(0,r,c) for c in range(size)] for r in range(size)]

    def __getitem__(self, index):
        """
        Get a row of the grid.

        Args:
            index (int): The row index.

        Returns:
            list: The row of cells.
        """
        return self.grid[index]

    def __repr__(self):
        """
        Return a string representation of the board.
        """
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.grid)

    def is_safe(self, row, col, num):
        """
        Check if it's safe to place a number in a specific cell.

        Args:
            row (int): The row index.
            col (int): The column index.
            num (int): The number to be placed.

        Returns:
            bool: True if it's safe to place the number, False otherwise.
        """
        # Check row
        for c in range(self.size):
            if self.grid[row][c].value == num:
                return False

        # Check column
        for r in range(self.size):
            if self.grid[r][col].value == num:
                return False

        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.grid[r][c].value == num:
                    return False

        return True

    def update_possible_values(self, row=None, col=None):
        """
        Update the possible values for cells in the grid.

        Args:
            row (int, optional): The row index. Default is None.
            col (int, optional): The column index. Default is None.
        """
        if row is None and col is None:
            for row in range(self.size):
                for col in range(self.size):
                    self.update_cell_possible_values(row, col)
        else:
            self.update_cell_possible_values(row, col)

    def update_cell_possible_values(self, row, col):
        """
        Update the possible values for a specific cell and remove the old value from affected cells.

        Args:
            row (int): The row index.
            col (int): The column index.
        """
        # Update possible values for the changed cell
        if self.grid[row][col].value == 0:
            self.grid[row][col].possible_values = {
                num for num in range(1, 10) if self.is_safe(row, col, num)
            }
        else:
            self.grid[row][col].possible_values.clear()

        # Remove the old value from affected cells in the same row
        for c in range(self.size):
            if c != col and self.grid[row][c].value == 0:
                self.grid[row][c].possible_values.discard(self.grid[row][col].value)

        # Remove the old value from affected cells in the same column
        for r in range(self.size):
            if r != row and self.grid[r][col].value == 0:
                self.grid[r][col].possible_values.discard(self.grid[row][col].value)

        # Remove the old value from affected cells in the same 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r != row or c != col) and self.grid[r][c].value == 0:
                    self.grid[r][c].possible_values.discard(self.grid[row][col].value)

    def get_mrv_cell(self):
        """
        Find the cell with the minimum remaining values (MRV) in the grid.

        Returns:
            tuple: The row and column index of the MRV cell, or None if no empty cell is found.
        """
        min_values = self.size + 1
        mrv_cell = None
        for row in range(self.size):
            for col in range(self.size):
                cell = self.grid[row][col]
                if cell.value == 0 and len(cell.possible_values) < min_values:
                    min_values = len(cell.possible_values)
                    mrv_cell = self.grid[row][col]
        return mrv_cell

    def get_possible_values(self, row, col):
        """
        Get the possible values for a specific cell in the grid.

        Args:
            row (int): The row index.
            col (int): The column index.

        Returns:
            set: A set of possible values for the cell.
        """
        possible_values = set(range(1, 10))
        for num in range(1, 10):
            if not self.is_safe(row, col, num):
                possible_values.discard(num)
        return possible_values
    
    def copy(self):
        """
        Create a copy of the board.

        Returns:
            Board: A copy of the board.
        """
        board_copy = Board(self.size)
        for r in range(self.size):
            for c in range(self.size):
                board_copy.grid[r][c].value = self.grid[r][c].value
                board_copy.grid[r][c].possible_values = self.grid[r][c].possible_values.copy()
        return board_copy