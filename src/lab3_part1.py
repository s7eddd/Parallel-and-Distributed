import time
import threading
import multiprocessing

def sequential_sum(n):
    start_time = time.time()
    total = sum(range(1, n+1))
    end_time = time.time()
    return total, end_time - start_time

def threaded_sum(n, num_threads):
    def partial_sum(start, end, result, index):
        result[index] = sum(range(start, end + 1))
    
    step = n // num_threads
    threads = []
    results = [0] * num_threads
    
    start_time = time.time()
    for i in range(num_threads):
        start = i * step + 1
        end = (i + 1) * step if i != num_threads - 1 else n
        thread = threading.Thread(target=partial_sum, args=(start, end, results, i))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    total = sum(results)
    end_time = time.time()
    return total, end_time - start_time

def multiprocessing_sum(n, num_processes):
    def partial_sum(start, end, queue):
        queue.put(sum(range(start, end + 1)))
    
    step = n // num_processes
    processes = []
    queue = multiprocessing.Queue()
    
    start_time = time.time()
    for i in range(num_processes):
        start = i * step + 1
        end = (i + 1) * step if i != num_processes - 1 else n
        process = multiprocessing.Process(target=partial_sum, args=(start, end, queue))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    total = sum(queue.get() for _ in range(num_processes))
    end_time = time.time()
    return total, end_time - start_time

def compute_metrics(seq_time, thread_time, process_time, num_threads, num_processes):
    speedup_threads = seq_time / thread_time
    speedup_processes = seq_time / process_time
    efficiency_threads = speedup_threads / num_threads
    efficiency_processes = speedup_processes / num_processes
    
    # Amdahl's Law
    p = 0.9  # Assuming 90% of the task is parallelizable
    amdahl_threads = 1 / ((1 - p) + (p / num_threads))
    amdahl_processes = 1 / ((1 - p) + (p / num_processes))
    
    # Gustafson's Law
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

if __name__ == "__main__":
    N = 10**7  # Large number for testing
    NUM_THREADS = 4
    NUM_PROCESSES = 4
    
    seq_sum, seq_time = sequential_sum(N)
    print(f"Sequential: Sum = {seq_sum}, Time = {seq_time:.6f} sec")
    
    thread_sum, thread_time = threaded_sum(N, NUM_THREADS)
    print(f"Threading: Sum = {thread_sum}, Time = {thread_time:.6f} sec")
    
    process_sum, process_time = multiprocessing_sum(N, NUM_PROCESSES)
    print(f"Multiprocessing: Sum = {process_sum}, Time = {process_time:.6f} sec")
    
    metrics = compute_metrics(seq_time, thread_time, process_time, NUM_THREADS, NUM_PROCESSES)
    for key, value in metrics.items():
        print(f"{key}: {value:.6f}")
