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

        cur.execute("UPDATE users SET role_fk=(SELECT role_pk FROM roles WHERE title=%s)", [role])
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

def asset_exists(tag):
    cur.execute("SELECT tag FROM assets WHERE tag=%s",[tag])
    return (cur.fetchone() is not None)

@app.route('/add_asset', methods = ['GET','POST'])
def add_asset():
    if request.method == 'GET':

        cur.execute("SELECT tag, description FROM assets")
        assets = cur.fetchall()
        assets_data = []
        for asset in assets:
            row = dict()
            row['tag'] = asset[0]
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
        tag = request.form['tag']
        description = request.form['description']
        facility = request.form['facility_name']
        arrive =  request.form['arrive']
        if asset_exists(tag):
            return render_template('asset_exists.html')
        else:
            cur.execute("INSERT INTO assets (tag, description) VALUES (%s, %s)", (tag, description))
            conn.commit()
            cur.execute("INSERT INTO asset_location (asset_fk, facility_fk, arrive) VALUES ((SELECT asset_pk FROM assets WHERE tag=%s),(SELECT facility_pk FROM facilities  WHERE common_name=%s),%s)",(tag, facility, arrive))

            conn.commit()            
            return redirect(url_for('add_asset'))

    return render_template('add_asset.html')

def is_disposed(tag):
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("SELECT tag FROM assets WHERE tag=%s AND disposed = 't'",[tag])
    return (cur.fetchone() is not None)

@app.route('/dispose_asset', methods=(['POST','GET']))
def dispose_asset():
    if request.method == 'GET':
            return render_template('dispose_asset.html')

    cur.execute("SELECT title FROM roles WHERE role_pk=(SELECT role_fk FROM users WHERE username=%s)",[session['username']])
    role = cur.fetchone()
    print ("BELLOW IS ROLE")
    print (role)
    if (role[0].lower() != 'logistics officer'):
        return render_template('unauthorized_access.html')

    if request.method == 'POST':
        tag  = request.form['tag']
        date = request.form['date']

        if not asset_exists(tag):
           return render_template('bad_dispose.html')

        if is_disposed(tag):
            return render_template('already_disposed.html')

        cur.execute("UPDATE assets SET disposed=%s WHERE tag=%s",(True, tag))
        conn.commit()

        cur.execute("UPDATE asset_location SET depart=%s WHERE asset_fk=(SELECT asset_pk FROM assets WHERE tag=%s)",(date,tag)) 
        conn.commit()    
        return render_template('dashboard.html', username=session['username'])



def facility_name_exists(name):
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("SELECT facility_pk FROM facilities WHERE common_name=%s",[name])
    return (cur.fetchone() is not None)

@app.route('/asset_report', methods=(['POST', 'GET']))
def asset_report():
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    if request.method == 'POST':
        facility = request.form['facility']
        date = request.form['report_date']
        if (facility == ' '):
            cur.execute("SELECT assets.tag, assets.description, facilities.common_name, aa.arrive, aa.depart FROM assets, facilities, asset_location AS aa")             
        elif (facility_name_exists(facility)):
            cur.execute("SELECT assets.tag, assets.description, facilities.common_name, aa.arrive, aa.depart FROM assets, facilities, asset_location AS aa WHERE (assets.asset_pk=aa.asset_fk AND facilities.facility_pk=aa.facility_fk AND facilities.common_name=%s AND aa.arrive<=%s)",(facility,date))
        else:
            cur.execute("SELECT assets.tag, assets.description, facilities.common_name, aa.arrive, aa.depart FROM assets, facilities, asset_location AS aa WHERE (assets.asset_pk=aa.asset_fk AND facilities.facility_pk=aa.facility_fk AND aa.arrive<=%s)",[date])        

        values = cur.fetchall()
        return render_template('asset_report.html', rows=values)        

    return render_template('asset_report.html')


        
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
