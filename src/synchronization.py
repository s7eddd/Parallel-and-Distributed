import threading
import queue

# Global Data Structures
latest_temperatures = {i: "--" for i in range(3)}
temperature_averages = {i: "--" for i in range(3)}
temperature_queue = queue.Queue()

# Thread Synchronization Tools
lock = threading.RLock()  # Ensures safe access to shared data
condition = threading.Condition(lock)  # Synchronizes display updates
