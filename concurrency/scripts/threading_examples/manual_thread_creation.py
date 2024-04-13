from threading import Thread

# Custom function to be executed in a new thread


def task():
    print('This is another thread')


# Protect the entry point of the program
if __name__ == '__main__':
    # Define a task to run in a new thread
    thread = Thread(target=task)
    # Start the task in a new thread
    thread.start()
    # Wait for the thread to terminate
    thread.join()
