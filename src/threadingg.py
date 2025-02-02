import threading
import time
import random
import string

# Function to join a thousand random letters
def join_random_letters():
    letters = [random.choice(string.ascii_letters) for _ in range(1000)]
    joined_letters = ''.join(letters)
    print("Joined Letters Task Done")

# Function to add a thousand random numbers
def add_random_numbers():
    numbers = [random.randint(1, 100) for _ in range(1000)]
    total_sum = sum(numbers)
    print("Add Numbers Task Done")

if __name__ == "__main__":
    total_start_time = time.time()

    # Create threads
    thread_letters = threading.Thread(target=join_random_letters)
    thread_numbers = threading.Thread(target=add_random_numbers)

    # Start the threads
    thread_letters.start()
    thread_numbers.start()

    # Wait for both threads to complete
    thread_letters.join()
    thread_numbers.join()

    total_end_time = time.time()
    print(f"Total time taken (threading): {total_end_time - total_start_time:.6f} seconds")
