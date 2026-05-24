# Timing Function Execution
# Problem: Write a decorator that measures the time a function takes to execute.
import time
def timer(func):
    def wrapper(*args, **kwargs): # Define a wrapper function that takes any arguments
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Call the original function
        end_time = time.time()  # Record the end time
        print(f"Execution time: {end_time - start_time:.4f} seconds")  # Print the execution time
        return result  # Return the result of the original function
    return wrapper