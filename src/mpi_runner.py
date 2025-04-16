from mpi4py import MPI
from src.explorer import Explorer
from src.maze import create_maze, Maze

def run_explorer_instance(grid, start_pos, end_pos):
    maze = Maze(len(grid[0]), len(grid))
    maze.grid = grid
    maze.start_pos = start_pos
    maze.end_pos = end_pos
    explorer = Explorer(maze, visualize=False)
    time_taken, moves = explorer.solve()
    return {
        'time_taken': time_taken,
        'moves': len(moves),
        'backtracks': explorer.backtrack_count
    }

def run_mpi_explorers():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        # Master process
        print(f" Running {size - 1} explorers with MPI...")
        maze = create_maze(30, 30, "random")
        grid = maze.grid
        start = maze.start_pos
        end = maze.end_pos

        for i in range(1, size):
            comm.send((grid, start, end), dest=i)

        results = []
        for i in range(1, size):
            result = comm.recv(source=i)
            results.append((i, result))

        print("\n Results Summary:")
        for i, res in results:
            print(f"Explorer {i} → Time: {res['time_taken']:.6f}s, "
                  f"Moves: {res['moves']}, Backtracks: {res['backtracks']}")

        best = min(results, key=lambda r: r[1]['time_taken'])
        print(f"\n Best Explorer: {best[0]} → {best[1]['time_taken']:.6f}s")

    else:
        # Worker process
        print(f"Worker {rank} is alive and waiting...")
        grid, start, end = comm.recv(source=0)
        print(f"Worker {rank} received maze data.")
        result = run_explorer_instance(grid, start, end)
        comm.send(result, dest=0)


if __name__ == "__main__":
    run_mpi_explorers()
