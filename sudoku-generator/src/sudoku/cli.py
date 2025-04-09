#!/usr/bin/env python3
"""
Command-line interface for Sudoku generator.

This module provides a command-line entry point for generating Sudoku puzzles.
"""
import argparse
import logging
import sys
import time
from .generator import SudokuGenerator
from .solver import SudokuSolver

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("sudoku.cli")

def setup_argparse():
    """
    Set up argument parsing for the CLI.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        description="Generate Sudoku puzzles with configurable options."
    )
    
    # Board size option
    parser.add_argument(
        "--size", "-s", 
        type=int, 
        default=9,
        choices=[4, 9, 16, 25],
        help="Board size (must be a perfect square: 4, 9, 16, or 25). Default: 9"
    )
    
    # Number of clues option
    parser.add_argument(
        "--clues", "-c", 
        type=int, 
        help="Number of clues to include in the puzzle. Default: auto-calculated based on size"
    )
    
    # Symmetric removal option
    parser.add_argument(
        "--symmetric", 
        action="store_true",
        help="Remove clues symmetrically"
    )
    
    # Output format option
    parser.add_argument(
        "--format", "-f",
        choices=["text", "csv", "json"],
        default="text",
        help="Output format. Default: text"
    )
    
    # Output file option
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file. If not specified, prints to stdout"
    )
    
    # Solve option
    parser.add_argument(
        "--solve",
        action="store_true",
        help="Also display the solution"
    )
    
    # Statistics option
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Display generation statistics"
    )
    
    # Verbosity option
    parser.add_argument(
        "--verbose", "-v",
        action="count",
        default=0,
        help="Increase output verbosity (can be used multiple times)"
    )
    
    # Quiet option
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress all non-error output"
    )
    
    return parser

def configure_logging(args):
    """
    Configure logging based on command line arguments.
    
    Args:
        args (argparse.Namespace): Parsed command line arguments
    """
    # Determine log level based on verbosity and quiet flags
    if args.quiet:
        log_level = logging.ERROR
    else:
        # Default to INFO, but allow increasing verbosity
        log_levels = [logging.INFO, logging.DEBUG]
        # Cap the verbosity level at the maximum available
        verbosity = min(args.verbose, len(log_levels) - 1)
        log_level = log_levels[verbosity]
    
    # Set the log level
    logging.getLogger("sudoku").setLevel(log_level)
    logger.setLevel(log_level)

def format_output(board, solution, stats, output_format):
    """
    Format the board and solution according to the specified format.
    
    Args:
        board (Board): The generated Sudoku board
        solution (Board): The solved board (if requested)
        stats (dict): Generation statistics
        output_format (str): The desired output format ('text', 'csv', or 'json')
        
    Returns:
        str: Formatted output
    """
    if output_format == "text":
        # Plain text format
        result = []
        result.append("PUZZLE:")
        result.append(str(board))
        
        if solution:
            result.append("\nSOLUTION:")
            result.append(str(solution))
        
        if stats:
            result.append("\nSTATISTICS:")
            for key, value in stats.items():
                # Format times to be more readable
                if "time" in key and isinstance(value, float):
                    value = f"{value:.3f} seconds"
                result.append(f"  {key}: {value}")
        
        return "\n".join(result)
    
    elif output_format == "csv":
        # CSV format
        result = []
        
        # Add puzzle
        for row in range(board.size):
            row_values = []
            for col in range(board.size):
                value = board.get_value(row, col)
                row_values.append(str(value if value is not None else ""))
            result.append(",".join(row_values))
        
        # Add solution if present
        if solution:
            result.append("")  # Empty line separator
            for row in range(solution.size):
                row_values = []
                for col in range(solution.size):
                    value = solution.get_value(row, col)
                    row_values.append(str(value if value is not None else ""))
                result.append(",".join(row_values))
        
        return "\n".join(result)
    
    elif output_format == "json":
        # JSON format
        import json
        
        output = {
            "puzzle": [],
            "size": board.size,
            "subgrid_size": board.subgrid_size
        }
        
        # Add puzzle
        for row in range(board.size):
            row_values = []
            for col in range(board.size):
                row_values.append(board.get_value(row, col))
            output["puzzle"].append(row_values)
        
        # Add solution if present
        if solution:
            output["solution"] = []
            for row in range(solution.size):
                row_values = []
                for col in range(solution.size):
                    row_values.append(solution.get_value(row, col))
                output["solution"].append(row_values)
        
        # Add stats if present
        if stats:
            output["statistics"] = stats
        
        return json.dumps(output, indent=2)
    
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

def write_output(output, filename=None):
    """
    Write output to a file or stdout.
    
    Args:
        output (str): The formatted output to write
        filename (str, optional): The output file. If None, writes to stdout.
    """
    if filename:
        with open(filename, 'w') as f:
            f.write(output)
        logger.info(f"Output written to {filename}")
    else:
        print(output)

def generate_puzzle(args):
    """
    Generate a Sudoku puzzle based on command line arguments.
    
    Args:
        args (argparse.Namespace): Parsed command line arguments
        
    Returns:
        tuple: (puzzle, solution, stats) - The generated puzzle, solution (if requested), and statistics
    """
    try:
        # Start timing
        start_time = time.time()
        
        # Initialize generator
        generator = SudokuGenerator(size=args.size)
        logger.debug(f"Initialized SudokuGenerator with size {args.size}")
        
        # Generate puzzle
        logger.info(f"Generating Sudoku puzzle of size {args.size}...")
        puzzle = generator.generate_puzzle(
            num_clues=args.clues,
            symmetric=args.symmetric
        )
        logger.info(f"Puzzle generated successfully with {args.clues or 'auto-calculated'} clues")
        
        # Create solution if requested
        solution = None
        if args.solve:
            logger.info("Generating solution...")
            # The generator already has the complete solution
            solution = generator.board.copy()
        
        # Get statistics
        stats = None
        if args.stats:
            stats = generator.get_stats()
            # Add total generation time
            stats["total_time"] = time.time() - start_time
        
        return puzzle, solution, stats
        
    except Exception as e:
        logger.error(f"Error generating puzzle: {e}")
        sys.exit(1)

def main():
    """
    Main entry point for the Sudoku generator CLI.
    """
    # Parse arguments
    parser = setup_argparse()
    args = parser.parse_args()
    
    # Configure logging
    configure_logging(args)
    
    # Generate puzzle
    puzzle, solution, stats = generate_puzzle(args)
    
    # Format output
    output = format_output(puzzle, solution, stats, args.format)
    
    # Write output
    write_output(output, args.output)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())