from flask import Flask, render_template, request, session, redirect
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
    if request.method=='POST' and 'mytext' in request.form:
        name = request.form['mytext']
        password = request.form['pass']
        session['mytext']=name
        session['pass']=password
        
        sql = "SELECT username FROM login_info WHERE username = %s;"
        cur.execute(sql,(name,))
        res = cur.fetchone()
        if res == None:
            return redirect('/not_a_user')
        else:
            sql = "SELECT username FROM login_info WHERE username = %s AND password = %s"
            cur.execute(sql,(name,password))
            res = cur.fetchone()
            if res == None:
                return redirect('/not_a_user')
            else:
                return redirect('/dashboard')


    if request.method=='GET':
        return render_template('login.html')


@app.route('/create_user', methods=['POST','GET'])
def create_user():
    if request.method=='POST' and 'mytext' in request.form:
        name = request.form['mytext']
        password = request.form['pass']
        role = request.form['role']
        if len(name) < 17:
            if len(password) < 17:
                session['mytext']=name
                session['pass']=password
                session['role']=role
            else:
                return redirect('already_a_user')
        else:
            return redirect('already_a_user')


        sql = "SELECT username FROM login_info WHERE username = %s;"
        cur.execute(sql,(name,))
        res = cur.fetchone()
        if res == None:
            new = "INSERT INTO login_info (username, password, role) VALUES (%s,%s,%s);"
            cur.execute(new,(name,password,role,))
            conn.commit()
            return redirect('/dashboard')
        else:
            return redirect('/already_a_user')

    if request.method=='GET':
        return render_template('create_user.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html',data=session['mytext'])

@app.route('/not_a_user')
def not_a_user():
    return render_template('not_a_user.html', data=session['mytext'])

@app.route('/already_a_user')
def already_a_user():
    return render_template('already_user.html', data=session['mytext'])


