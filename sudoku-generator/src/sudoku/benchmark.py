"""
Benchmarking module for Sudoku generator.

This module provides performance testing utilities for the Sudoku generator.
"""
import time
import gc
import statistics
import psutil
import os
from .board import Board
from .solver import SudokuSolver
from .generator import SudokuGenerator

class SudokoBenchmark:
    """Class for benchmarking Sudoku generator and solver performance."""
    
    def __init__(self):
        """Initialize a new benchmark instance."""
        self.results = {}
    
    def benchmark_solver(self, board_size=9, num_runs=5, difficulty='medium'):
        """
        Benchmark the solver performance.
        
        Args:
            board_size (int): Size of the board to test
            num_runs (int): Number of runs for averaging
            difficulty (str): Difficulty level ('easy', 'medium', 'hard')
                             Controls the number of clues
        
        Returns:
            dict: Performance metrics
        """
        # Determine number of clues based on difficulty
        if difficulty == 'easy':
            clue_factor = 0.5  # 50% of cells filled
        elif difficulty == 'medium':
            clue_factor = 0.35  # 35% of cells filled
        else:  # hard
            clue_factor = 0.25  # 25% of cells filled
            
        num_clues = int(board_size * board_size * clue_factor)
        
        # Create generator and solver
        generator = SudokuGenerator(board_size)
        solver = SudokuSolver()
        
        # Metrics to track
        solve_times = []
        iterations_list = []
        memory_usages = []
        success_count = 0
        
        # Generate and solve multiple puzzles
        for _ in range(num_runs):
            # Generate a puzzle
            puzzle = generator.generate_puzzle(num_clues=num_clues)
            
            # Force garbage collection for more accurate timing
            gc.collect()
            
            # Measure memory before solving
            process = psutil.Process(os.getpid())
            mem_before = process.memory_info().rss / (1024 * 1024)  # Convert to MB
            
            # Solve it and measure performance
            success = solver.solve(puzzle)
            
            # Measure memory after solving
            mem_after = process.memory_info().rss / (1024 * 1024)  # Convert to MB
            memory_usages.append(mem_after - mem_before)
            
            if success:
                success_count += 1
                solve_times.append(solver.solve_time)
                iterations_list.append(solver.iterations)
        
        # Calculate statistics
        if solve_times:
            avg_time = statistics.mean(solve_times)
            avg_iterations = statistics.mean(iterations_list)
            min_time = min(solve_times)
            max_time = max(solve_times)
            avg_memory = statistics.mean(memory_usages)
        else:
            avg_time = avg_iterations = min_time = max_time = avg_memory = 0
        
        success_rate = (success_count / num_runs) * 100 if num_runs > 0 else 0
        
        # Store and return results
        result = {
            'board_size': board_size,
            'num_clues': num_clues,
            'difficulty': difficulty,
            'num_runs': num_runs,
            'avg_time_sec': avg_time,
            'min_time_sec': min_time,
            'max_time_sec': max_time,
            'avg_iterations': avg_iterations,
            'avg_memory_mb': avg_memory,
            'success_rate': success_rate
        }
        
        self.results['solver'] = result
        return result
    
    def benchmark_generator(self, board_size=9, num_runs=5, num_clues=None, symmetric=False):
        """
        Benchmark the generator performance.
        
        Args:
            board_size (int): Size of the board to generate
            num_runs (int): Number of runs for averaging
            num_clues (int, optional): Number of clues to leave
            symmetric (bool): Whether to use symmetric clue removal
        
        Returns:
            dict: Performance metrics
        """
        # Default num_clues if not specified
        if num_clues is None:
            if board_size == 4:
                num_clues = 7
            elif board_size == 9:
                num_clues = 25
            else:
                num_clues = board_size * board_size // 3
        
        # Metrics to track
        generation_times = []
        removal_times = []
        total_times = []
        memory_usages = []
        success_count = 0
        
        # Generate multiple puzzles
        for _ in range(num_runs):
            gc.collect()  # Force garbage collection
            
            # Create generator and measure performance
            process = psutil.Process(os.getpid())
            mem_before = process.memory_info().rss / (1024 * 1024)  # Convert to MB
            
            start_time = time.time()
            
            try:
                generator = SudokuGenerator(board_size)
                # Generate solution and measure time
                solution = generator.generate_solution()
                generation_times.append(generator.generation_time)
                
                # Generate puzzle and measure time
                puzzle = generator.generate_puzzle(num_clues=num_clues, symmetric=symmetric)
                removal_times.append(generator.removal_time)
                
                # Track total time
                total_times.append(time.time() - start_time)
                
                # Measure memory usage
                mem_after = process.memory_info().rss / (1024 * 1024)  # Convert to MB
                memory_usages.append(mem_after - mem_before)
                
                # Check if puzzle has a unique solution
                if puzzle.count_solutions() == 1:
                    success_count += 1
            except Exception:
                # Count as a failure
                pass
        
        # Calculate statistics
        if generation_times:
            avg_generation = statistics.mean(generation_times)
            avg_removal = statistics.mean(removal_times)
            avg_total = statistics.mean(total_times)
            min_total = min(total_times)
            max_total = max(total_times)
            avg_memory = statistics.mean(memory_usages) if memory_usages else 0
        else:
            avg_generation = avg_removal = avg_total = min_total = max_total = avg_memory = 0
        
        success_rate = (success_count / num_runs) * 100 if num_runs > 0 else 0
        
        # Store and return results
        result = {
            'board_size': board_size,
            'num_clues': num_clues,
            'symmetric': symmetric,
            'num_runs': num_runs,
            'avg_generation_time_sec': avg_generation,
            'avg_removal_time_sec': avg_removal,
            'avg_total_time_sec': avg_total,
            'min_total_time_sec': min_total,
            'max_total_time_sec': max_total,
            'avg_memory_mb': avg_memory,
            'success_rate': success_rate
        }
        
        self.results['generator'] = result
        return result
    
    def run_comprehensive_benchmark(self):
        """
        Run a comprehensive benchmark across different board sizes and difficulties.
        
        Returns:
            dict: Comprehensive benchmark results
        """
        results = {'solver': {}, 'generator': {}}
        
        # Test different board sizes
        for board_size in [4, 9]:
            # Benchmark solver at different difficulties
            for difficulty in ['easy', 'medium', 'hard']:
                key = f'size_{board_size}_{difficulty}'
                results['solver'][key] = self.benchmark_solver(
                    board_size=board_size, 
                    num_runs=3, 
                    difficulty=difficulty
                )
            
            # Benchmark generator with different clue counts
            # Use more reasonable clue counts that ensure uniqueness
            if board_size == 4:
                # 4x4 puzzles need at least 4-5 clues for uniqueness
                clue_counts = [6, 8, 10]
            else:  # size 9
                # 9x9 puzzles need at least 17 clues for uniqueness
                clue_counts = [20, 25, 30]
                
            for num_clues in clue_counts:
                key = f'size_{board_size}_clues_{num_clues}'
                results['generator'][key] = self.benchmark_generator(
                    board_size=board_size,
                    num_runs=3,
                    num_clues=num_clues
                )
        
        self.results['comprehensive'] = results
        return results
    
    def print_results(self):
        """Print benchmark results in a formatted way."""
        print("\n===== SUDOKU BENCHMARK RESULTS =====\n")
        
        # Print solver results
        if 'solver' in self.results:
            solver = self.results['solver']
            print(f"SOLVER BENCHMARK (Size: {solver['board_size']}x{solver['board_size']}, " 
                 f"Difficulty: {solver['difficulty']})")
            print(f"- Clues: {solver['num_clues']}")
            print(f"- Avg time: {solver['avg_time_sec']:.6f} seconds")
            print(f"- Min/Max time: {solver['min_time_sec']:.6f}/{solver['max_time_sec']:.6f} seconds")
            print(f"- Avg iterations: {solver['avg_iterations']:.1f}")
            print(f"- Avg memory usage: {solver.get('avg_memory_mb', 0):.2f} MB")
            print(f"- Success rate: {solver['success_rate']:.1f}%\n")
        
        # Print generator results
        if 'generator' in self.results:
            gen = self.results['generator']
            print(f"GENERATOR BENCHMARK (Size: {gen['board_size']}x{gen['board_size']})")
            print(f"- Target clues: {gen['num_clues']}")
            print(f"- Symmetric: {'Yes' if gen.get('symmetric', False) else 'No'}")
            print(f"- Avg solution generation time: {gen['avg_generation_time_sec']:.6f} seconds")
            print(f"- Avg clue removal time: {gen['avg_removal_time_sec']:.6f} seconds")
            print(f"- Avg total time: {gen['avg_total_time_sec']:.6f} seconds")
            print(f"- Min/Max total time: {gen['min_total_time_sec']:.6f}/{gen['max_total_time_sec']:.6f} seconds")
            print(f"- Avg memory usage: {gen.get('avg_memory_mb', 0):.2f} MB")
            print(f"- Success rate: {gen['success_rate']:.1f}%\n")
        
        # Print comprehensive results
        if 'comprehensive' in self.results:
            print("COMPREHENSIVE BENCHMARK SUMMARY:")
            comp = self.results['comprehensive']
            
            print("\nSolver Performance:")
            for key, data in comp['solver'].items():
                print(f"- {key}: {data['avg_time_sec']:.6f} seconds, "
                     f"{data['success_rate']:.1f}% success rate")
            
            print("\nGenerator Performance:")
            for key, data in comp['generator'].items():
                print(f"- {key}: {data['avg_total_time_sec']:.6f} seconds, "
                     f"{data['success_rate']:.1f}% success rate")