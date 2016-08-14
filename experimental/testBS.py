import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from pandas import read_html

url = 'http://www.fdic.gov/bank/individual/failed/banklist.html'
dframe_list = pd.io.html.read_html(url)
print(dframe_list)
dframe = dframe_list[0]
print(dframe)