import threading
from src.sensor_simulation import *
from src.data_processing import *
from src.display_logic import *

def start_threads():
    """Creates and starts all required threads."""
    
    # Create sensor threads
    sensor_threads = [threading.Thread(target=simulate_sensor, args=(i,), daemon=True) for i in range(3)]

    # Create data processing thread
    processing_thread = threading.Thread(target=process_temperatures, daemon=True)

    # Create display update thread (refresh every 5s)
    display_thread = threading.Thread(target=update_display, daemon=True)

    # Start all threads
    for thread in sensor_threads:
        thread.start()

    processing_thread.start()
    display_thread.start()

    # Return thread objects (optional, for monitoring)
    return sensor_threads, processing_thread, display_thread
