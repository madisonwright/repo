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

@app.route('/add_facility', methods=['POST','GET'])
def add_facility():
    if request.method=='POST' and 'text' in request.form:
        name = request.form['text']
        fcode = request.form['fcode']
        if len(name) < 33:
            if len(fcode) < 77:
                session['text']=name
                session['code']=fcode
            else:
                session['error'] = fcode
                return redirect('already_a_facility')
        else:
            session['error'] = name
            return redirect('already_a_facility')

        sql = "SELECT facility_fk FROM facilities where facility_fk = %s;"
        cur.execute(sql,(name,))
        res = cur.fetchone()
        if res == None:
            sql2 = "SELECT code FROM facilities where code = %s;"
            cur.execute(sql2,(fcode,))
            res2 = cur.fetchone()
            if res2 == None:
                new = "INSERT INTO facilities (facility_fk, code) VALUES (%s,%s);"
                cur.execute(new,(name,fcode,))
                conn.commit()
                return redirect('/add_facility') 
            else:
                session['error'] = fcode
                return redirect('/already_a_facility')
        else:
            session['error'] = res
            return redirect('/already_a_facility')
        return redirect('/login')
    if request.method=='GET':
        sql = "SELECT facility_fk FROM facilities;"
        cur.execute(sql)
        res = cur.fetchall()
        session['facilities_list'] = res
        return render_template('add_facility.html',data=session['facilities_list'])

@app.route('/add_asset', methods=['POST','GET'])
def add_asset():
    if request.method=='POST' and 'text' in request.form:
        name = request.form['text']
        description = request.form['description']
        location =request.form['location']
        if len(name) < 17:
            session['text']=name
            session['description']=description
            session['location']=location
        else:
            session['error'] = name
            return redirect('already_an_asset')
        sql = "SELECT asset_tag FROM Assets where asset_tag = %s;"
        cur.execute(sql,(name,))
        res = cur.fetchone()
        if res == None:
            new = "INSERT INTO Assets (asset_tag,description,current_location) VALUES (%s,%s,%s);"
            cur.execute(new,(name,description,location,))
            conn.commit()
            return redirect('/add_asset') 
        else:
            session['error'] = name
            return redirect('/already_an_asset')
        session['error'] = request.form['text']
        return redirect('/already_an_asset')
    if request.method=='GET':
        sql = "SELECT asset_tag FROM Assets;"
        cur.execute(sql)
        res = cur.fetchall()
        session['asset_list'] = res
        return render_template('add_asset.html',data=session['asset_list'])

@app.route('/dispose_asset', methods=['GET','POST'])
def dispose_asset():
    sql = "SELECT username FROM Login_info WHERE username = %s AND role = 'Logistics Officer';"
    cur.execute(sql,(session['mytext'],))
    res = cur.fetchone()
    if res == None:
        return redirect('/classified')
    else:
        if request.method=='POST' and 'text' in request.form:
            name = request.form['text']
            sql2 = "SELECT asset_tag FROM Assets WHERE asset_tag = %s;"
            cur.execute(sql2,(name,))
            res2 = cur.fetchone()
            if res2 == None:
                return redirect('/not_an_asset')
            else:
                sql3 = "SELECT asset_tag FROM Assets WHERE asset_tag = %s AND current_location = 3;"
                cur.execute(sql3,(name,))
                res3 = cur.fetchone()
                if res3 == None:
                    sql4 = "UPDATE Assets SET current_location = 3 WHERE asset_tag = %s"
                    #sql5 = "UPDATE Assets SET date = %s WHERE asset_tag = %s"
                    cur.execute(sql4,(name,))
                    conn.commit()
                    return redirect('/dashboard')
                else:
                    return redirect('/already_disposed')
        if request.method=='GET':
            return render_template('dispose_asset.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html',data=session['mytext'])

@app.route('/not_a_user')
def not_a_user():
    return render_template('not_a_user.html', data=session['mytext'])

@app.route('/not_an_asset')
def not_an_asset():
    return render_template('not_an_asset.html',data=session['text'])

@app.route('/already_a_user')
def already_a_user():
    return render_template('already_user.html', data=session['mytext'])

@app.route('/already_a_facility')
def already_a_facility():
    return render_template('already_a_facility.html', data=session['error'])

@app.route('/already_an_asset')
def already_an_asset():
    return render_template('already_an_asset.html', data=session['error'])

@app.route('/already_disposed')
def already_disposed():
    return render_template('already_disposed.html',data=session['text'])

@app.route('/classified')
def classified():
    return render_template('classified.html', data=session['mytext'])


