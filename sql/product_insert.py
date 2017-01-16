import psycopg2 as p
import csv
import sys

conn = p.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))

cur = conn.cursor()

stmt = "INSERT INTO products (vendor, description, alt_description) VALUES (%s, %s, %s)"

with open('osnap_legacy/product_list.csv') as f:
	reader = csv.DictReader(f)
	for row in reader:
		data = (row['vendor'], row['name'], row['description'])
		cur.execute(stmt, data)
		#print (row['name'])

stmt = "INSERT INTO products (vendor, description, alt_description) VALUES (%s, %s, %s)"
	
# commit the changes to the database
conn.commit()

# close the connection nicely
cur.close()
conn.close()
