#!/usr/bin/env python
"""
Continuous Sudoku Puzzle Generation Test Script

This script attempts to generate Sudoku puzzles of different sizes repeatedly 
until a successful generation occurs or the user interrupts with Ctrl+C.
It collects and displays statistics about the generation process.
"""

import sys
import time
import signal
import statistics
from datetime import datetime, timedelta
import os

# Ensure we can access the src package
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.sudoku.generator import SudokuGenerator
from src.sudoku.solver import SudokuSolver


class TestStatistics:
    """Statistics collector for puzzle generation tests."""
    
    def __init__(self, board_size):
        """Initialize statistics for a specific board size."""
        self.board_size = board_size
        self.attempts = 0
        self.successful_generations = 0
        self.generation_times = []
        self.solution_generation_times = []
        self.removal_times = []
        self.attempt_counts = []
        self.start_time = time.time()
        self.last_success_time = None
    
    def record_attempt(self):
        """Record an attempted generation."""
        self.attempts += 1
    
    def record_success(self, stats):
        """Record a successful generation and its statistics."""
        self.successful_generations += 1
        self.generation_times.append(stats["generation_time"])
        self.solution_generation_times.append(stats["solution_generation_time"])
        self.removal_times.append(stats["clue_removal_time"])
        self.attempt_counts.append(stats["attempts"])
        self.last_success_time = time.time()
    
    def get_summary(self):
        """Get a summary of the statistics collected so far."""
        elapsed = time.time() - self.start_time
        
        summary = {
            "board_size": self.board_size,
            "total_attempts": self.attempts,
            "successful_generations": self.successful_generations,
            "success_rate": self.successful_generations / max(1, self.attempts),
            "elapsed_time": elapsed,
            "attempts_per_minute": self.attempts / (elapsed / 60) if elapsed > 0 else 0
        }
        
        # Add statistics for successful generations if any
        if self.successful_generations > 0:
            summary.update({
                "avg_generation_time": statistics.mean(self.generation_times),
                "min_generation_time": min(self.generation_times),
                "max_generation_time": max(self.generation_times),
                "avg_solution_time": statistics.mean(self.solution_generation_times),
                "avg_removal_time": statistics.mean(self.removal_times),
                "avg_attempts": statistics.mean(self.attempt_counts)
            })
            
            # Add standard deviation if we have more than one successful generation
            if self.successful_generations > 1:
                summary.update({
                    "stdev_generation_time": statistics.stdev(self.generation_times),
                    "stdev_attempts": statistics.stdev(self.attempt_counts)
                })
        
        return summary
    
    def display_summary(self):
        """Display a formatted summary of the statistics."""
        summary = self.get_summary()
        
        print(f"\n{'-'*60}")
        print(f"STATISTICS FOR {summary['board_size']}x{summary['board_size']} BOARD")
        print(f"{'-'*60}")
        
        # Format elapsed time nicely
        elapsed = timedelta(seconds=int(summary["elapsed_time"]))
        
        print(f"Total runtime: {elapsed}")
        print(f"Total attempts: {summary['total_attempts']}")
        print(f"Successful generations: {summary['successful_generations']}")
        print(f"Success rate: {summary['success_rate']*100:.2f}%")
        print(f"Attempts per minute: {summary['attempts_per_minute']:.2f}")
        
        # Show successful generation statistics if any
        if summary['successful_generations'] > 0:
            print(f"\nSuccessful Generation Statistics:")
            print(f"  Average generation time: {summary['avg_generation_time']:.3f}s")
            print(f"  Min/Max generation time: {summary['min_generation_time']:.3f}s / {summary['max_generation_time']:.3f}s")
            
            # Show standard deviation if more than one successful generation
            if summary['successful_generations'] > 1:
                print(f"  Generation time std dev: {summary['stdev_generation_time']:.3f}s")
                
            print(f"  Average solution time: {summary['avg_solution_time']:.3f}s")
            print(f"  Average removal time: {summary['avg_removal_time']:.3f}s")
            print(f"  Average attempts per puzzle: {summary['avg_attempts']:.1f}")
            
            if summary['successful_generations'] > 1:
                print(f"  Attempts std dev: {summary['stdev_attempts']:.1f}")
                
            # Show when the last successful generation was
            if self.last_success_time is not None:
                last_success_ago = timedelta(seconds=int(time.time() - self.last_success_time))
                print(f"  Last successful generation: {last_success_ago} ago")
                
        print(f"{'-'*60}\n")


