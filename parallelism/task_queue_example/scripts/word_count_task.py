from collections import Counter
import json
import os
import sys
import uuid
from pathlib import Path

import nltk
from nltk.corpus import stopwords

from utils import setup_logger

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")
finally:
    stop_words = set(stopwords.words("english"))

project_path = Path(__file__).resolve().parents[1]
data_path = project_path / "data"
output_path = project_path / "output"

logger = setup_logger(name="word_count_task")


def save_file(filename: str, data: str) -> None:
    """
    Save data to a file with a random ID in the filename.

    Parameters
    ----------
    filename : str
        The base filename to use.
    data : str
        The string representation of the data to save.

    Notes
    -----
    The function saves the data to a file in the output directory with a random ID
    """
    # Random 32-character hexadecimal string
    random_id = uuid.uuid4().hex
    output_file = output_path / f"{filename}_{random_id}.txt"
    with open(output_file, "w") as file:
        file.write(data)


def count_words(filename: str) -> None:
    """
    Count the words in a file and save the top 20 most common words, not including any stop words.

    Parameters
    ----------
    filename : str
        The name of the file to process.
    """

    word_counter: Counter = Counter()
    data_file = data_path / filename
    with open(data_file, "r") as file:
        for line in file:
            words = line.split()
            word_counter.update(words)
    for stop_word in stop_words:
        del word_counter[stop_word]
    list_of_word_count_tuples = word_counter.most_common(20)
    word_to_count_map = dict(list_of_word_count_tuples)
    save_file(filename=filename, data=json.dumps(word_to_count_map, indent=None))

    process_id = os.getpid()
    logger.info(f"Process ID: {process_id} | Saved word counts as {filename}")


def main() -> int:
    count_words(sys.argv[1])
    return 0


if __name__ == "__main__":
    main()
