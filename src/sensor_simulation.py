import threading
import random
import time
from src.synchronization import *

def simulate_sensor(sensor_id):
    """Simulates a temperature sensor that updates readings."""
    while True:
        temp = random.randint(15, 40)
        with lock:
            latest_temperatures[sensor_id] = temp
            temperature_queue.put((sensor_id, temp))
        
        with condition:
            condition.notify()  # Notify display to update
        
        time.sleep(1)  # Generate a new reading every second
