import threading
from concurrent.futures import ThreadPoolExecutor

# A mock task


def task(name):
    pass


# Create a thread pool with a custom name prefix
executor = ThreadPoolExecutor(thread_name_prefix='TasksPool')
# Execute tasks
executor.map(task, range(10))
# Report all thread names
for thread in threading.enumerate():
    print(thread.name)
# Shutdown the thread pool
executor.shutdown()
