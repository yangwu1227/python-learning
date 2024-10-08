# --------------------- Packages -------------------- #

import os
from argparse import ArgumentParser, Namespace

import pandas as pd

# ------------------------- Functions ------------------------ #


def read_csv_file(filepath: str, separator: str = ";") -> pd.DataFrame:
    """
    Read data from a CSV file and return a pandas DataFrame.

    Parameters
    ----------
    filepath : str
        Path to the CSV file.
    separator : str, optional
        Delimiter to use (default is ';').

    Returns
    -------
    pd.DataFrame
        Data from the CSV file as a DataFrame.
    """
    return pd.read_csv(filepath, sep=separator, header=0, index_col=None)


def export_to_txt(dataframe: pd.DataFrame, filepath: str) -> None:
    """
    Export a DataFrame to a text file, truncating the file first if it exists.
    This uses mode 'w+', which stands for writing and reading; it truncates the file first.
    See more on file modes: https://docs.python.org/3/library/functions.html#open.

    Parameters
    ----------
    dataframe : pd.DataFrame
        DataFrame to export.
    filepath : str
        Path where the text file will be saved.
    """
    with open(file=filepath, mode="w+") as f:
        df_string = dataframe.to_string(header=True, index=False)
        f.write(df_string)


def read_txt_method1(filepath: str) -> pd.DataFrame:
    """Read a text file using fixed-width columns."""
    return pd.read_fwf(filepath, colspecs="infer")


def read_txt_method2(filepath: str) -> pd.DataFrame:
    """
    Read a text file using a regular expression as delimiter to handle multiple whitespace characters.
    The regular expression used is '\s{1,}', which matches one or more whitespace characters.

    Parameters
    ----------
    filepath : str
        Path to the text file.

    Returns
    -------
    pd.DataFrame
        Data from the text file as a DataFrame.
    """
    return pd.read_table(filepath, sep=r"\s{1,}")


def read_txt_method3(filepath: str) -> pd.DataFrame:
    """
    Read a text file using a regular expression as delimiter with read_csv method.
    This is similar to method 2 but uses the read_csv function from pandas.
    The regular expression '\s{1,}' is used to split on one or more whitespace characters.

    Parameters
    ----------
    filepath : str
        Path to the text file.

    Returns
    -------
    pd.DataFrame
        Data from the text file as a DataFrame.
    """
    return pd.read_csv(filepath, sep=r"\s{1,}")


# ------------------------ Main Program ----------------------- #


def parse_arguments() -> Namespace:
    """
    Parse command line arguments to determine the method for processing text files.

    Returns
    -------
    Namespace
        The parsed command line arguments.
    """
    parser = ArgumentParser(
        description="Process text files using various pandas methods."
    )
    parser.add_argument(
        "-m",
        "--method",
        choices=["1", "2", "3"],
        default="1",
        help="Method to use for reading text files (1=fwf, 2=table, 3=csv)",
    )
    parser.add_argument("--path", type=str)
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    csv_path = os.path.join(args.path, "bank-full.csv")
    txt_path = os.path.join(args.path, "bank-full.txt")

    df_csv = read_csv_file(csv_path)
    export_to_txt(df_csv, txt_path)

    if args.method == "1":
        df_txt = read_txt_method1(txt_path)
    elif args.method == "2":
        df_txt = read_txt_method2(txt_path)
    else:
        df_txt = read_txt_method3(txt_path)

    print(df_txt.describe())

    return 0


if __name__ == "__main__":
    main()
