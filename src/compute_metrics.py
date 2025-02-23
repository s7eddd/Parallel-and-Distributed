def compute_metrics(seq_time, thread_time, process_time, num_threads, num_processes):
    speedup_threads = seq_time / thread_time
    speedup_processes = seq_time / process_time
    efficiency_threads = speedup_threads / num_threads
    efficiency_processes = speedup_processes / num_processes
    
    p = 0.9  # Assuming 90% of the task is parallelizable
    amdahl_threads = 1 / ((1 - p) + (p / num_threads))
    amdahl_processes = 1 / ((1 - p) + (p / num_processes))
    gustafson_threads = (1 - p) + (p * num_threads)
    gustafson_processes = (1 - p) + (p * num_processes)
    
    return {
        'Speedup (Threads)': speedup_threads,
        'Speedup (Processes)': speedup_processes,
        'Efficiency (Threads)': efficiency_threads,
        'Efficiency (Processes)': efficiency_processes,
        "Amdahl's Speedup (Threads)": amdahl_threads,
        "Amdahl's Speedup (Processes)": amdahl_processes,
        "Gustafson's Speedup (Threads)": gustafson_threads,
        "Gustafson's Speedup (Processes)": gustafson_processes
    }
