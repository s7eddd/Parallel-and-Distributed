import time

def sequential_sum(n):
    start_time = time.time()
    total = sum(range(1, n+1))
    end_time = time.time()
    return total, end_time - start_time

if __name__ == "__main__":
    N = 10**7
    seq_sum, seq_time = sequential_sum(N)
    print(f"Sequential: Sum = {seq_sum}, Time = {seq_time:.6f} sec")
