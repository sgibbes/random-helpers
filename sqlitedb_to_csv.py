import os
import simpledbf
import pandas as pd
import sys
import sqlite3
import csv

def write_to_csv(input_db):
    conn = sqlite3.connect(input_db)
    cursor = conn.cursor()
    cursor.execute("select * from forest_loss;")
    with open("out.csv", "wb") as csv_file:              # Python 2 version
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description]) # write headers
        csv_writer.writerows(cursor)


write_to_csv('zstats_results_db.db')