import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from sequential_sum import sequential_sum
from threaded_sum import threaded_sum
from multiprocessing_sum import multiprocessing_sum
from compute_metrics import compute_metrics

if __name__ == "__main__":
    N = 10**7
    NUM_THREADS = 4
    NUM_PROCESSES = 4
    
    seq_sum, seq_time = sequential_sum(N)
    thread_sum, thread_time = threaded_sum(N, NUM_THREADS)
    process_sum, process_time = multiprocessing_sum(N, NUM_PROCESSES)
    
    print(f"Sequential: Sum = {seq_sum}, Time = {seq_time:.6f} sec")
    print(f"Threading: Sum = {thread_sum}, Time = {thread_time:.6f} sec")
    print(f"Multiprocessing: Sum = {process_sum}, Time = {process_time:.6f} sec")
    
    metrics = compute_metrics(seq_time, thread_time, process_time, NUM_THREADS, NUM_PROCESSES)
    for key, value in metrics.items():
        print(f"{key}: {value:.6f}")
