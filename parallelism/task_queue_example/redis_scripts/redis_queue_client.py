from pathlib import Path

import redis
from redis_queue import SimpleQueue
from utils import setup_logger
from word_count_task import count_words

book_multipler = 10
project_path = Path(__file__).resolve().parents[1]
data_path = project_path / "data"
logger = setup_logger("redis_enqueue")


def main() -> int:
    redis_connection = redis.Redis()
    queue = SimpleQueue(redis_connection, "word_count_queue")
    books = list(path.name for path in data_path.rglob("*.txt"))
    for _ in range(book_multipler):
        for book in books:
            queue.enqueue(count_words, book)
    logger.info(f"Enqueued {len(books) * book_multipler} books")

    return 0


if __name__ == "__main__":
    main()
