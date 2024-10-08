import os
from datetime import datetime


def hash_it(x):
    # Get the current time to log when the hash is calculated
    current_time = datetime.now().strftime("%H:%M:%S.%f")
    # Retrieve the PYTHONHASHSEED environment variable if set
    hash_seed = os.environ.get("PYTHONHASHSEED", "not set")
    # Return the hash along with the current time and seed information
    return (hash(x), current_time, hash_seed)


def main():
    now_datetime = datetime.now()
    string = "Yang Wu"
    bytes_string = b"Yang Wu"

    for item in [now_datetime, string, bytes_string]:
        print(f"Hash for the same item {item} multiple times:")
        print({key: hash_it(item) for key in range(3)})

    return 0


if __name__ == "__main__":
    main()
