from flask import Flask, render_template, request, session
from config import dbname, dbhost, dbport
import sys
import psycopg2
import json

app = Flask(__name__)
SECRET_KEY = 'this_is_my_fake_key'
app.secret_key = SECRET_KEY

def exists(username):
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE username=%s",(username,))
    return (cur.fetchone() is not None)
    
def valid_username(username, password):
    if (len(username) <= 16 and len(password) <= 16):
        conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)",(username, password))
        conn.commit()
        return True
    else:
        return False

def check_password(username, password):
    conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
    cur = conn.cursor()
    cur.execute("SELECT password  FROM users WHERE username=%s AND password = %s",(username,password))
    return (cur.fetchone() is not None)

@app.route('/create_user', methods = ['POST','GET'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if exists(username):
            return render_template('username_exists.html')
        elif valid_username(username, password):
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
            return dashboard()
        else:
            return render_template('invalid_login.html')

@app.route('/dashboard', methods = ['GET'])
def dashboard():
    return render_template('dashboard.html', username = session['username'])

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
