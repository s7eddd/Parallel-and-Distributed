import time
import random
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

# Function to compute square
def square(x):
    return x * x

# Generate list of numbers
N = 10**6  # Change to 10**7 for the extended test
numbers = [random.randint(1, 100) for _ in range(N)]

print("--- Testing with", N, "numbers ---")

# 1. Sequential for loop
start = time.time()
result_seq = [square(x) for x in numbers]
end = time.time()
print("Sequential:", round(end - start, 4), "seconds")

# 2. multiprocessing.Process for each number (not recommended in real scenarios)
def run_process(numbers):
    result = mp.Manager().list()
    processes = []
    start = time.time()
    for num in numbers:
        p = mp.Process(target=lambda x: result.append(square(x)), args=(num,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    end = time.time()
    print("multiprocessing.Process per number:", round(end - start, 4), "seconds")

# run_process(numbers[:100])  # ONLY run with very small subset to avoid system crash

# 3. multiprocessing.Pool with map
start = time.time()
with mp.Pool() as pool:
    result_pool_map = pool.map(square, numbers)
end = time.time()
print("Pool.map:", round(end - start, 4), "seconds")

# 4. multiprocessing.Pool with apply (sync)
start = time.time()
with mp.Pool() as pool:
    result_pool_apply = [pool.apply(square, args=(num,)) for num in numbers[:1000]]  # limit size
end = time.time()
print("Pool.apply (sync, 1K samples):", round(end - start, 4), "seconds")

# 5. multiprocessing.Pool with apply_async (async)
start = time.time()
with mp.Pool() as pool:
    result_pool_async = [pool.apply_async(square, args=(num,)) for num in numbers[:1000]]  # limit size
    result_pool_async = [r.get() for r in result_pool_async]
end = time.time()
print("Pool.apply_async (async, 1K samples):", round(end - start, 4), "seconds")

# 6. concurrent.futures.ProcessPoolExecutor
start = time.time()
with ProcessPoolExecutor() as executor:
    result_concurrent = list(executor.map(square, numbers))
end = time.time()
print("ProcessPoolExecutor:", round(end - start, 4), "seconds")
