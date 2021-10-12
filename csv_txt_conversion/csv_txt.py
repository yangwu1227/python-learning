# --------------------- Packages -------------------- #

import pandas as pd
import os
import glob as gl

# ------------------------- Read in data in .csv format ------------------------ #

# Working directory
os.getcwd()
# Read .csv file
df_csv = pd.read_csv(
    "./bank data/bank-full.csv",
    sep=";",
    header=0,
    index_col=None
)
# Shape
df_csv.shape
# Descriptive statistics
df_csv.describe()

# ---------------------- Export data frame as .txt file ---------------------- #

# Open for reading and writing, truncating the file first
# Other modes can be found via https://docs.python.org/3/library/functions.html#open
with open(file="./bank data/bank-full.txt", mode='w+') as f:
    df_string = df_csv.to_string(
        # Columns to write (default all)
        columns=None,
        header=True,
        index=False
    )
    # Write to disk
    f.write(df_string)

# ------------------------ Read in data in .txt format ----------------------- #

# Method 1
df_txt = pd.read_fwf(
    "./bank data/bank-full.txt",
    # Different fields have different widths as delimiters
    colspecs="infer"
)

# Method 2
df_txt_2 = pd.read_table(
    "./bank data/bank-full.txt",
    # Use regular expressions
    # At least 1 or more whitespace characters
    # Use \s == whitespace and {1,} == at least one
    sep=r'\s{1,}'
)

# Method 3
df_txt_3 = pd.read_csv(
    "./bank data/bank-full.txt",
    sep=r'\s{1,}'
)
