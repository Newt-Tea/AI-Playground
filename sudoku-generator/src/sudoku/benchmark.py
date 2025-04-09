"""
Benchmark module for measuring Sudoku generator and solver performance.

This module provides tools for benchmarking the Sudoku generator and solver
functionality across different board sizes and configurations.
"""

import time
import gc
import statistics
import psutil
import os
from contextlib import contextmanager
from src.sudoku.generator import SudokuGenerator
from src.sudoku.solver import SudokuSolver
from src.sudoku.board import Board

class BenchmarkResult:
    """Container for benchmark results."""
    
    def __init__(self):
        """Initialize an empty benchmark result."""
        self.times = []
        self.iterations = []
        self.memory_usages = []
        self.success_rate = 0.0
        self.board_size = None
        self.num_clues = None
        self.symmetric = None
    
    def add_run(self, time_taken, iterations, memory_usage):
        """
        Add the results from a single benchmark run.
        
        Args:
            time_taken (float): Time taken for the run in seconds
            iterations (int): Number of iterations/steps performed
            memory_usage (float): Peak memory usage during the run in MB
        """
        self.times.append(time_taken)
        self.iterations.append(iterations)
        self.memory_usages.append(memory_usage)
    
    def finalize(self, success_count, total_runs, board_size, num_clues=None, symmetric=False):
        """
        Finalize the benchmark result with summary statistics.
        
        Args:
            success_count (int): Number of successful runs
            total_runs (int): Total number of runs attempted
            board_size (int): Size of the board used in the benchmark
            num_clues (int, optional): Number of clues for puzzle generation
            symmetric (bool): Whether symmetry was used in puzzle generation
        """
        self.success_rate = success_count / total_runs if total_runs > 0 else 0.0
        self.board_size = board_size
        self.num_clues = num_clues
        self.symmetric = symmetric
    
    def get_summary(self):
        """
        Get a summary of the benchmark results.
        
        Returns:
            dict: Dictionary containing benchmark summary statistics
        """
        if not self.times:
            return {"error": "No benchmark data available"}
        
        time_stats = {
            "mean": statistics.mean(self.times),
            "median": statistics.median(self.times),
            "min": min(self.times),
            "max": max(self.times)
        }
        
        if len(self.times) > 1:
            time_stats["stdev"] = statistics.stdev(self.times)
        
        memory_stats = {
            "mean_mb": statistics.mean(self.memory_usages),
            "max_mb": max(self.memory_usages)
        }
        
        iteration_stats = {
            "mean": statistics.mean(self.iterations),
            "median": statistics.median(self.iterations),
            "min": min(self.iterations),
            "max": max(self.iterations)
        }
        
        return {
            "board_size": self.board_size,
            "num_clues": self.num_clues,
            "symmetric": self.symmetric,
            "success_rate": self.success_rate,
            "time": time_stats,
            "memory": memory_stats,
            "iterations": iteration_stats
        }
    
    def __str__(self):
        """
        String representation of the benchmark result.
        
        Returns:
            str: Formatted benchmark summary
        """
        summary = self.get_summary()
        if "error" in summary:
            return summary["error"]
        
        result = []
        result.append(f"Benchmark Summary (Board size: {summary['board_size']})")
        
        if summary['num_clues'] is not None:
            result.append(f"Puzzle generation with {summary['num_clues']} clues")
            result.append(f"Symmetric: {summary['symmetric']}")
        
        result.append(f"Success Rate: {summary['success_rate']*100:.1f}%")
        result.append(f"Time (seconds):")
        result.append(f"  Mean: {summary['time']['mean']:.6f}")
        result.append(f"  Median: {summary['time']['median']:.6f}")
        result.append(f"  Min: {summary['time']['min']:.6f}")
        result.append(f"  Max: {summary['time']['max']:.6f}")
        
        if "stdev" in summary["time"]:
            result.append(f"  Std Dev: {summary['time']['stdev']:.6f}")
        
        result.append(f"Memory Usage (MB):")
        result.append(f"  Mean: {summary['memory']['mean_mb']:.2f}")
        result.append(f"  Max: {summary['memory']['max_mb']:.2f}")
        
        result.append(f"Iterations:")
        result.append(f"  Mean: {summary['iterations']['mean']:.1f}")
        result.append(f"  Median: {summary['iterations']['median']}")
        
        return "\n".join(result)


@contextmanager
def memory_usage_monitor():
    """
    Context manager to monitor memory usage during a block of code.
    
    Yields:
        float: Peak memory usage in MB
    """
    process = psutil.Process(os.getpid())
    
    # Record the starting memory usage
    start_memory = process.memory_info().rss / (1024 * 1024)  # Convert to MB
    peak_memory = start_memory
    
    try:
        yield lambda: peak_memory - start_memory
    finally:
        # Record the final memory usage
        current_memory = process.memory_info().rss / (1024 * 1024)
        peak_memory = max(peak_memory, current_memory)


