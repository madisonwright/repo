from flask import Flask, render_template, request, session
from config import dbname, dbhost, dbport
import json
import psycopg2

app = Flask(__name__)
app.secret_key="hello"

conn = psycopg2.connect(dbname=dbname,host=dbhost,port=dbport)
cur = conn.cursor()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html',dbname=dbname,dbhost=dbhost,dbport=dbport)

@app.route('/report_filter_screen')
def rfs(): 
    return render_template('rfs.html',data=request.args.get('mytext'))

@app.route('/facility_inventory_report')
def fir():
    usr_input = request.args.get('mytext2')
    mid = usr_input.split(',')
    sql = "SELECT " + mid[0] + " FROM asset_at"
    if len(mid)>1:
        sql += "WhERE arrive_dt = " + "'" + mid[1] + "'" +";"
    else:
        sql += ";"
    cur.execute(usr_input)
    res = cur.fetchall()
    session["result"]=res
    return render_template('fir.html')

@app.route('/in_transit_report')
def itr():
    usr_input = request.args.get('mytext3')
    mid = usr_input.split(',')
    sql = "SELECT " + mid[0] + " FROM asset_on"
    if len(mid)>1:
        sql += "WhERE convoy_fk = " + "'" + mid[1] + "'" +";"
    else:
        sql += ";"
    cur.execute(usr_input)
    res = cur.fetchall()
    session["result2"]=res
    return render_template('itr.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/rest')
def rest():
    return render_template('rest.html')

@app.route('/rest/lost_key', methods=('POST',))
def lost_key():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data


@app.route('/rest/activate_user', methods=('POST',))
def activate_user():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data

@app.route('/rest/suspend_user', methods=('POST',))
def suspend_user():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data

@app.route('/rest/list_products', methods=('POST',))
def list_products():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data


@app.route('/rest/add_products', methods=('POST'))
def add_products():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data


@app.route('/rest/add_assets', methods=('POST'))
def add_assets():
    if request.method=='POST' and 'arguments' in request.form:
        req=json.loads(request.form['arguments'])
    dat = dict()
    dat['timestamp'] = req['timestamp']
    dat['result'] = 'OK'
    data = json.dumps(dat)
    return data





