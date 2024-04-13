import pandas as pd
import glob
import os
from collections.abc import Sequence
from typing import List
from argparse import ArgumentParser, Namespace

# --------------------------------- File path -------------------------------- #

def get_csv_files(path: str) -> List[str]:
    """
    Return a list of CSV file paths in the given directory.

    Parameters
    ----------
    path : str
        The directory to search for CSV files.

    Returns
    -------
    List[str]
        A list of paths to CSV files found in the specified directory.
    """
    return glob.glob(os.path.join(path, "*.csv"))

# ------------------------ Method 1: Using a for loop ------------------------ #

def method_for_loop(sequence_of_csv: Sequence[str]) -> pd.DataFrame:
    """
    Read CSV files using a for loop and concatenate them into a single DataFrame.

    Parameters
    ----------
    sequence_of_csv : Sequence[str]
        A sequence of CSV file paths.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing concatenated data from all CSV files.
    """
    container_loop = []
    for filename in sequence_of_csv:
        df = pd.read_csv(filename, header=0, index_col=None)
        container_loop.append(df)
    return pd.concat(container_loop, axis=0, ignore_index=True)

# ------------------------------- Method 2: Map ------------------------------ #

def method_map(sequence_of_csv: Sequence[str]) -> pd.DataFrame:
    """
    Read CSV files using the map function and concatenate them into a single DataFrame.

    Parameters
    ----------
    sequence_of_csv : Sequence[str]
        A sequence of CSV file paths.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing concatenated data from all CSV files.
    """
    map_obj = map(lambda filename: pd.read_csv(filename, header=0, index_col=None), sequence_of_csv)
    container_map = list(map_obj)
    return pd.concat(container_map, axis=0, ignore_index=True)

# ----------------------- Method 3: List comprehension ----------------------- #

def method_list_comprehension(list_of_csv: List[str]) -> pd.DataFrame:
    """
    Read CSV files using list comprehension and concatenate them into a single DataFrame.

    Parameters
    ----------
    list_of_csv : Sequence[str]
        A list of CSV file paths.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing concatenated data from all CSV files.
    """
    container_comp = [pd.read_csv(filename, header=0, index_col=None) for filename in list_of_csv]
    return pd.concat(container_comp, axis=0, ignore_index=True)

# ----------------------------------- Main ----------------------------------- #

def parse_arguments() -> Namespace:
    """
    Parse command line arguments to determine the method and path for processing CSV files.

    Returns
    -------
    Namespace
        The parsed arguments with `method` and `path` attributes.
    """
    parser = ArgumentParser(description="Process CSV files in different ways.")
    parser.add_argument("-m", "--method", choices=["loop", "map", "comp"], default="loop",
                        help="Method to use for processing CSV files (loop, map, or comp)")
    parser.add_argument("-p", "--path", default="car_data/",
                        help="Path to the directory containing CSV files")
    return parser.parse_args()

def main():
    
    args = parse_arguments()
    csv_files = get_csv_files(args.path)

    if args.method == "loop":
        result = method_for_loop(csv_files)
    elif args.method == "map":
        result = method_map(csv_files)
    else:
        result = method_list_comprehension(csv_files)

    print(result.describe())

if __name__ == "__main__":
    
    main()
