#!/usr/bin/env python
"""
Example script for generating multiple Sudoku puzzles in batch.

This script demonstrates how to generate multiple puzzles with different
configurations and save them to files.
"""

import sys
import os
import time
import argparse
import json
from datetime import datetime

# Add the parent directory to path so we can import the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sudoku.generator import SudokuGenerator

def generate_puzzles(size, count, num_clues=None, symmetric=False, output_dir="puzzles"):
    """
    Generate multiple puzzles with specified parameters.
    
    Args:
        size (int): Size of the puzzles (4, 9, or 16)
        count (int): Number of puzzles to generate
        num_clues (int, optional): Number of clues for each puzzle
        symmetric (bool): Whether to use symmetric clue removal
        output_dir (str): Directory to save the puzzles
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Create a timestamp for the batch
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a generator instance
    generator = SudokuGenerator(size)
    
    # Statistics for the batch
    batch_stats = {
        "size": size,
        "count": count,
        "num_clues": num_clues,
        "symmetric": symmetric,
        "timestamp": timestamp,
        "total_time": 0,
        "puzzles": []
    }
    
    print(f"Generating {count} {size}x{size} puzzles with {'default' if num_clues is None else num_clues} clues...")
    
    # Record start time for the batch
    batch_start = time.time()
    
    # Generate each puzzle
    for i in range(count):
        print(f"Generating puzzle {i+1}/{count}...")
        start_time = time.time()
        
        try:
            # Generate the puzzle
            puzzle = generator.generate_puzzle(num_clues=num_clues, symmetric=symmetric)
            
            # Get statistics
            stats = generator.get_stats()
            
            # Create puzzle metadata
            puzzle_data = {
                "id": f"{size}x{size}_{timestamp}_{i+1}",
                "size": size,
                "num_clues": stats["num_clues"],
                "symmetric": stats["symmetric"],
                "generation_time": stats["generation_time"],
                "grid": [[puzzle.get_value(row, col) for col in range(size)] for row in range(size)]
            }
            
            # Save the puzzle to a JSON file
            filename = f"{output_dir}/puzzle_{size}x{size}_{timestamp}_{i+1}.json"
            with open(filename, "w") as f:
                json.dump(puzzle_data, f, indent=2)
            
            # Add to batch statistics
            puzzle_data["file"] = filename
            batch_stats["puzzles"].append(puzzle_data)
            
            print(f"  Puzzle saved to {filename} ({stats['generation_time']:.3f} seconds)")
        
        except Exception as e:
            print(f"  Error generating puzzle: {e}")
    
    # Complete batch statistics
    batch_stats["total_time"] = time.time() - batch_start
    batch_stats["avg_time"] = batch_stats["total_time"] / count if count > 0 else 0
    
    # Save batch statistics
    batch_file = f"{output_dir}/batch_{size}x{size}_{timestamp}.json"
    with open(batch_file, "w") as f:
        json.dump(batch_stats, f, indent=2)
    
    print(f"\nBatch generation complete!")
    print(f"Total time: {batch_stats['total_time']:.3f} seconds")
    print(f"Average time per puzzle: {batch_stats['avg_time']:.3f} seconds")
    print(f"Batch statistics saved to {batch_file}")

def main():
    """Parse arguments and generate puzzles."""
    parser = argparse.ArgumentParser(description="Generate multiple Sudoku puzzles in batch.")
    parser.add_argument("--size", type=int, choices=[4, 9, 16], default=9, 
                        help="Size of the puzzles (4, 9, or 16)")
    parser.add_argument("--count", type=int, default=5, 
                        help="Number of puzzles to generate")
    parser.add_argument("--clues", type=int, 
                        help="Number of clues for each puzzle (default depends on size)")
    parser.add_argument("--symmetric", action="store_true", 
                        help="Use symmetric clue removal")
    parser.add_argument("--output-dir", type=str, default="puzzles", 
                        help="Directory to save the puzzles")
    
    args = parser.parse_args()
    
    generate_puzzles(args.size, args.count, args.clues, args.symmetric, args.output_dir)

if __name__ == "__main__":
    main()