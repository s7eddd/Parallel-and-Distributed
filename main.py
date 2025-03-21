from src.connection_pool import run_connection_pool
from src.square_multiprocessing import run_square_multiprocessing

if __name__ == "__main__":
    print("\n=== Running Connection Pool Test ===")
    run_connection_pool()
    
    print("\n=== Running Multiprocessing Square Test ===")
    run_square_multiprocessing()
