#!/usr/bin/env python3
import time


def count() -> None:
    """
    Synchronous count function.
    """
    print("One")
    time.sleep(1)
    print("Two")


def main() -> int:
    for i in range(3):
        count()

    return 0


if __name__ == "__main__":
    import os

    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    file_name = os.path.basename(__file__)
    print(f"The module {file_name} executed in {elapsed: .2f} seconds")
