import lib.thirteenfdb as db

db.getFilings().to_csv('filings.csv', index = False)
