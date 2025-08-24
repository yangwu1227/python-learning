from time import perf_counter, sleep


def task(id) -> str:
    print(f"Starting task {id}")
    # Simulate wait
    sleep(1)
    return f"Finished task {id}"


# Start the timer
start = perf_counter()

for i in range(4):
    print(task(i))

finish = perf_counter()

print(f"It took {finish - start} second(s) to finish.")
