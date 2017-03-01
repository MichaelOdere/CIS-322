from flask import Flask, render_template, request, session, redirect, url_for
from config import dbname, dbhost, dbport
import sys
import psycopg2
import json

app = Flask(__name__)
SECRET_KEY = 'this_is_my_fake_key'
app.secret_key = SECRET_KEY

conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
cur = conn.cursor()

def exists(username):
    cur.execute("SELECT username FROM users WHERE username=%s",(username,))
    return (cur.fetchone() is not None)

def valid_username(username, password, role):
    if (len(username) <= 16 and len(password) <= 16 and len(role) <= 32):
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)",(username, password))
        conn.commit()

        cur.execute("SELECT title FROM roles WHERE (title=%s)",[role])

        if (cur.fetchone() == None):
            cur.execute("INSERT INTO roles (title) VALUES (%s)", [role])
            conn.commit()

        cur.execute("UPDATE users SET role_fk=(SELECT role_pk FROM roles WHERE title=%s) WHERE username=%s", (role,username))

        conn.commit()
        return True
    else:
        return False

def check_password(username, password):
    cur.execute("SELECT password  FROM users WHERE username=%s AND password = %s",(username,password))
    return (cur.fetchone() is not None)

@app.route('/create_user', methods = ['POST','GET'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if exists(username):
            return render_template('username_exists.html')
        elif valid_username(username, password, role):
            session['username'] = username
            session['role'] = role
            return render_template('success.html')
        else:
            return render_template('create_user.html')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        if check_password(username,password):
            session['username'] = username
            cur.execute("SELECT title FROM roles WHERE role_pk=(SELECT role_fk FROM users WHERE username=%s)",[session['username']])
            role = cur.fetchone()
            session['role'] = role[0]
            return dashboard()
        else:
            return render_template('invalid_login.html')

@app.route('/dashboard', methods = ['GET'])
def dashboard():

    values = []
    role = session['role']
    if role.lower() == 'logistics officer':
        cur.execute("SELECT a.description, a.asset_tag, t.transfer_pk FROM assets AS a, transfers AS t WHERE (a.asset_pk=t.asset_fk AND t.approved_dt is not null AND (t.load_dt is null OR t.unload_dt is null))")
        results = cur.fetchall()
        if results != None:
            for r in results:
                row = dict()
                row['description'] = r[0]
                row['asset_tag'] = r[1]
                row['transfer_pk'] = r[2]
                values.append(row)
            session['dashboard'] = values
    if role.lower() == 'facilities officer':
        cur.execute("SELECT a.asset_tag, f.common_name, t.transfer_pk FROM assets AS a, transfers AS t, facilities AS f WHERE f.facility_pk=t.dest_fk AND a.asset_pk=t.asset_fk AND t.approver_fk is null")
        results = cur.fetchall()
        if results != None:
            for r in results:
                row = dict()
                row['destination_facility'] = r[1]
                row['transfer_pk'] = r[2]
                row['asset_tag'] = r[0]
                values.append(row)
            session['dashboard'] = values
    return render_template('dashboard.html', username = session['username'])

def facility_exists(name, code):
    cur.execute("SELECT common_name FROM facilities WHERE common_name=%s",[name])
    if (cur.fetchone() is not None):
        return True
    cur.execute("SELECT facility_code FROM facilities WHERE facility_code=%s",[code])
    return (cur.fetchone() is not None)

def create_facility(name, code):
    cur.execute("INSERT INTO facilities (common_name, facility_code) VALUES (%s,%s)",(name,code))
    conn.commit()

@app.route('/add_facility', methods = ['POST','GET'])
def add_facility():

    if request.method == 'GET':
        cur.execute("SELECT common_name, facility_code FROM facilities")
        facilities = cur.fetchall()
        facilities_data = []
        for facility in facilities:
            row = dict()
            row['common_name'] = facility[0]
            row['code'] = facility[1]
            facilities_data.append(row)
        session['facilities'] = facilities_data
        return render_template('add_facility.html')
    elif request.method == 'POST':
        name = request.form['common_name']
        code = request.form['code']
        if facility_exists(name, code):
            return render_template('facility_exists.html')
        else:
            create_facility(name, code)
        return redirect(url_for('add_facility'))
    return render_template('add_facility.html')

def asset_exists(asset_tag):
    cur.execute("SELECT asset_tag FROM assets WHERE asset_tag=%s",[asset_tag])
    return (cur.fetchone() is not None)

@app.route('/add_asset', methods = ['GET','POST'])
def add_asset():
    if request.method == 'GET':

        cur.execute("SELECT asset_tag, description FROM assets")
        assets = cur.fetchall()
        assets_data = []
        for asset in assets:
            row = dict()
            row['asset_tag'] = asset[0]
            row['description'] = asset[1]
            assets_data.append(row)
        session['assets'] = assets_data

        cur.execute("SELECT common_name FROM facilities")
        facilities = cur.fetchall()
        facility_data = []
        for facility in facilities:
            row = dict()
            row['common_name'] = facility[0]
            facility_data.append(row)
        session['facilities'] = facility_data

        return render_template('add_asset.html')

    if request.method == 'POST':
        asset_tag = request.form['asset_tag']
        description = request.form['description']
        facility = request.form['facility_name']
        arrive =  request.form['arrive']
        if asset_exists(asset_tag):
            return render_template('asset_exists.html')
        else:
            cur.execute("INSERT INTO assets (asset_tag, description) VALUES (%s, %s)", (asset_tag, description))
            conn.commit()
            cur.execute("INSERT INTO asset_location (asset_fk, facility_fk, arrive) VALUES ((SELECT asset_pk FROM assets WHERE asset_tag=%s),(SELECT facility_pk FROM facilities  WHERE common_name=%s),%s)",(asset_tag, facility, arrive))

            conn.commit()
            return redirect(url_for('add_asset'))

    return render_template('add_asset.html')

def is_disposed(asset_tag):

    cur.execute("SELECT asset_tag FROM assets WHERE asset_tag=%s AND disposed = 't'",[asset_tag])
    return (cur.fetchone() is not None)

@app.route('/dispose_asset', methods=(['POST','GET']))
def dispose_asset():
    if request.method == 'GET':
            return render_template('dispose_asset.html')

    cur.execute("SELECT title FROM roles WHERE role_pk=(SELECT role_fk FROM users WHERE username=%s)",[session['username']])
    role = cur.fetchone()
    if (role[0].lower() != 'logistics officer'):
        return render_template('unauthorized_access.html')

    if request.method == 'POST':
        asset_tag  = request.form['asset_tag']
        date = request.form['date']

        if not asset_exists(asset_tag):
           return render_template('bad_dispose.html')

        if is_disposed(asset_tag):
            return render_template('already_disposed.html')

        cur.execute("UPDATE assets SET disposed=%s WHERE asset_tag=%s",(True, asset_tag))
        conn.commit()

        cur.execute("UPDATE asset_location SET depart=%s WHERE asset_fk=(SELECT asset_pk FROM assets WHERE asset_tag=%s)",(date,asset_tag))
        conn.commit()
        return render_template('dashboard.html', username=session['username'])



def facility_name_exists(name):

    cur.execute("SELECT facility_pk FROM facilities WHERE common_name=%s",[name])
    return (cur.fetchone() is not None)

@app.route('/asset_report', methods=(['POST', 'GET']))
def asset_report():

    if request.method == 'POST':
        facility = request.form['facility']
        date = request.form['report_date']

        if (facility_name_exists(facility)):
            cur.execute("SELECT a.asset_tag, a.description, f.common_name, al.arrive, al.depart FROM assets AS a, facilities AS f, asset_location AS al WHERE (a.asset_pk=al.asset_fk AND f.facility_pk=al.facility_fk AND f.common_name=%s AND al.arrive<=%s)",(facility,date))
        else:
            cur.execute("SELECT a.asset_tag, a.description, f.common_name, al.arrive, al.depart FROM assets AS a, facilities AS f, asset_location AS al WHERE (a.asset_pk=al.asset_fk AND f.facility_pk=al.facility_fk AND al.arrive<=%s)",[date])        

        values = cur.fetchall()
        return render_template('asset_report.html', rows=values)

    return render_template('asset_report.html')

@app.route('/transfer_req', methods=(['POST', 'GET']))
def transfer_req():

    if session['role'].lower() != 'logistics officer':
        return render_template('unauthorized_access.html')

    if request.method == 'GET':
        cur.execute("SELECT asset_tag FROM assets WHERE disposed = 'f'")
        temp  = cur.fetchall()
        assets = []

        for asset in temp:
            assets.append(asset[0])
        cur.execute("SELECT common_name FROM facilities")
        temp  = cur.fetchall()
        facilities = []

        for fac in temp:
            facilities.append(fac[0])

        return render_template('transfer_req.html', assets=assets, facilities=facilities)

    if request.method == 'POST':
        asset = request.form['asset_to_transfer']
        facility = request.form['facility_to_transfer']

        cur.execute("SELECT user_pk FROM users WHERE username = %s", (session['username'],))
        requester = cur.fetchone()

        cur.execute("SELECT asset_pk FROM assets WHERE asset_tag = %s", [asset])
        asset_fk = cur.fetchone()

        if(asset_fk is None):
            return render_template('general_error.html', general_error='No such asset')

        cur.execute("SELECT facility_pk FROM facilities WHERE common_name = %s", [facility])
        dest_facility = cur.fetchone()

        if(dest_facility is None):
            return render_template('general_error.html', general_error='No such facility')

        cur.execute("SELECT facility_fk FROM asset_location WHERE asset_fk = %s", [asset_fk])
        src_facility = cur.fetchone()

        cur.execute("INSERT INTO transfers (requester_fk, asset_fk, src_fk, dest_fk, request_dt) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)", (requester, asset_fk, src_facility, dest_facility))

        conn.commit()

        return redirect(url_for('transfer_request_success'))

@app.route('/transfer_request_success')
def transfer_request_success():
    return render_template('transfer_request_success.html')

@app.route('/approve_req', methods=('GET', 'POST'))
def approve_req():
    if session['role'].lower() != 'facilities officer':
        return render_template('unauthorized_access.html')

    if request.method == 'GET':
        transfer_pk = request.args['transfer_pk']
        approval_tag = request.args['approval_tag']

        return render_template('approve_req.html', transfer_pk=transfer_pk, approval_tag=approval_tag)

    if request.method == 'POST':
        transfer_pk = int(request.form['transfer_pk'])

        if request.form.get('approve'):
            cur.execute("UPDATE transfers SET approver_fk=(SELECT user_pk FROM users WHERE username=%s), approved_dt=CURRENT_TIMESTAMP WHERE (transfer_pk=CAST(%s as integer))", (session['username'], transfer_pk))
            conn.commit()

        if request.form.get('reject'):
            cur.execute("DELETE FROM transfers WHERE (transfer_pk=CAST(%s as integer))",[transfer_pk])
            conn.commit()

    return redirect(url_for('dashboard'))

@app.route('/update_transit', methods=('GET', 'POST'))
def update_transit():

    if session['role'].lower() != 'logistics officer':
        return render_template('general_error.html', general_error='No such must be logistics officer to in order to update transit data')

        transfer_pk = request.args['transfer_pk']
        asset_tag = request.args['asset_tag']

        return render_template('update_transit.html', transfer_pk=transfer_pk, asset_tag=asset_tag)
    
    if request.method == 'GET':
        transfer_pk = request.args['transfer_pk']
        asset_tag = request.args['asset_tag']
        return render_template('update_transit.html', transfer_pk=transfer_pk, asset_tag=asset_tag)

    if request.method == 'POST':
        transfer_pk = request.form['transfer_pk']
        cur.execute("SELECT unload_dt FROM transfers WHERE transfer_pk=CAST(%s as integer)", [transfer_pk])

        load_dt = request.form['load_dt']
        if (load_dt != None or load_dt != ' '):
            cur.execute("UPDATE transfers SET load_dt=%s WHERE transfer_pk=CAST(%s as integer)", (load_dt, transfer_pk))

        unload_dt = request.form['unload_dt']
        if (unload_dt != None or unload_dt != ' ' ):
            cur.execute("UPDATE transfers SET unload_dt=%s WHERE transfer_pk=CAST(%s as integer)", (unload_dt, transfer_pk))

        conn.commit()

        return redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
