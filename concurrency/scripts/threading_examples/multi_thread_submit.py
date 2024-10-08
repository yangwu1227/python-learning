from concurrent.futures import ThreadPoolExecutor
from time import perf_counter, sleep


def task(id):
    print(f"Starting task {id}")
    # Simulate wait
    sleep(1)
    return f"Finished task {id}"


# Protect entry point of the program
if __name__ == "__main__":
    start = perf_counter()

    # Context manager
    with ThreadPoolExecutor() as executor:
        future_instance1 = executor.submit(task, 0)
        future_instance2 = executor.submit(task, 1)
        future_instance3 = executor.submit(task, 2)
        future_instance4 = executor.submit(task, 3)

        print(future_instance1.result())
        print(future_instance2.result())
        print(future_instance3.result())
        print(future_instance4.result())

    finish = perf_counter()

    print(f"It took {finish-start} second(s) to finish.")
