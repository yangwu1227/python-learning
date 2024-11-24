from multiprocessing import Queue
from pathlib import Path
from queue import Empty

from utils import setup_logger

logger = setup_logger("multiprocessing_queue")
project_path = Path(__file__).resolve().parents[1]
data_path = project_path / "data"


def main() -> int:
    books = list(path.name for path in data_path.rglob("*.txt"))
    # Infinite size queue
    queue: Queue = Queue(maxsize=-1)

    logger.info(f"Enqueuing {len(books)} books")
    for book in books:
        # Block if necessary until a free slot is available (i.e., never raise a Full exception queue.Full exception)
        queue.put(obj=book, block=True, timeout=None)
        logger.info(f"Enqueued {book}")

    logger.info(f"Dequeuing {len(books)} books")
    while True:
        try:
            # Return an item if one is immediately available, else raise the Empty exception, ignoring the timeout
            book = queue.get(block=False)
            logger.info(f"Dequeued {book}")
        except Empty:
            logger.info("Queue is empty")
            break
        except Exception as error:
            logger.error(f"Error dequeuing book: {error}")
            # Don't continue processing if any error occurs
            break

    return 0


if __name__ == "__main__":
    main()