def benchmark_solver(board_size=9, num_runs=5, profile=False):
    """
    Benchmark the Sudoku solver on boards of specified size.
    
    Args:
        board_size (int): Size of the Sudoku board to benchmark (default: 9)
        num_runs (int): Number of benchmark runs (default: 5)
        profile (bool): Whether to collect profiling data
        
    Returns:
        BenchmarkResult: Object containing benchmark results and statistics
    """
    generator = SudokuGenerator(board_size)
    solver = SudokuSolver()
    result = BenchmarkResult()
    
    success_count = 0
    
    for _ in range(num_runs):
        # Generate a complete board
        full_board = generator.generate_solution()
        
        # Make a random puzzle with half the cells revealed
        puzzle = full_board.copy()
        
        # Remove a fixed percentage of clues
        target_clues = board_size * board_size // 2
        
        # Make a copy with 50% of cells empty for testing solver performance
        positions = [(row, col) for row in range(board_size) for col in range(board_size)]
        import random
        random.shuffle(positions)
        
        # Keep only the target number of clues
        for i, (row, col) in enumerate(positions):
            if i >= target_clues:
                puzzle.set_value(row, col, None)
        
        # Force garbage collection before benchmark
        gc.collect()
        
        # Benchmark solving
        with memory_usage_monitor() as memory_getter:
            try:
                # Record start time
                start_time = time.time()
                
                # Solve the puzzle
                success = solver.solve(puzzle, profile=profile)
                
                # Record end time
                end_time = time.time()
                
                if success:
                    success_count += 1
                    
                    # Add performance data
                    result.add_run(
                        end_time - start_time,
                        solver.iterations,
                        memory_getter()
                    )
            except Exception as e:
                print(f"Error during solving benchmark: {e}")
                continue
    
    # Finalize the benchmark result
    result.finalize(success_count, num_runs, board_size)
    
    return result


def benchmark_generator(board_size=9, num_clues=None, symmetric=False, num_runs=3):
    """
    Benchmark the Sudoku puzzle generator.
    
    Args:
        board_size (int): Size of the Sudoku board to benchmark (default: 9)
        num_clues (int, optional): Number of clues to leave in the puzzle
        symmetric (bool): Whether to generate symmetric puzzles
        num_runs (int): Number of benchmark runs (default: 3)
        
    Returns:
        BenchmarkResult: Object containing benchmark results and statistics
    """
    generator = SudokuGenerator(board_size)
    result = BenchmarkResult()
    
    success_count = 0
    
    for _ in range(num_runs):
        # Force garbage collection before benchmark
        gc.collect()
        
        # Benchmark generation
        with memory_usage_monitor() as memory_getter:
            try:
                # Record start time
                start_time = time.time()
                
                # Generate a puzzle
                puzzle = generator.generate_puzzle(num_clues=num_clues, symmetric=symmetric)
                
                # Record end time
                end_time = time.time()
                
                # Verify the generated puzzle has the requested number of clues
                filled_cells = sum(1 for row in range(board_size) for col in range(board_size) 
                                  if not puzzle.is_empty(row, col))
                
                if num_clues is None or filled_cells == num_clues:
                    success_count += 1
                    
                    # Extract iterations from generator stats
                    iterations = generator.stats.get("attempts", 1)
                    
                    # Add performance data
                    result.add_run(
                        end_time - start_time,
                        iterations,
                        memory_getter()
                    )
            except Exception as e:
                print(f"Error during generation benchmark: {e}")
                continue
    
    # Finalize the benchmark result
    result.finalize(success_count, num_runs, board_size, num_clues, symmetric)
    
    return result


def run_comprehensive_benchmarks():
    """
    Run a comprehensive suite of benchmarks testing various board sizes and configurations.
    
    Returns:
        dict: Dictionary of benchmark results organized by category and configuration
    """
    results = {
        "solver": {},
        "generator": {}
    }
    
    # Benchmark solver for different board sizes
    for size in [4, 9, 16]:
        print(f"Benchmarking solver for {size}x{size} board...")
        results["solver"][size] = benchmark_solver(size, num_runs=3).get_summary()
    
    # Benchmark generator for different board sizes and configurations
    for size, configs in [
        (4, [{"num_clues": 7, "symmetric": False}, {"num_clues": 8, "symmetric": True}]),
        (9, [{"num_clues": 25, "symmetric": False}, {"num_clues": 30, "symmetric": True}]),
        (16, [{"num_clues": None, "symmetric": False}])  # Use default clues for 16x16
    ]:
        results["generator"][size] = {}
        
        for config in configs:
            config_name = f"{config['num_clues']}_clues_{'sym' if config['symmetric'] else 'nonsym'}"
            print(f"Benchmarking generator for {size}x{size} board with {config_name}...")
            
            results["generator"][size][config_name] = benchmark_generator(
                size, 
                config["num_clues"], 
                config["symmetric"],
                num_runs=2  # Reduced for larger boards as they take longer
            ).get_summary()
    
    return results


def compare_implementations(old_func, new_func, input_data, num_runs=10):
    """
    Compare performance of two implementations of the same function.
    Useful for measuring the impact of optimizations.
    
    Args:
        old_func (callable): The original function implementation
        new_func (callable): The optimized function implementation
        input_data: Input data to pass to both functions
        num_runs (int): Number of runs for each function
        
    Returns:
        dict: Performance comparison statistics
    """
    old_times = []
    new_times = []
    
    # Benchmark old implementation
    for _ in range(num_runs):
        gc.collect()
        start_time = time.time()
        old_func(input_data)
        old_times.append(time.time() - start_time)
    
    # Benchmark new implementation
    for _ in range(num_runs):
        gc.collect()
        start_time = time.time()
        new_func(input_data)
        new_times.append(time.time() - start_time)
    
    # Calculate statistics
    old_avg = statistics.mean(old_times)
    new_avg = statistics.mean(new_times)
    improvement = (old_avg - new_avg) / old_avg * 100 if old_avg > 0 else 0
    
    return {
        "old_implementation": {
            "mean": old_avg,
            "min": min(old_times),
            "max": max(old_times)
        },
        "new_implementation": {
            "mean": new_avg,
            "min": min(new_times),
            "max": max(new_times)
        },
        "improvement_percentage": improvement
    }