import os
import time
from src.synchronization import *

def initialize_display():
    """Prints the initial display layout with placeholders."""
    os.system("cls" if os.name == "nt" else "clear")
    print("Current temperatures:")
    print("Latest Temperatures:", end=" ")
    for i in range(3):
        print(f"Sensor {i}: --°C", end="  ")
    print("\n")
    for i in range(3):
        print(f"Sensor {i} Average:   --°C")

def update_display():
    """Updates the display every 5 seconds, synchronized with new data."""
    while True:
        with condition:
            condition.wait()  # Wait for new data
            os.system("cls" if os.name == "nt" else "clear")
            print("Current temperatures:")

            # Display latest temperatures
            print("Latest Temperatures:", end=" ")
            for i in range(3):
                temp = latest_temperatures.get(i, "--")
                print(f"Sensor {i}: {temp}°C", end="  ")
            print("\n")

            # Display temperature averages
            for i in range(3):
                avg_temp = temperature_averages.get(i, "--")
                print(f"Sensor {i} Average:   {avg_temp}°C")

        time.sleep(5)  # Refresh display every 5 seconds
