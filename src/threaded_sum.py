import time
import threading

def partial_sum(start, end, result, index):
    result[index] = sum(range(start, end + 1))

def threaded_sum(n, num_threads):
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

if __name__ == "__main__":
    N = 10**7
    NUM_THREADS = 4
    thread_sum, thread_time = threaded_sum(N, NUM_THREADS)
    print(f"Threading: Sum = {thread_sum}, Time = {thread_time:.6f} sec")
