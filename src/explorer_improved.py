import time
import pygame
from typing import Tuple, List, Optional, Deque
from collections import deque
from .constants import BLUE, WHITE, CELL_SIZE, WINDOW_SIZE
import random

class Explorer:
    def __init__(self, maze, visualize: bool = False):
        # Initialize explorer with maze info and options for visualization
        self.maze = maze
        self.x, self.y = maze.start_pos  # Set starting position
        self.direction = (1, 0)  # Default direction: facing right
        self.moves = []  # Track all the visited coordinates
        self.start_time = None  # To store start time of exploration
        self.end_time = None  # To store end time of exploration
        self.visualize = visualize  # Enable or disable GUI display
        self.move_history = deque(maxlen=3)  # (kept from original logic)
        self.backtracking = False  # Not used in BFS, but retained for compatibility
        self.backtrack_path = []
        self.backtrack_count = 0
        self.visited = set()  # Track visited cells to avoid revisiting

        # Initialize pygame screen if visualization is enabled
        if visualize:
            pygame.init()
            self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            pygame.display.set_caption("Maze Explorer - Improved Solving")
            self.clock = pygame.time.Clock()

    def turn_right(self):
        # Rotate the explorer direction 90 degrees clockwise
        x, y = self.direction
        self.direction = (-y, x)

    def turn_left(self):
        # Rotate the explorer direction 90 degrees counter-clockwise
        x, y = self.direction
        self.direction = (y, -x)

    def can_move(self, dx, dy) -> bool:
        # Check if the next position (dx, dy) is valid and unvisited
        new_x, new_y = self.x + dx, self.y + dy
        return (0 <= new_x < self.maze.width and 
                0 <= new_y < self.maze.height and 
                self.maze.grid[new_y][new_x] == 0 and
                (new_x, new_y) not in self.visited)

    def move_to(self, dx, dy):
        # Move explorer to the new position (x+dx, y+dy)
        self.x += dx
        self.y += dy
        current_move = (self.x, self.y)
        self.moves.append(current_move)  # Save the move
        self.move_history.append(current_move)
        self.visited.add(current_move)  # Mark as visited
        if self.visualize:
            self.draw_state()  # Update GUI if enabled

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        # Find all walkable, unvisited neighbor cells of a given position
        x, y = pos
        neighbors = []
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:  # Right, Left, Down, Up
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.maze.width and 0 <= ny < self.maze.height and 
                self.maze.grid[ny][nx] == 0 and (nx, ny) not in self.visited):
                neighbors.append((nx, ny))
        random.shuffle(neighbors)  # Shuffle for slight randomness in direction
        return neighbors

    def bfs_solve(self):
        # Use Breadth-First Search to find shortest path from start to end
        queue = deque()
        came_from = {}  # To reconstruct the shortest path
        start = (self.x, self.y)
        queue.append(start)
        came_from[start] = None

        # Loop until the queue is empty or goal is found
        while queue:
            current = queue.popleft()
            if current == self.maze.end_pos:
                break  # Goal reached

            # Explore valid neighbors
            for neighbor in self.get_neighbors(current):
                if neighbor not in came_from:  # Only visit each node once
                    queue.append(neighbor)
                    came_from[neighbor] = current  # Track how we reached this node

        # Reconstruct path from goal to start
        path = []
        current = self.maze.end_pos
        while current and current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()  # Reverse to get path from start to goal

        return path

    def draw_state(self):
        # GUI function to draw maze and explorer position using pygame
        self.screen.fill(WHITE)  # Clear screen

        # Draw maze walls
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if self.maze.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0),
                                     (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw start point in green
        pygame.draw.rect(self.screen, (0, 255, 0),
                         (self.maze.start_pos[0] * CELL_SIZE,
                          self.maze.start_pos[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))

        # Draw end point in red
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.maze.end_pos[0] * CELL_SIZE,
                          self.maze.end_pos[1] * CELL_SIZE,
                          CELL_SIZE, CELL_SIZE))

        # Draw current explorer position in blue
        pygame.draw.rect(self.screen, BLUE,
                         (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()
        self.clock.tick(30)  # Control frame rate

    def print_statistics(self, time_taken: float):
        # Print runtime stats for the explorer
        print("\n=== Maze Exploration Statistics ===")
        print(f"Total time taken: {time_taken:.6f} seconds")
        print(f"Total moves made: {len(self.moves)}")
        print(f"Number of backtrack operations: {self.backtrack_count}")  # stays 0 in BFS
        print(f"Average moves per second: {len(self.moves)/time_taken:.2f}")
        print("==================================\n")

    def solve(self) -> Tuple[float, List[Tuple[int, int]]]:
        # Solve the maze using BFS and return total time and path
        self.start_time = time.perf_counter()  # Start timer
        path = self.bfs_solve()  # Get shortest path using BFS

        # Move through path one step at a time
        for pos in path:
            dx = pos[0] - self.x
            dy = pos[1] - self.y
            self.move_to(dx, dy)

        self.end_time = time.perf_counter()  # End timer
        time_taken = self.end_time - self.start_time

        if self.visualize:
            pygame.time.wait(2000)  # Pause to show final state
            pygame.quit()  # Close window

        self.print_statistics(time_taken)  # Output results
        return time_taken, self.moves
