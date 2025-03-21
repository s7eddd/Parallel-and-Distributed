from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()  # Get the number of processes

if rank == 0:
    # Run sequential execution only on rank 0
    sequential_time = sequential()
    print(f"Sequential Execution Time: {sequential_time}")

# Synchronize before starting parallel execution
comm.Barrier()

# Run parallel execution on all ranks
parallel_time = genetic_algorithm_mpi()

# Ensure all ranks finish before proceeding
comm.Barrier()

# Compute performance metrics on rank 0
if rank == 0:
    # Speedup (S)
    speedup = sequential_time / parallel_time
    print(f"Speedup (S): {speedup:.2f}")

    # Efficiency (E)
    efficiency = speedup / size
    print(f"Efficiency (E): {efficiency:.2%}")

    # Amdahl's Law: S = 1 / ( (1 - P) + P / N )
    P = 0.9  # Assumption: 90% of execution is parallelizable (adjust based on profiling)
    amdahl_speedup = 1 / ((1 - P) + (P / size))
    print(f"Amdahl’s Law Speedup: {amdahl_speedup:.2f}")

    # Gustafson’s Law: S = N - α(N - 1)
    alpha = 1 - P  # Sequential portion
    gustafson_speedup = size - alpha * (size - 1)
    print(f"Gustafson’s Law Speedup: {gustafson_speedup:.2f}")

    print(f"Parallel Execution Time: {parallel_time}")
