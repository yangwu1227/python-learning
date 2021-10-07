# ---------------------------------- Source ---------------------------------- #

# https://www.business-science.io/python/2021/09/21/python-read-csv.html

# ---------------------------------- Library --------------------------------- #

import pandas as pd
import glob
import os

# --------------------------------- File path -------------------------------- #

# Current working directory
os.getcwd()
# Create relative path
path = "car_data/"
# Return a list of paths matching a pathname pattern
# Similar to R's list.file(pattern)
list_of_csv = glob.glob(path + "*.csv")
# Examine
list_of_csv

# ------------------------ Method 1: Using a for loop ------------------------ #

# Instantiate container list
container_loop = []
# For loop
# Column names inferred from first line of files with header=0
# Do not specify row labels using index_col=None
for filename in list_of_csv:
    df = pd.read_csv(filename, header=0, index_col=None)
    # Lists are mutable
    container_loop.append(df)
# Output
for df in container_loop:
    print(df.describe())
# Examine one data frame
container_loop[4]
# Number of data frames
len(container_loop)
# Concatenate pandas objects along a particular axis
# Row-wise concatenation using axis=0
# Do not use index values along concatenation axis
df_loop = pd.concat(container_loop, axis=0, ignore_index=True)
df_loop.describe()

# ------------------------------- Method 2: Map ------------------------------ #

# Apply given function to each item of a given iterable (list, tuple, etc.)
# Return a map object which is an iterator
# An iterator is an object that contains a countable number of elements that can be iterated upon
map_obj = map(
    # Anonymous function
    lambda filename: pd.read_csv(filename, header=0, index_col=None),
    # Iterable
    list_of_csv
)
# Class
type(map_obj)
# Create list of data frames
container_map = list(map_obj)
# Row-wise concatenation
df_map = pd.concat(container_map, axis=0, ignore_index=True)
df_map.describe()

# ----------------------- Method 3: List comprehension ----------------------- #

# List comprehension
# Basic syntax is [i for i in iterable]
# Operations can be carried out on the first i
# We may also add if statements after "iterable"
container_comp = [pd.read_csv(filename, header=0, index_col=None)
                  for filename in list_of_csv]
# Row-wise concatenation
df_comp = pd.concat(container_comp, axis=0, ignore_index=True)
df_comp.describe()
