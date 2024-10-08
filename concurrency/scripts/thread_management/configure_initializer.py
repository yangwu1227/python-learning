from concurrent.futures import ThreadPoolExecutor
from random import random
from threading import current_thread
from time import sleep

# Function for initializing the worker thread


def initializer_worker():
    # get the unique name for this thread
    name = current_thread().name
    # store the unique worker name in a thread local variable
    print(f"Initializing worker thread {name}")


# A mock task that sleeps for a random amount of time less than one second


def task(identifier):
    sleep(random())
    return identifier


# Create a thread pool
with ThreadPoolExecutor(max_workers=2, initializer=initializer_worker) as executor:
    # Execute Tasks
    for result in executor.map(task, range(10)):
        print(result)
