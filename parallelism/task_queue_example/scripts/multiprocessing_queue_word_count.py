import logging
import os
import time
from multiprocessing import Process, Queue, cpu_count, get_logger
from pathlib import Path
from queue import Empty
from typing import List

from utils import setup_logger
from word_count_task import count_words

num_processes = cpu_count() - 1
book_multipler = 10
project_path = Path(__file__).resolve().parents[1]
data_path = project_path / "data"


def setup_multiprocessing_logger(process_id: int) -> logging.Logger:
    """
    Set up a logger for the process with the given ID.

    Parameters
    ----------
    process_id : int
        The ID of the process.

    Returns
    -------
    logging.Logger
        A logger instance for the process.
    """
    logger = get_logger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(f"logs/process_{process_id}.log")
    logger.addHandler(file_handler)
    return logger


def process_tasks(task_queue: Queue) -> bool:
    """
    Process tasks from the queue until it is empty. Process means counting the words in a book,
    not including any stop words.

    Parameters
    ----------
    task_queue : Queue
        The queue to process tasks from.

    Returns
    -------
    bool
        True to indicate that all tasks have been processed.
    """
    process_id = os.getpid()
    logger = setup_multiprocessing_logger(process_id)
    logger.info(f"Process ID: {process_id} | Starting process_tasks")
    while True:
        try:
            book = task_queue.get(block=False)
            logger.info(f"Process ID: {process_id} | Dequeued {book}")
            count_words(book)
        except Empty:
            logger.info(f"Process ID: {process_id} | Queue is empty")
            break
        except Exception as error:
            # No break here, continue processing the rest of the queue
            logger.error(f"Process ID: {process_id} | Error processing book: {error}")
    return True


def enque(task_queue: Queue, books: List[str], logger: logging.Logger) -> Queue:
    """
    Enqueue books to the task queue, multiplying by the book multiplier.

    Parameters
    ----------
    task_queue : Queue
        The queue to enqueue tasks to.
    books : List[str]
        The list of books (filenames) to enqueue.
    logger : logging.Logger
        The logger instance for the main process.

    Returns
    -------
    Queue
        The task queue with the books enqueued.
    """

    # Enqueue (len(books) x book_multipler) books to the task queue
    for i in range(book_multipler):
        for book in books:
            # Block if necessary until a free slot is available, never raise a Full exception
            task_queue.put(obj=book, block=True, timeout=None)
            logger.info(f"Enqueued {book}")
    return task_queue


def main() -> int:
    # Logger for the main process
    logger = setup_logger("multiprocessing_queue_word_count")
    # Get all books
    books = list(path.name for path in data_path.rglob("*.txt"))
    # Infinite size queue
    task_queue: Queue = Queue()
    task_queue = enque(task_queue, books, logger)

    processes = []
    start_time = time.time()
    for _ in range(num_processes):
        process = Process(target=process_tasks, args=(task_queue,))
        # Add the process to the list of child processes
        processes.append(process)
        # Start the process
        process.start()
    # Main process will wait for all child processes to complete
    for process in processes:
        process.join()
    logger.info(f"Word count task completed in {time.time() - start_time:.2f} seconds")

    return 0


if __name__ == "__main__":
    main()
