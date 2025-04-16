## Running Instructions

- Single Explorer (Original):
  Run with:
  python main.py --type static --auto

- Run Four Explorers in Parallel (Multiprocessing):
  Run with:
  python main.py --multi 4 --type static
  Note: For standard execution, import using: from src.explorer import Explorer
        For the improved version, import using: from src.explorer_improved import Explorer

- Run with MPI (3 Workers):
  Run with:
  mpirun -n 3 env PYTHONPATH=. python src/mpi_runner.py


## Files

- explorer.py: Contains the standard right-hand rule logic.
- explorer_improved.py: Contains an improved version using BFS.
- multi_runner.py: Implements the multiprocessing logic.
- mpi_runner.py: Implements the MPI-based approach.
- maze_explorer_comparison.ipynb: Notebook with visual bar charts for performance comparison.


## Questions

Question 1:
The automated maze explorer is built on the classic right-hand rule algorithm. In this approach, the explorer always attempts to turn right first. If there is a wall to the right, it moves straight; if that option is blocked, it turns left. This strategy helps the explorer follow the maze boundaries until the exit is found.
To prevent getting stuck in loops, the explorer records its last three positions. If these three positions are the same, it concludes that it is looping. It then starts a backtracking process by moving back through its recorded positions until it reaches a decision point where multiple paths were available. After backtracking, it resumes exploration from that point. When visualization is enabled, the explorer’s path is shown in real time, with every step, turn, and backtrack displayed. Without visualization, the logic still applies behind the scenes and runs faster since no drawing is done.
Once the goal is reached, the explorer prints several performance statistics: total time taken, number of moves made, count of backtracks, and the average moves per second. These metrics help assess the efficiency of the explorer's decisions and route.


Question 2:
We used Python's multiprocessing module to run four explorers at the same time using the --multi option. For a more advanced setup, we also used mpi4py to run explorers on separate processes via MPI, as seen in mpi_runner.py.
Each explorer runs independently and reports its own statistics, which are then printed and compared to determine the fastest explorer.

Output for multiprocessing:
 Results Summary:
Explorer 0 → Time: 0.001318s, Moves: 1279, Backtracks: 0
Explorer 1 → Time: 0.002018s, Moves: 1279, Backtracks: 0
Explorer 2 → Time: 0.001272s, Moves: 1279, Backtracks: 0
Explorer 3 → Time: 0.001260s, Moves: 1279, Backtracks: 0

 Best Explorer: 3 → 0.001260s

Output for MPI:
 Results Summary:
Explorer 1 → Time: 0.000307s, Moves: 246, Backtracks: 0
Explorer 2 → Time: 0.000349s, Moves: 246, Backtracks: 0

 Best Explorer: 1 → 0.000307s


Question 3:
Results Summary from testing four maze explorers on a static maze:
 Explorer 0 → Time: 0.001318s, Moves: 1279, Backtracks: 0
 Explorer 1 → Time: 0.002018s, Moves: 1279, Backtracks: 0
 Explorer 2 → Time: 0.001272s, Moves: 1279, Backtracks: 0
 Explorer 3 → Time: 0.001260s, Moves: 1279, Backtracks: 0

The fastest explorer was Explorer 3 with a completion time of 0.001260 seconds.

All explorers followed the same path, making exactly 1279 moves with no backtracking. This indicates that the maze has a single clear solution and that the algorithm is deterministic—it always follows the same route given the same maze. The slight differences in time are likely due to how the parallel processes were scheduled by the system.


Question 4:
Note: The improved explorer is in a separate file (explorer_improved.py) to preserve the original version and allow for easy comparison.

The original explorer uses the right-hand rule, meaning it always tries to turn right first, then moves straight, and finally turns left if necessary. Although this method ensures that an exit will eventually be found, it has some drawbacks. It does not consider the exit's location, which can result in long, winding paths or loops. In our test, the explorer made over 1200 moves, even though a much shorter route was possible. This is because the algorithm follows the wall without considering a more direct path.
To address these issues, two major improvements were made:

1. Breadth-First Search (BFS) Algorithm  
   The right-hand rule was replaced with BFS, which always finds the shortest path from the start to the goal. BFS explores the maze layer by layer, constructing the path to the exit as soon as it is found. This change reduced the move count to just 128 moves, a major improvement.

2. Visited Tracking System  
   A visited set was added to track cells that have already been checked. This prevents the explorer from re-evaluating the same paths, saving time and improving efficiency. Together, the BFS approach and visited tracking guarantee a short, loop-free path.

Although the BFS-based explorer runs slightly slower because it checks more possible paths and uses extra memory, it delivers a far more efficient solution by minimizing unnecessary moves.

Results Summary:
 Explorer 0 → Time: 0.002269s, Moves: 128, Backtracks: 0
 Explorer 1 → Time: 0.002033s, Moves: 128, Backtracks: 0
 Explorer 2 → Time: 0.002047s, Moves: 128, Backtracks: 0
 Explorer 3 → Time: 0.002131s, Moves: 128, Backtracks: 0

 Best Explorer: 1 → 0.002033s


Question 5:
The notebook file maze_explorer_comparison.ipynb includes bar charts that visually compare the time taken and the number of moves for each explorer version. These charts clearly show that the improved explorer is much more efficient in terms of the path taken.

When comparing the two versions, the original explorer took around 1279 moves along a long and indirect route. The improved version solved the maze in just 128 moves, demonstrating a significant increase in efficiency. However, this improvement comes with some trade-offs. The BFS-based explorer uses more time to check multiple paths and more memory to store visited cells, and its logic is more complex, which can make it harder to modify or understand at first. Despite these factors, the improved version is more reliable and effective, especially for larger or more complex mazes.


Question 6 (10 points):
Answer: Achieve the best result of 128 moves

The improved explorer demonstrates the best performance by solving the maze using only 128 moves. This result shows that the optimized BFS approach, along with the visited tracking system, effectively minimizes unnecessary moves and finds the shortest path to the exit.
