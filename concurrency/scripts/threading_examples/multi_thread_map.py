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
        results = executor.map(task, range(4))
        for result in results:
            print(result)

    finish = perf_counter()

    print(f"It took {finish-start} second(s) to finish.")
