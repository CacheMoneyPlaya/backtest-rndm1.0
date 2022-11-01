import time
import _csv
import pandas as pd

def convert_from_unix_stamp(raw):
   return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(raw) / 1000))

out=open("Datasets/btc_binance.csv","r")
data=_csv.reader(out)

data=[(convert_from_unix_stamp(row[0]),row[1],row[2],row[3],row[4],row[5]) for row in data]
out.close()

a = pd.DataFrame(data)
print(a)

a.to_csv("Datasets/btc_binance_datetime.csv", index=False)
