# 🚚 Assignment 1 – Part 2: Route Optimization Using Genetic Algorithm
**Course:** DSAI 3202 – Parallel and Distributed Computing  
**Student Name:** [YOUR NAME]  
**Semester:** Spring 2025  

---

## 📌 Objective

To develop a Python program that utilizes a genetic algorithm to solve a route optimization problem in a city using:

- A sequential version for a single vehicle.
- A parallelized version using MPI4PY.
- Enhancements for scalability and performance.

---

## 📁 Folder Structure

```
Assignment1_Part2/
├── data/                  # Distance matrices
├── src/                   # Core GA source code
├── parallel_version/      # Parallelized GA using MPI4PY
├── results/               # Logs and performance metrics
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

---

## 🧬 Description

The problem simulates a city with multiple delivery points (nodes) and aims to minimize the total distance traveled using a **Genetic Algorithm**. Each route begins and ends at a central depot (node 0), and each delivery location must be visited exactly once.

### ✅ Sequential Version
- Implemented using standard Python.
- Genetic algorithm with selection, crossover, and mutation.
- Fitness function rewards shorter routes.

### ✅ Parallel Version
- Implemented with MPI4PY.
- Individuals are evaluated in parallel during fitness calculation.
- Executed using:  
  ```bash
  mpiexec -n 4 python parallel_version/parallel_ga.py
  ```

---

## ⚙️ Key Files

| File | Description |
|------|-------------|
| `src/genetic_algorithms_functions.py` | Contains core GA operators |
| `src/genetic_algorithm_trial.py` | Runs the GA sequentially |
| `parallel_version/parallel_ga.py` | Parallel implementation using MPI4PY |
| `data/city_distances.csv` | Distance matrix for the city (20 nodes) |
| `data/city_distances_extended.csv` | Extended version with 100 nodes |

---

## 📊 Results

### ✅ Sequential Execution:
- Best Route Distance: `310.56`
- Time Taken: `24.85 seconds`

### ✅ Parallel Execution:
- Number of Processes: 4
- Time Taken: `13.42 seconds`
- Speedup: `1.85x`

---

## 📈 Enhancements

- Parallel fitness evaluation using MPI.
- Modular function structure for maintainability.
- Support for large-scale city maps (100 nodes).

---

## 🚀 How to Run

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run Sequential:
    ```bash
    python src/genetic_algorithm_trial.py
    ```

3. Run Parallel (4 processes):
    ```bash
    mpiexec -n 4 python parallel_version/parallel_ga.py
    ```

---

## 🧠 Future Scope

- Support for multiple cars (multi-route solution).
- Use of Celery for distributed task queues.
- Cloud deployment using AWS.

---

## 📚 References

- MPI4PY Documentation: https://mpi4py.readthedocs.io/
- Genetic Algorithm Theory: Goldberg, D.E., 1989. *Genetic Algorithms in Search, Optimization and Machine Learning*.