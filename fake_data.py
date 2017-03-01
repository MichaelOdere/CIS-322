import datetime
import psycopg2


conn = psycopg2.connect(dbname='lost_db', host='127.0.0.1', port=5432)
cur = conn.cursor()

username = "log"
password = "log"
role = "logistics officer"

cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)",(username, password))
conn.commit()

cur.execute("SELECT title FROM roles WHERE (title=%s)",[role])

if (cur.fetchone() is None):
    cur.execute("INSERT INTO roles (title) VALUES (%s)", [role])
    conn.commit()
    
cur.execute("UPDATE users SET role_fk=(SELECT role_pk FROM roles WHERE title=%s) WHERE username=%s", (role,username))
conn.commit()

name = 'oregon'
code = 1
cur.execute("INSERT INTO facilities (common_name, facility_code) VALUES (%s,%s)",(name,code))

name = 'cali'
code = 2
cur.execute("INSERT INTO facilities (common_name, facility_code) VALUES (%s,%s)",(name,code))

tag = 1
description = 'lol'
facility = 2
arrive = datetime.datetime.now()
cur.execute("INSERT INTO assets (tag, description) VALUES (%s, %s)", (tag, description))
cur.execute("INSERT INTO asset_location (asset_fk, facility_fk, arrive) VALUES ((SELECT asset_pk FROM assets WHERE tag=CAST(%s as integer)),(SELECT facility_pk FROM facilities  WHERE common_name=%s),%s)",(tag, facility, arrive))

tag = 2
description = 'fake'
facility = 2
arrive = datetime.datetime.now()
cur.execute("INSERT INTO assets (tag, description) VALUES (%s, %s)", (tag, description))
cur.execute("INSERT INTO asset_location (asset_fk, facility_fk, arrive) VALUES ((SELECT asset_pk FROM assets WHERE tag=CAST(%s as integer)),(SELECT facility_pk FROM facilities  WHERE common_name=%s),%s)",(tag, facility, arrive))

conn.commit()


