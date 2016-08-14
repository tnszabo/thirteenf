import pandas as pd
#import numpy as np

file = "./output/13F_12-31-2015.txt"
df = pd.read_csv(file, header=0)
print df.head()

grouped = df.groupby(['Period','Manager','MgrCik','CUSIP','Name','PutCall','Class']).sum()
print grouped

