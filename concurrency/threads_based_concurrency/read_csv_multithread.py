import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import glob
import time

if __name__ == '__main__':

    start_time = time.perf_counter()

    list_of_csv = glob.glob('data/*.csv')

    with ThreadPoolExecutor(max_workers=20) as executor:
        container = executor.map(
            lambda x: pd.read_csv(x, header=0), list_of_csv)

    finish_time = time.perf_counter()

    print('It took ', finish_time - start_time,
          ' seconds to finish reading the csv files.')
