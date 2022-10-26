import pandas as pd
import glob
import time

start_time = time.perf_counter()

list_of_csv = glob.glob('data/*.csv')

container = list(map(lambda x: pd.read_csv(x, header=0), list_of_csv))

finish_time = time.perf_counter()

print('It took ', finish_time - start_time,
      ' seconds to finish reading the csv files.')