def test_generation(board_size, num_clues=None, max_attempts=100, max_total_attempts=None, algorithm="optimized"):
    """
    Test Sudoku puzzle generation for a specific board size until successful or interrupted.
    
    Args:
        board_size (int): Size of the Sudoku board (4, 9, or 16)
        num_clues (int, optional): Number of clues to leave in the puzzle
        max_attempts (int): Maximum attempts for each generation try
        max_total_attempts (int, optional): Maximum total attempts before giving up
        algorithm (str): Algorithm to use for clue removal ("optimized" or "basic")
    
    Returns:
        TestStatistics: Statistics object with generation results
    """
    print(f"Starting continuous generation test for {board_size}x{board_size} board")
    if num_clues:
        print(f"Target: {num_clues} clues using {algorithm} algorithm")
    else:
        print(f"Using default number of clues with {algorithm} algorithm")
    print(f"Max attempts per generation: {max_attempts}")
    if max_total_attempts:
        print(f"Will stop after {max_total_attempts} total attempts")
    print("Press Ctrl+C to stop the test and view results\n")
    
    # Initialize statistics
    stats = TestStatistics(board_size)
    
    # Initialize generator
    generator = SudokuGenerator(board_size)
    
    try:
        while True:
            # Check if we've reached the maximum total attempts
            if max_total_attempts and stats.attempts >= max_total_attempts:
                print(f"\nReached maximum total attempts ({max_total_attempts})")
                break
                
            # Record attempt
            stats.record_attempt()
            
            # Show progress
            if stats.attempts % 10 == 0:
                elapsed = time.time() - stats.start_time
                attempts_per_min = stats.attempts / (elapsed / 60) if elapsed > 0 else 0
                print(f"Attempt {stats.attempts} | "
                      f"Time: {timedelta(seconds=int(elapsed))} | "
                      f"Rate: {attempts_per_min:.1f} attempts/min | "
                      f"Successes: {stats.successful_generations}")
            
            try:
                # Try to generate a puzzle
                puzzle = generator.generate_puzzle(
                    num_clues=num_clues,
                    max_attempts=max_attempts,
                    algorithm=algorithm
                )
                
                # Verify the puzzle has a unique solution
                if puzzle.count_solutions(max_count=2) == 1:
                    print(f"\n🎉 SUCCESS! Generated a {board_size}x{board_size} puzzle with a unique solution")
                    
                    # Record success and stats
                    stats.record_success(generator.get_stats())
                    
                    # Display the puzzle
                    print(f"\nGenerated Puzzle ({generator.stats['num_clues']} clues):")
                    puzzle.print_grid()
                    
                    # Display generation statistics
                    gen_stats = generator.get_stats()
                    print(f"\nGeneration Statistics:")
                    print(f"- Total generation time: {gen_stats['generation_time']:.3f}s")
                    print(f"- Solution generation time: {gen_stats['solution_generation_time']:.3f}s")
                    print(f"- Clue removal time: {gen_stats['clue_removal_time']:.3f}s")
                    print(f"- Number of attempts: {gen_stats['attempts']}")
                    
                    # Stats so far
                    stats.display_summary()
                else:
                    print(f"Warning: Generated puzzle does not have a unique solution!")
                    
            except RuntimeError as e:
                # Generation failed, continue with next attempt
                if stats.attempts % 10 == 0:
                    print(f"Generation attempt {stats.attempts} failed: {e}")
            except Exception as e:
                # Unexpected error
                print(f"Unexpected error in generation attempt {stats.attempts}: {e}")
                
    except KeyboardInterrupt:
        # User interrupted the test
        print("\n\nTest interrupted by user.")
    
    # Display final statistics
    stats.display_summary()
    return stats


def main():
    """Main entry point for the script."""
    print("Sudoku Puzzle Generator Continuous Test")
    print("======================================\n")
    
    # Define board sizes to test
    board_sizes = [9, 16]
    
    # Define maximum attempts for each board size
    max_attempts = {
        9: 25,    # Updated to match new defaults
        16: 40    # Updated to match new defaults
    }
    
    # Store statistics for each board size
    all_stats = {}
    
    try:
        for size in board_sizes:
            print(f"\n{'='*60}")
            print(f"TESTING {size}x{size} BOARD")
            print(f"{'='*60}\n")
            
            # Test with the appropriate max_attempts for this board size
            all_stats[size] = test_generation(
                board_size=size,
                max_attempts=max_attempts.get(size, 50),
                algorithm="optimized"
            )
            
    except KeyboardInterrupt:
        print("\n\nTesting interrupted by user. Displaying collected results.")
    
    # Display final summary for all board sizes
    print("\n\nFINAL SUMMARY")
    print("============")
    
    for size, stats in all_stats.items():
        summary = stats.get_summary()
        print(f"\n{size}x{size} Board:")
        print(f"- Attempts: {summary['total_attempts']}")
        print(f"- Successes: {summary['successful_generations']}")
        print(f"- Success rate: {summary['success_rate']*100:.2f}%")
        if summary['successful_generations'] > 0:
            print(f"- Average generation time: {summary['avg_generation_time']:.3f}s")
            print(f"- Average attempts per success: {summary['avg_attempts']:.1f}")


if __name__ == "__main__":
    # Register signal handler for cleaner interrupts
    # def signal_handler(sig, frame):
    #     print("\n\nReceived interrupt signal. Exiting gracefully...")
    #     sys.exit(0)
        
    # signal.signal(signal.SIGINT, signal_handler)
    
    # Run the main function
    main()