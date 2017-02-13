from flask import Flask, render_template, request
from config import dbname, dbhost, dbport
import sys
import psycopg2
import json

conn = psycopg2.connect(dbname=dbname, host=dbhost,port=dbport)
cur = conn.cursor()

app = Flask(__name__)

def main():
    print ("GOODBYE")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/rest')
def rest():
    return render_template('rest.html')

@app.route('/rest/lost_key', methods=['POST'])
def lost_key():
    if request.method == 'POST' and 'arguments' in request.form:
        req = json.loads(request.form['arguments'])
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    dat['key'] = "bksaoudu......aoelchsauh"
    return json.dumps(dat)

@app.route('/rest/activate_user', methods=('POST',))
def activate_user():
    # Try to handle as plaintext
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])

    # parse data out, return timestamp, and result
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data

@app.route('/rest/suspend_user', methods=['POST'])
def suspend_user():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    return  json.dumps(dat)

@app.route('/rest/list_products', methods=['POST'])
def list_products():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    cur = conn.cursor()
    cur.execute("SELECT vendor, description FROM products WHERE description = %s", [req['description']]);
    res = cur.fetchall()

    lis = []
    for r in res:
        products_data = dict()
        print (r)
        products_data['vendor'] = r[0]
        products_data['description'] = r[1]
        products_data['compartments'] = []
        lis.append(products_data)
    dat['listing'] = lis
    return json.dumps(dat)

@app.route('/rest/add_products', methods=['POST'])
def add_products():
    if request.method == 'POST' and 'arguments' in request.form:
        req = json.loads(request.form['arguments'])
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    dat['key'] = "bksaoudu......aoelchsauh"
    return json.dumps(dat)

@app.route('/rest/add_asset', methods=['POST'])
def add_asset():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    return json.dumps(dat)

@app.route('/report_filter')
def report_filter():
    # Get list of facilities for the option field
    cur.execute("SELECT common_name FROM facilities")
    res = cur.fetchall()
    facilities_data = []
    for r in res:
        facilities_data.append( dict(zip(('common_name'), r)))
    return render_template('report_filter.html', facilities_data=facilities_data)

@app.route('/facility_inventory_report', methods = ['GET', 'POST'])
def facility_inventory_report():
    # Select is the value that was passed from the option field used to query DB
    select = request.form.get('facility')
    cur.execute("SELECT facilities.common_name, assets.asset_tag, assets.description, asset_at.arrive_dt, asset_at.depart_dt FROM facilities, assets, asset_at WHERE assets.asset_pk=asset_at.asset_fk AND asset_at.facility_fk=facilities.facility_pk AND facilities.common_name = %s", [select])
    res = cur.fetchall()
    print (res)
    asset_data = []
    for r in res:
        asset_data.append( dict(zip(('common_name', 'asset_tag', 'description', 'arrive_dt', 'depart_dt'), r)))
    return render_template('facility_inventory_report.html', asset_data=asset_data)

@app.route('/in_transit_report')
def in_transit_report():
    cur = conn.cursor()
    cur.execute("SELECT convoys.request, convoys.depart_dt, convoys.arrive_dt, facilities.common_name FROM convoys, facilities WHERE convoys.dest_fk=facilities.facility_pk")
    res = cur.fetchall()
    transit_data = []
    for r in res:
        transit_data.append( dict(zip(('request', 'depart_dt', 'arrive_dt', common_name), r)))
    return render_template('in_transit_report.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
    main()
