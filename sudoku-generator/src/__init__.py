from generator import SudokuGenerator
from solver import SudokuSolver
import time

if __name__ == "__main__":
    generator = SudokuGenerator()
    solver = SudokuSolver()
    attempts = 0
    start_overall_time = time.time()
    board = generator.generate_puzzle(30)
    start_instace_time = time.time()
    while solver.solve(board):

        board = generator.generate_puzzle(30)
        attempts += 1
        end_instance_time = time.time()
        print(f"Time taken for instance {attempts}: {end_instance_time - start_instace_time:.2f} seconds")
        

        if attempts > 1000 or input("Do you want to continue? (y/n): ").lower() == "n":
            print(f"Failed to generate invalid puzzle at {attempts} attempts")
            end_overall_time = time.time()
            print(f"Time taken: {end_overall_time - start_overall_time:.2f} seconds")
            break
        elif input("Do you want to continue? (y/n): ").lower() == "y":
            print(f"Puzzle generation attempt {attempts} successful")
            end_overall_time = time.time()
            start_instace_time = time.time()
            print(f"Total time taken: {end_overall_time - start_overall_time:.2f} seconds")
        else:
            print("Invalid input. Try again.")
    print("Unsolvable puzzle generated")
    print(board)
    end_overall_time = time.time()
    print(f"Total time taken: {end_overall_time - start_overall_time:.2f} seconds") 
            