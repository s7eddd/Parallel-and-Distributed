import multiprocessing as mp
import time
import random

class ConnectionPool:
    def __init__(self, size):
        self.connections = [f"Connection-{i}" for i in range(size)]
        self.semaphore = mp.Semaphore(size)
        self.lock = mp.Lock()  # For safe printing/logging

    def get_connection(self):
        self.semaphore.acquire()
        conn = self.connections.pop()
        return conn

    def release_connection(self, conn):
        self.connections.append(conn)
        self.semaphore.release()


def access_database(pool, proc_id):
    with pool.lock:
        print(f"Process {proc_id}: Waiting for connection...")
    conn = pool.get_connection()
    with pool.lock:
        print(f"Process {proc_id}: Acquired {conn}")
    time.sleep(random.uniform(0.5, 2))  # Simulate DB work
    pool.release_connection(conn)
    with pool.lock:
        print(f"Process {proc_id}: Released {conn}")


def main():
    num_connections = 3
    num_processes = 10
    
    pool = ConnectionPool(num_connections)
    
    processes = []
    for i in range(num_processes):
        p = mp.Process(target=access_database, args=(pool, i))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()


if __name__ == '__main__':
    main()
