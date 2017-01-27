from flask import Flask, render_template, request, session
from config import dbname, dbhost, dbport
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


