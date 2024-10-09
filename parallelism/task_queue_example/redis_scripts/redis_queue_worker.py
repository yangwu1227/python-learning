import redis

from redis_queue import SimpleQueue
from utils import setup_logger

logger = setup_logger("redis_dequeue")


def worker() -> int:
    """
    A worker is a Python process that typically runs in the background and exists solely as a work horse to perform lengthy or blocking tasks.
    """
    redis_connection = redis.Redis()
    queue = SimpleQueue(redis_connection, "word_count_queue")
    # If there are remaining tasks in the queue, dequeue them and process them
    if queue.size() > 0:
        queue.dequeue()
    else:
        logger.info("No more tasks in the queue")

    return 0


if __name__ == "__main__":
    worker()
