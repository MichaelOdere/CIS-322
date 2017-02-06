from flask import Flask, render_template, request
from config import dbname, dbhost, dbport
import sys
import psycopg2

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

@app.route('/report_filter')
def report_filter():
    cur.execute("SELECT common_name FROM facilities")
    res = cur.fetchall()
    facilities_data = []
    for r in res:
        facilities_data.append( dict(zip(('common_name'), r)))
    return render_template('report_filter.html', facilities_data=facilities_data)

@app.route('/facility_inventory_report', methods = ['GET', 'POST'])
def facility_inventory_report():
   
    select = request.form.get('facility')
    # The below dates would be used if my db had dates
    #date_begin = request.form.get('date_begin')
    #date_end = request.form.get('date_end')
    cur.execute("SELECT facilities.common_name, assets.asset_tag, assets.description, asset_at.arrive_dt, asset_at.depart_dt FROM facilities, assets, asset_at WHERE assets.asset_pk=asset_at.asset_fk AND asset_at.facility_fk=facilities.facility_pk AND facilities.common_name = %s", [select])
    res = cur.fetchall()
    print (res)
    asset_data = []
    for r in res:
        asset_data.append( dict(zip(('common_name', 'asset_tag', 'description', 'arrive_dt', 'depart_dt'), r)))
    return render_template('facility_inventory_report.html', asset_data=asset_data)

@app.route('/in_transit_report')
def in_transit_report():
    return render_template('in_transit_report.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
    main() 
