import csv
import sys
import os
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1], host='127.0.0.1', port=5432)
cur = conn.cursor()

output = sys.argv[2]

if not (os.path.isdir(output)):
    os.mkdir(output)

if (output [-1] != '/'):
        output  += '/'

with open(output+'users.csv') as csvfile:
    rows = csv.DictReader(csvfile)

    for row in rows:

        cur.execute("SELECT role_pk FROM roles WHERE title = %s", [row['role']])
        role = cur.fetchone()

        if role == None:
            cur.execute("INSERT INTO roles (title) VALUES (%s)", [row['role']])

        cur.execute("SELECT role_pk FROM roles WHERE title = %s", [row['role']])
        role = cur.fetchone()
    

        cur.execute("INSERT INTO users (username, password, role_fk, active) VALUES (%s, %s, %s, %s)", (row['username'], row['password'], role, row['active']))
    
    conn.commit()

with open(output+'facilities.csv') as csvfile:
    rows = csv.DictReader(csvfile)

    for row in rows:
        cur.execute("INSERT INTO facilities (common_name, facility_code) VALUES (%s, %s)", (row['common_name'], row['fcode']))
    
    conn.commit()

with open(output+'assets.csv') as csvfile:
    rows = csv.DictReader(csvfile)

    for row in rows:
        disposed = 'f'
        
        if row['disposed'] != 'NULL':
            disposed = 't'

        cur.execute("INSERT INTO assets (asset_tag, description, disposed, in_transit) VALUES (%s, %s, %s, %s)", (row['asset_tag'], row['description'], disposed, 'f'))

        cur.execute("SELECT asset_pk FROM assets WHERE asset_tag = %s", [row['asset_tag']])
        asset_fk = cur.fetchone()

        cur.execute("SELECT facility_pk FROM facilities WHERE facility_code = %s", [row['facility']])
        facility_fk = cur.fetchone()

        departure = row['disposed']
        if departure == 'NULL':
            departure = None

        cur.execute("INSERT INTO asset_location (asset_fk, facility_fk, arrive, depart) VALUES (%s, %s, %s, %s)", (asset_fk, facility_fk, row['acquired'], departure))

        
    conn.commit()

with open(output+'transfers.csv') as csvfile:
    rows = csv.DictReader(csvfile)

    for row in rows:

        cur.execute("SELECT user_pk FROM users WHERE username=%s", [row['request_by']])
        requester_fk = cur.fetchone()

        cur.execute("SELECT user_pk FROM users WHERE username=%s", [row['approve_by']])
        approver_fk = cur.fetchone()

        cur.execute("SELECT asset_pk FROM assets WHERE asset_tag=%s", [row['asset_tag']])
        asset_fk = cur.fetchone()        

        cur.execute("SELECT facility_pk FROM facilities WHERE facility_code=%s", [row['source']])
        src_fk = cur.fetchone()

        cur.execute("SELECT facility_pk FROM facilities WHERE facility_code=%s", [row['destination']])
        dest_fk = cur.fetchone()

        request_dt = row['request_dt']
                
        approved_dt = row['approve_dt']
        if approved_dt == '':
            approved_dt = None

        load_dt = row['load_dt']
        if load_dt == 'NULL':
            load_dt = None

        unload_dt = row['unload_dt']
        if unload_dt == 'NULL':
            unload_dt = None

        cur.execute("INSERT INTO transfers (requester_fk, approver_fk, asset_fk, src_fk, dest_fk, request_dt, approved_dt, load_dt, unload_dt) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)", (requester_fk, approver_fk, asset_fk, src_fk, dest_fk, request_dt, approved_dt, load_dt, unload_dt))
        
    conn.commit()


