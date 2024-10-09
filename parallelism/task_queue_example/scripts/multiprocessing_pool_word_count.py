from multiprocessing import Pool, cpu_count
import time
from pathlib import Path

from word_count_task import count_words
from utils import setup_logger

num_processes = cpu_count() - 1
logger = setup_logger("multiprocessing_pool")
project_path = Path(__file__).resolve().parents[1]
data_path = project_path / "data"


def main() -> int:
    logger.info(f"Running word count task with {num_processes} num_processes")
    data_files = list(path.name for path in data_path.rglob("*.txt"))

    start_time = time.time()
    with Pool(num_processes) as pool:
        # Map is blocking and will not return until all tasks are complete, so there is no need to call pool.close and pool.join
        pool.map(count_words, data_files)

    logger.info(f"Word count task completed in {time.time() - start_time:.2f} seconds")
    return 0


if __name__ == "__main__":
    main()
