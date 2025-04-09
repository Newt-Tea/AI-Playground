"""
Tests for the CLI module.

This module contains tests for the command-line interface for Sudoku generator.
"""
import pytest
import argparse
import json
import io
import sys
import logging
from unittest.mock import patch, MagicMock, call

from src.sudoku.cli import (
    setup_argparse, 
    configure_logging, 
    format_output, 
    write_output, 
    generate_puzzle,
    main
)
from src.sudoku.board import Board

class TestCLI:
    """Tests for the CLI module."""
    
    def test_argparse_setup(self):
        """Test that argparse is set up correctly."""
        parser = setup_argparse()
        assert isinstance(parser, argparse.ArgumentParser)
        
        # Test with default arguments
        args = parser.parse_args([])
        assert args.size == 9
        assert args.clues is None
        assert not args.symmetric
        assert args.format == "text"
        assert args.output is None
        assert not args.solve
        assert not args.stats
        assert args.verbose == 0
        assert not args.quiet
        
        # Test with custom arguments
        args = parser.parse_args([
            "--size", "4",
            "--clues", "7",
            "--symmetric",
            "--format", "json",
            "--output", "output.json",
            "--solve",
            "--stats",
            "-vv",
            "--quiet"
        ])
        assert args.size == 4
        assert args.clues == 7
        assert args.symmetric
        assert args.format == "json"
        assert args.output == "output.json"
        assert args.solve
        assert args.stats
        assert args.verbose == 2
        assert args.quiet
    
    @patch('src.sudoku.cli.logging.getLogger')
    def test_configure_logging(self, mock_get_logger):
        """Test that logging is configured correctly."""
        # Set up mock loggers that will be returned by logging.getLogger
        mock_sudoku_logger = MagicMock()
        mock_cli_logger = MagicMock()
        
        # Configure the mock to return our mock loggers
        # This patches the getLogger function to return our mocks based on the name
        mock_get_logger.side_effect = lambda name: {
            "sudoku": mock_sudoku_logger,
            "sudoku.cli": mock_cli_logger
        }.get(name, MagicMock())
        
        # Test with default verbosity (INFO)
        args = argparse.Namespace(verbose=0, quiet=False)
        configure_logging(args)
        mock_sudoku_logger.setLevel.assert_called_once_with(logging.INFO)
        # Reset mocks for next test
        mock_sudoku_logger.reset_mock()
        
        # Test with increased verbosity (DEBUG)
        args = argparse.Namespace(verbose=1, quiet=False)
        configure_logging(args)
        mock_sudoku_logger.setLevel.assert_called_once_with(logging.DEBUG)
        # Reset mocks for next test
        mock_sudoku_logger.reset_mock()
        
        # Test with quiet mode (ERROR)
        args = argparse.Namespace(verbose=0, quiet=True)
        configure_logging(args)
        mock_sudoku_logger.setLevel.assert_called_once_with(logging.ERROR)
    
    def test_format_output_text(self):
        """Test formatting output as text."""
        # Create a simple board for testing
        board = Board(4)
        board.set_value(0, 0, 1)
        board.set_value(1, 1, 2)
        
        # Create a solution board
        solution = Board(4)
        for row in range(4):
            for col in range(4):
                solution.set_value(row, col, (row + col) % 4 + 1)
        
        # Create sample stats
        stats = {
            "size": 4,
            "num_clues": 2,
            "generation_time": 0.123,
            "solution_generation_time": 0.045,
            "clue_removal_time": 0.078
        }
        
        # Test without solution or stats
        output = format_output(board, None, None, "text")
        assert "PUZZLE:" in output
        assert "SOLUTION:" not in output
        assert "STATISTICS:" not in output
        
        # Test with solution
        output = format_output(board, solution, None, "text")
        assert "PUZZLE:" in output
        assert "SOLUTION:" in output
        assert "STATISTICS:" not in output
        
        # Test with stats
        output = format_output(board, None, stats, "text")
        assert "PUZZLE:" in output
        assert "SOLUTION:" not in output
        assert "STATISTICS:" in output
        assert "generation_time: 0.123 seconds" in output
        
        # Test with solution and stats
        output = format_output(board, solution, stats, "text")
        assert "PUZZLE:" in output
        assert "SOLUTION:" in output
        assert "STATISTICS:" in output
    
    def test_format_output_csv(self):
        """Test formatting output as CSV."""
        # Create a simple board for testing
        board = Board(4)
        board.set_value(0, 0, 1)
        board.set_value(1, 1, 2)
        
        # Create a solution board
        solution = Board(4)
        for row in range(4):
            for col in range(4):
                solution.set_value(row, col, (row + col) % 4 + 1)
        
        # Test without solution
        output = format_output(board, None, None, "csv")
        lines = output.strip().split("\n")
        assert len(lines) == 4  # 4 rows for the puzzle
        assert lines[0] == "1,,,"  # First row, only first cell filled
        assert lines[1] == ",2,,"  # Second row, only second cell filled
        
        # Test with solution
        output = format_output(board, solution, None, "csv")
        lines = output.strip().split("\n")
        assert len(lines) == 9  # 4 rows for puzzle + empty line + 4 rows for solution
        assert lines[5] == "1,2,3,4"  # First row of solution
    
    def test_format_output_json(self):
        """Test formatting output as JSON."""
        # Create a simple board for testing
        board = Board(4)
        board.set_value(0, 0, 1)
        board.set_value(1, 1, 2)
        
        # Create a solution board
        solution = Board(4)
        for row in range(4):
            for col in range(4):
                solution.set_value(row, col, (row + col) % 4 + 1)
        
        # Create sample stats
        stats = {
            "size": 4,
            "num_clues": 2,
            "generation_time": 0.123
        }
        
        # Test with all options
        output = format_output(board, solution, stats, "json")
        data = json.loads(output)
        
        # Check basic structure
        assert "puzzle" in data
        assert "solution" in data
        assert "statistics" in data
        assert "size" in data
        assert "subgrid_size" in data
        
        # Check content
        assert data["size"] == 4
        assert data["subgrid_size"] == 2
        assert data["puzzle"][0][0] == 1
        assert data["puzzle"][1][1] == 2
        assert data["solution"][0][0] == 1
        assert data["statistics"]["size"] == 4
    
    @patch('builtins.open', new_callable=MagicMock)
    @patch('builtins.print')
    def test_write_output(self, mock_print, mock_open):
        """Test writing output to file or stdout."""
        # Test writing to stdout
        write_output("test output")
        mock_print.assert_called_once_with("test output")
        mock_open.assert_not_called()
        
        # Reset mocks
        mock_print.reset_mock()
        mock_open.reset_mock()
        
        # Test writing to file
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        write_output("test output", "output.txt")
        mock_print.assert_not_called()
        mock_open.assert_called_once_with("output.txt", "w")
        mock_file.write.assert_called_once_with("test output")
    
    @patch('src.sudoku.cli.SudokuGenerator')
    def test_generate_puzzle(self, mock_generator_class):
        """Test generating a puzzle."""
        # Set up mocks
        mock_generator = MagicMock()
        mock_generator_class.return_value = mock_generator
        
        mock_puzzle = MagicMock()
        mock_solution = MagicMock()
        mock_stats = {"generation_time": 0.5}
        
        mock_generator.generate_puzzle.return_value = mock_puzzle
        mock_generator.board = mock_solution
        mock_generator.get_stats.return_value = mock_stats
        
        # Test with minimal options
        args = argparse.Namespace(
            size=9,
            clues=None,
            symmetric=False,
            solve=False,
            stats=False
        )
        
        puzzle, solution, stats = generate_puzzle(args)
        
        # Check that the generator was initialized correctly
        mock_generator_class.assert_called_once_with(size=9)
        
        # Check that generate_puzzle was called correctly
        mock_generator.generate_puzzle.assert_called_once_with(
            num_clues=None,
            symmetric=False
        )
        
        # Check that the correct objects were returned
        assert puzzle == mock_puzzle
        assert solution is None
        assert stats is None
        
        # Reset mocks
        mock_generator_class.reset_mock()
        mock_generator.reset_mock()
        
        # Test with all options
        args = argparse.Namespace(
            size=4,
            clues=7,
            symmetric=True,
            solve=True,
            stats=True
        )
        
        puzzle, solution, stats = generate_puzzle(args)
        
        # Check that the generator was initialized correctly
        mock_generator_class.assert_called_once_with(size=4)
        
        # Check that generate_puzzle was called correctly
        mock_generator.generate_puzzle.assert_called_once_with(
            num_clues=7,
            symmetric=True
        )
        
        # Check that the correct objects were returned
        assert puzzle == mock_puzzle
        assert solution == mock_solution.copy.return_value
        assert stats is not None
    
    @patch('src.sudoku.cli.setup_argparse')
    @patch('src.sudoku.cli.configure_logging')
    @patch('src.sudoku.cli.generate_puzzle')
    @patch('src.sudoku.cli.format_output')
    @patch('src.sudoku.cli.write_output')
    def test_main(self, mock_write_output, mock_format_output, mock_generate_puzzle, 
                 mock_configure_logging, mock_setup_argparse):
        """Test the main function."""
        # Set up mocks
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_puzzle = MagicMock()
        mock_solution = MagicMock()
        mock_stats = MagicMock()
        mock_output = "formatted output"
        
        mock_setup_argparse.return_value = mock_parser
        mock_parser.parse_args.return_value = mock_args
        mock_generate_puzzle.return_value = (mock_puzzle, mock_solution, mock_stats)
        mock_format_output.return_value = mock_output
        
        # Set format attribute on mock_args
        mock_args.format = "text"
        mock_args.output = None
        
        # Call main function
        result = main()
        
        # Check that all the functions were called correctly
        mock_setup_argparse.assert_called_once()
        mock_parser.parse_args.assert_called_once()
        mock_configure_logging.assert_called_once_with(mock_args)
        mock_generate_puzzle.assert_called_once_with(mock_args)
        mock_format_output.assert_called_once_with(
            mock_puzzle, mock_solution, mock_stats, mock_args.format
        )
        mock_write_output.assert_called_once_with(mock_output, mock_args.output)
        
        # Check that main returned 0 (success)
        assert result == 0

    @patch('sys.argv', ['sudoku_cli.py', '--size', '4', '--clues', '7'])
    @patch('src.sudoku.cli.generate_puzzle')
    @patch('src.sudoku.cli.format_output')
    @patch('src.sudoku.cli.write_output')
    def test_main_integration(self, mock_write_output, mock_format_output, mock_generate_puzzle):
        """Test the main function with command line arguments."""
        # Set up mocks
        mock_puzzle = MagicMock()
        mock_solution = MagicMock()
        mock_stats = MagicMock()
        mock_output = "formatted output"
        
        mock_generate_puzzle.return_value = (mock_puzzle, mock_solution, mock_stats)
        mock_format_output.return_value = mock_output
        
        # Call main function
        result = main()
        
        # Check that functions were called with correct arguments
        args = mock_generate_puzzle.call_args[0][0]
        assert args.size == 4
        assert args.clues == 7
        
        # Check that main returned 0 (success)
        assert result == 0