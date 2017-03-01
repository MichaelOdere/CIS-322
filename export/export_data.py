import csv
import sys
import os
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=5432)
cur = conn.cursor()

output = sys.argv[2]
    
if not (os.path.isdir(output)):
    os.mkdir(output)


