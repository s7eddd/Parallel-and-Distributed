import time
import threading
import multiprocessing
import random
import string

# Function to join a thousand random letters
def join_random_letters():
    letters = [random.choice(string.ascii_letters) for _ in range(1000)]
    joined_letters = ''.join(letters)

# Function to add a thousand random numbers
def add_random_numbers():
    numbers = [random.randint(1, 100) for _ in range(1000)]
    total_sum = sum(numbers)

# Performance analysis functions
def compute_performance(sequential_time, parallel_time, num_threads):
    speedup = sequential_time / parallel_time
    efficiency = speedup / num_threads
    print(f"Speedup: {speedup:.2f}")
    print(f"Efficiency: {efficiency:.2f}")

if __name__ == "__main__":
    ### 1️⃣ Sequential Execution ###
    start_time = time.time()
    join_random_letters()
    add_random_numbers()
    sequential_time = time.time() - start_time
    print(f"Sequential execution time: {sequential_time:.6f} seconds\n")

    ### 2️⃣ Threading Execution ###
    start_time = time.time()
    thread1 = threading.Thread(target=join_random_letters)
    thread2 = threading.Thread(target=add_random_numbers)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    thread_time = time.time() - start_time
    print(f"Threading execution time: {thread_time:.6f} seconds")

    compute_performance(sequential_time, thread_time, 2)
    print()

    ### 3️⃣ Multiprocessing Execution ###
    start_time = time.time()
    process1 = multiprocessing.Process(target=join_random_letters)
    process2 = multiprocessing.Process(target=add_random_numbers)
    process1.start()
    process2.start()
    process1.join()
    process2.join()
    process_time = time.time() - start_time
    print(f"Multiprocessing execution time: {process_time:.6f} seconds")

    compute_performance(sequential_time, process_time, 2)
