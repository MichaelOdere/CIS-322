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

with open(output + 'users.csv', 'w') as data:
	w = csv.writer(data, quotechar="'")
	w.writerow(['username', 'password', 'role', 'active'])
    
	cur.execute("SELECT u.username, u.password, r.title, u.active FROM users AS u INNER JOIN roles AS r ON r.role_pk=u.role_fk")
	db_output = cur.fetchall()

	for row in db_output:
		w.writerow([row[0], row[1], row[2], row[3]])

with open(output + 'facilities.csv', 'w') as data:
	w = csv.writer(data, quotechar="'")
	w.writerow(['facility_code', 'common_name'])
    
	cur.execute("SELECT facility_code, common_name FROM facilities")
	db_output = cur.fetchall()

	for row in db_output:
		w.writerow([row[0], row[1]])

with open(output + 'assets.csv', 'w') as data:
	w = csv.writer(data, quotechar="'")
	w.writerow(['asset_tag', 'description', 'facility', 'acquired', 'disposed'])
	
	cur.execute("SELECT a.asset_tag, a.description, f.facility_code, al.arrive, al.depart FROM assets AS a INNER JOIN asset_location AS al ON al.asset_fk=a.asset_pk INNER JOIN facilities AS f ON f.facility_pk=al.facility_fk")
	db_output = cur.fetchall()

	for row in db_output:
            if row[4] == None:
                w.writerow([row[0], row[1], row[2], row[3], "Null"])
            else:
                w.writerow([row[0], row[1], row[2], row[3], row[4]])

with open(output + 'transfers.csv', 'w') as data:
    w = csv.writer(data, quotechar="'")
    w.writerow(['asset_tag', 'request_by', 'request_dt', 'approve_by', 'approve_dt', 'source', 'destination', 'load_dt', 'unload_dt'])
    cur.execute("SELECT a.asset_tag, u1.username, t.request_dt, u2.username, t.approved_dt, f1.facility_code, f2.facility_code, t.load_dt, t.unload_dt FROM transfers AS t INNER JOIN users AS u1 on t.requester_fk = u1.user_pk INNER JOIN users AS u2 ON u2.user_pk = t.approver_fk INNER JOIN assets AS a ON a.asset_pk = t.asset_fk INNER JOIN facilities AS f1 ON f1.facility_pk = t.src_fk INNER JOIN facilities AS f2 ON f2.facility_pk = t.dest_fk ")
    db_output = cur.fetchall()
    
    for row in db_output:
        w.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
