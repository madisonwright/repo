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
    return render_template('index.html',dbname=dbname, dbhost=dbhost,dbport=dbport)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        name = request.form['mytext']
        password = request.form['pass']



        session["user"]=name
        return render_template('dashboard.html',data=session.user)

    if request.method=='GET':
        return render_template('login.html')

    return render_template('index.html')

@app.route('/create_user', methods=['POST','GET'])
def create_user():
    #if request.method=='POST' and 'arguments' in request.form:
    #    req=json.loads(request.form['arguments'])
    #dat = dict()
    #dat['timestamp'] = req['timestamp']
    #dat['result'] = 'OK'
   # data = json.dumps(dat)
   # return data
    if request.method=='POST':
        name = request.form['mytext']
        password = request.form['pass']



        session["user"]=name
        return render_template('dashboard.html',data=session.user)
    if request.method=='GET':
        return render_template('create_user.html')


@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    return render_template('dashboard.html',data=request.args.get('mytext'))



