from src.explorer_improved import Explorer
from src.maze import Maze, create_maze
from multiprocessing import Pool
import time

# 🔹 Function to run one explorer instance on a given maze
def run_explorer_instance(grid, start_pos, end_pos, explorer_id):
    # Rebuild the maze object using the shared grid and start/end positions
    maze = Maze(len(grid[0]), len(grid))  # width = columns, height = rows
    maze.grid = grid
    maze.start_pos = start_pos
    maze.end_pos = end_pos

    # Create and run the explorer (no visualization)
    explorer = Explorer(maze, visualize=False)
    time_taken, moves = explorer.solve()

    # Return the results as a dictionary
    return {
        'explorer_id': explorer_id,
        'time_taken': time_taken,
        'moves': len(moves),
        'backtracks': explorer.backtrack_count
    }

# 🔹 Main function to run multiple explorers in parallel
def run_multiple_explorers(num_explorers, width=30, height=30, maze_type="random"):
    print(f" Running {num_explorers} explorers in parallel...")

    # Generate the maze once and share it with all explorers
    maze = create_maze(width, height, maze_type)
    grid = maze.grid                    # The maze structure (walls and paths)
    start = maze.start_pos             # Starting point of the maze
    end = maze.end_pos                 # Ending point of the maze

    # Prepare arguments for each explorer process
    args = [(grid, start, end, i) for i in range(num_explorers)]

    # Start multiprocessing: each explorer runs in a separate process
    with Pool(processes=num_explorers) as pool:
        results = pool.starmap(run_explorer_instance, args)

    # Print all explorer results
    print("\n Results Summary:")
    for res in results:
        print(f"Explorer {res['explorer_id']} → Time: {res['time_taken']:.6f}s, "
              f"Moves: {res['moves']}, Backtracks: {res['backtracks']}")

    # Identify and display the best explorer (based on shortest time)
    best = min(results, key=lambda r: r['time_taken'])
    print(f"\n Best Explorer: {best['explorer_id']} → {best['time_taken']:.6f}s")
    
if __name__ == "__main__":
    run_multiple_explorers(4)
