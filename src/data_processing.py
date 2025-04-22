import time
from src.synchronization import *

def process_temperatures():
    """Computes moving averages from sensor readings."""
    sensor_data = {i: [] for i in range(3)}

    while True:
        if not temperature_queue.empty():
            with lock:
                sensor_id, temp = temperature_queue.get()
                sensor_data[sensor_id].append(temp)

                # Keep last 10 readings for averaging
                if len(sensor_data[sensor_id]) > 10:
                    sensor_data[sensor_id].pop(0)

                avg_temp = sum(sensor_data[sensor_id]) / len(sensor_data[sensor_id])
                temperature_averages[sensor_id] = round(avg_temp, 2)

            with condition:
                condition.notify()  # Notify display to update

        time.sleep(1)
