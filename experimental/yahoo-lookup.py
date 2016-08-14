import pandas.io.data as web
import datetime

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2013, 1, 27)
# call with yahoo or google as second parameter
f = web.DataReader("AAPL", 'google', start, end)
print f.ix['2010-01-04']