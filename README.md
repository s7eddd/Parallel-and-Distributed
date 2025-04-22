# Description lab 4 part1

1️⃣ Which synchronization metric did you use for each of the tasks?
We used thread synchronization mechanisms rather than traditional performance "metrics" like execution time or CPU usage. The mechanisms we implemented are:

Task	Synchronization Metric Used
3.a - Sensor Simulation	RLock (Reentrant Lock) to ensure thread-safe updates to latest_temperatures and temperature_queue.
3.b - Data Processing	RLock to prevent race conditions when computing temperature averages.
3.c - Threading	daemon=True for automatic thread cleanup, ensuring that threads stop when main.py exits.
3.d - Display Logic	Condition (with RLock) to ensure the display updates only when new data is available.
3.e - Synchronization	Combination of RLock and Condition to ensure safe access to shared data structures.
Why These?
RLock ensures that multiple threads can safely access shared data without conflicts.
Condition allows the display to update only when new data is available, reducing unnecessary CPU usage.
Daemon Threads ensure proper cleanup when the program exits.
2️⃣ Why did the professor not ask you to compute metrics?
The professor likely avoided explicit performance metrics for the following reasons:

Focus on Synchronization, Not Performance

The main goal of this project is to practice safe multithreading and shared resource management, not measure execution speed.
Non-Deterministic Thread Execution

Threads execute independently, and exact execution times vary based on system load, making metrics like runtime difficult to interpret.
Simple Simulation (Low CPU Usage)

Since the tasks involve basic sensor simulation and averaging, performance optimization isn’t critical.
Blocking Synchronization Reduces CPU Waste

The use of Condition.wait() means threads only run when needed, rather than consuming CPU constantly.
Real-World Metrics Would Require More Complex Scenarios

In actual applications, we would measure latency, throughput, and response time, which are unnecessary for this exercise.
✨ Summary
We used RLock and Condition for thread synchronization.
The professor likely skipped metrics to emphasize correct threading logic, not performance tuning.
