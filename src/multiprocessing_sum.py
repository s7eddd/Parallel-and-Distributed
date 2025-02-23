import time
import multiprocessing

def partial_sum(start, end, queue):
    queue.put(sum(range(start, end + 1)))

def multiprocessing_sum(n, num_processes):
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

if __name__ == "__main__":
    N = 10**7
    NUM_PROCESSES = 4
    process_sum, process_time = multiprocessing_sum(N, NUM_PROCESSES)
    print(f"Multiprocessing: Sum = {process_sum}, Time = {process_time:.6f} sec")
