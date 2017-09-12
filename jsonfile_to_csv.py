import json
import pandas as pd

jsonfile = r"C:\Users\samantha.gibbes\Documents\gis\hansen_2015\hadoop_downloads_from_s3\080715\extent2000_20170531.json"

with open(jsonfile) as datafile:
    data = json.load(datafile)
    real_data = data['data']
    
    df = pd.DataFrame(real_data)
    df.to_csv("results.csv", index=None)