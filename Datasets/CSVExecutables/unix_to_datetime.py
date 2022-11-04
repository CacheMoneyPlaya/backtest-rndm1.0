import time
import _csv
import pandas as pd

def convert_from_unix_stamp(raw):
   return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(raw) / 1000))

def convert_unix_to_datetime(asset, exchange):
    out=open("Datasets/Data/" + asset + "_" + exchange + ".csv", "r")
    data=_csv.reader(out)

    data=[(convert_from_unix_stamp(row[0]),row[1],row[2],row[3],row[4],row[5]) for row in data]
    out.close()

    a = pd.DataFrame(data)
    a.to_csv("Datasets/Data/" + asset + "_" + exchange + "_datetime.csv", index=False, mode="w")

    print('Data retrieval complete!')
