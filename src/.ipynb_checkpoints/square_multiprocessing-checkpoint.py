import time
import math
import numpy as np
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

# Heavy function to justify multiprocessing
def heavy_function(x):
    return x**2 + math.sin(x) * math.log(x + 1)

def heavy_function_batch(numbers):
    return [heavy_function(x) for x in numbers]

def run_square_multiprocessing():
    N = 10**7
    numbers = np.random.randint(1, 100, N)
    print(f"\nProcessing {N} numbers")

    # 1. Sequential
    start = time.time()
    result_seq = [heavy_function(x) for x in numbers]
    end = time.time()
    print("Sequential time:", end - start)

    # 2. Multiprocessing.Process (individual processes — use small subset)
    numbers_subset = numbers[:100]  # Don't overload system
    manager = mp.Manager()
    result_mp = manager.list()

    def compute_and_store(x):
        result_mp.append(heavy_function(x))

    start = time.time()
    processes = []
    for x in numbers_subset:
        p = mp.Process(target=compute_and_store, args=(x,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    end = time.time()
    print("Multiprocessing individual processes time:", end - start)

    # 3. Pool.map
    start = time.time()
    with mp.Pool() as pool:
        result_pool_map = pool.map(heavy_function, numbers)
    end = time.time()
    print("Multiprocessing pool map time:", end - start)

    # 4. Pool.apply
    start = time.time()
    with mp.Pool() as pool:
        result_pool_apply = [pool.apply(heavy_function, args=(x,)) for x in numbers[:1000]]
    end = time.time()
    print("Multiprocessing pool apply time:", end - start)

    # 5. ProcessPoolExecutor
    start = time.time()
    with ProcessPoolExecutor() as executor:
        result_executor = list(executor.map(heavy_function, numbers))
    end = time.time()
    print("ProcessPoolExecutor time:", end - start)

    # 6. Pool.apply_async
    start = time.time()
    with mp.Pool() as pool:
        async_results = [pool.apply_async(heavy_function, args=(x,)) for x in numbers[:1000]]
        result_async = [r.get() for r in async_results]
    end = time.time()
    print("Async pool map time:", end - start)

if __name__ == "__main__":
    run_square_multiprocessing()
