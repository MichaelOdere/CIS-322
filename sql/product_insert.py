import psycopg2 as p
import csv
import sys

conn = p.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))

cur = conn.cursor()

with open('osnap_legacy/product_list.csv') as f:
    stmt = "INSERT INTO products (vendor, description, alt_description) VALUES (%s, %s, %s)"
    reader = csv.DictReader(f)
    for row in reader:
        data = (row['vendor'], row['name'], row['description'])
        cur.execute(stmt, data)

stmt1 = "INSERT INTO products (description) SELECT (%s) WHERE NOT EXISTS (SELECT 1 FROM products WHERE (description = %s AND vendor IS NULL))"
stmt2 = "INSERT INTO assets (product_fk, asset_tag) VALUES ((SELECT product_pk FROM products WHERE (description = %s AND vendor IS NULL) LIMIT 1),%s)"

with open('osnap_legacy/DC_inventory.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data1 = (row['product'],row['product'])
        data2 = (row['product'],row['asset tag'])
        cur.execute(stmt1, data1)
        cur.execute(stmt2, data2)

with open('osnap_legacy/HQ_inventory.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data1 = (row['product'],row['product'])
        data2 = (row['product'],row['asset tag'])
        cur.execute(stmt1, data1)
        cur.execute(stmt2, data2)

with open('osnap_legacy/MB005_inventory.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data1 = (row['product'],row['product'])
        data2 = (row['product'],row['asset tag'])
        cur.execute(stmt1, data1)
        cur.execute(stmt2, data2)

with open('osnap_legacy/NC_inventory.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data1 = (row['product'],row['product'])
        data2 = (row['product'],row['asset tag'])
        cur.execute(stmt1, data1)
        cur.execute(stmt2, data2)

with open('osnap_legacy/SPNV_inventory.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data1 = (row['product'],row['product'])
        data2 = (row['product'],row['asset tag'])
        cur.execute(stmt1, data1)
        cur.execute(stmt2, data2)

with open('osnap_legacy/transit.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        stmt = "INSERT INTO facilities (common_name) SELECT (%s) WHERE NOT EXISTS (SELECT 1 FROM facilities WHERE common_name = %s)"

        data11 = (row['src facility'],row['src facility'])
        data12 = (row['dst facility'],row['dst facility'])

        cur.execute(stmt, data11)
        cur.execute(stmt, data12)

        tags = row['asset tag'].split(', ')

        for tag in tags:
            tag1_stmt = "INSERT INTO asset_at (asset_fk, facility_fk) VALUES ((SELECT asset_pk FROM assets WHERE asset_tag = %s), (SELECT facility_pk FROM facilities WHERE common_name = %s))"
            tag2_stmt = "UPDATE asset_at SET depart_dt=%s WHERE ((facility_fk=(SELECT facility_pk FROM facilities WHERE common_name=%s)) AND (asset_fk=(SELECT asset_pk FROM assets WHERE asset_tag=%s)))"
            cur.execute(tag1_stmt, (tag,row['src facility']))
            cur.execute(tag2_stmt, (row['depart date'],row['src facility'],tag))
            cur.execute(tag1_stmt, (tag,row['dst facility']))
            cur.execute(tag2_stmt, (row['arrive date'],row['dst facility'],tag))

with open('osnap_legacy/security_levels.csv') as f:
    reader = csv.DictReader(f)

    for row in reader:
        stmt = "INSERT INTO levels (abbrv, comment) VALUES (%s, %s)"
        cur.execute(stmt,(row['level'],row['description']))

with open('osnap_legacy/security_compartments.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        stmt = "INSERT INTO compartments (abbrv, comment) VALUES (%s, %s)"
        cur.execute(stmt,(row['compartment_tag'],row['compartment_desc']))

# commit the changes to the database
conn.commit()

# close the connection nicely
cur.close()
conn.close()
 
