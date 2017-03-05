from flask import Flask, render_template, request, session, redirect
from config import dbname, dbhost, dbport
import json
import psycopg2
from jinja2 import Template
import datetime
import time

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
                sql2 = "SELECT username FROM Login_info WHERE username = %s AND role = 'Logistics Officer';"
                cur.execute(sql2,(session['mytext'],))
                res2 = cur.fetchone()
                if res2 == None:
                    session['my_role'] = "Facility Officer"
                    return redirect('/dashboard')
                else:
                    session['my_role'] = "Logistics Officer"
                    return redirect('/dashboard')
    if request.method=='GET':
        return render_template('login.html')
#####################################################

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
            
            sql2 = "SELECT username FROM Login_info WHERE username = %s AND role = 'Logistics Officer';"
            cur.execute(sql2,(session['mytext'],))
            res2 = cur.fetchone()
            if res2 == None:
                session['my_role'] = "Facility Officer"
                return redirect('/dashboard')
            else:
                session['my_role'] = "Logistics Officer"
                return redirect('/dashboard')
        else:
            return redirect('/already_a_user')

    if request.method=='GET':
        return render_template('create_user.html')
##########################################################3

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
##############################################################

@app.route('/add_asset', methods=['POST','GET'])
def add_asset():
    if request.method=='POST' and 'text' in request.form:
        name = request.form['text']
        description = request.form['description']
        location =request.form['location']
        date = request.form['date']
        if len(name) < 17:
            session['text']=name
            session['description']=description
            session['location']=location
            session['date'] = date
        else:
            session['error'] = name
            return redirect('already_an_asset')
        sql = "SELECT asset_tag FROM Assets where asset_tag = %s;"
        cur.execute(sql,(name,))
        res = cur.fetchone()
        if res == None:
            sql2 = "SELECT facility_pk FROM facilities WHERE facility_fk = %s"
            cur.execute(sql2,(location,))
            facility_fk = cur.fetchone()
            new = "INSERT INTO Assets (asset_tag,description,current_location,arrived) VALUES (%s,%s,%s,%s);"
            cur.execute(new,(name,description,facility_fk,date))
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
        sql2 = "SELECT facility_fk FROM facilities;"
        cur.execute(sql2)
        res2 = cur.fetchall()
        session['fac_list'] = res2
        return render_template('add_asset.html',data=session['asset_list'])
##############################################################

@app.route('/dispose_asset', methods=['GET','POST'])
def dispose_asset():
    if session['my_role'] == "Facility Officer":
        return redirect('/classified')
    else:
        if request.method=='POST' and 'text' in request.form:
            name = request.form['text']
            date = request.form['date']
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
                    sql5 = "UPDATE Assets SET disposal_date = %s WHERE asset_tag = %s"
                    cur.execute(sql4,(name,))
                    conn.commit()
                    cur.execute(sql5,(date,name))
                    conn.commit()
                    return redirect('/dashboard')
                else:
                    return redirect('/already_disposed')
        if request.method=='GET':
            return render_template('dispose_asset.html')
#########################################################

@app.route('/asset_report', methods=['POST','GET'])
def asset_report():
    if request.method=='POST' and 'text' in request.form:
        facility = request.form['text']
        date = request.form['date']
        if len(facility) < 1:
            sql = "SELECT asset_tag, description, current_location, arrived, disposal_date FROM Assets WHERE arrived = %s"
            cur.execute(sql,(date,))
            session['report'] = cur.fetchall()
            return redirect('/asset_report')
        else:
            find_fac = "SELECT facility_pk FROM facilities WHERE facility_fk = %s"
            cur.execute(find_fac,(facility,))
            fac = cur.fetchone()
            sql2 = "SELECT asset_tag, description, current_location, arrived, disposal_date FROM Assets where current_location = %s AND arrived = %s"
            cur.execute(sql2,(fac,date))
            session['report'] = cur.fetchall()
            return redirect('/asset_report')
    if request.method=='GET':
            return render_template('asset_report.html',data=session['report'])
#############################################

@app.route('/transfer_req',methods=['POST','GET'])
def transfer_req():
    if request.method=="POST" and "destination" in request.form:
        dest = request.form['destination']
        asset_fac = request.form['asset_fac']
        asset = asset_fac[0]

        sql = "SELECT asset_pk FROM Assets WHERE asset_tag = %s;"
        cur.execute(sql,(asset,))
        asset_pk = cur.fetchone()
        sql4 = "SELECT login_pk FROM Login_info WHERE username = %s;"
        name = session['mytext']
        cur.execute(sql4,(name,))
        log_officer = cur.fetchone()
        sql5 = "SELECT facility_pk FROM facilities WHERE facility_fk = %s;"
        cur.execute(sql5,(dest,))
        destination = cur.fetchone()
        dat = datetime.date.today()
        date = str(dat.month)+'-'+str(dat.day)+'-'+str(dat.year)
        time = str(datetime.datetime.now().time())
        
        sql3 = "INSERT INTO request (log_officer,submit_date,submit_time,destination,asset) VALUES (%s,%s,%s,%s,%s);"
        cur.execute(sql3,(log_officer,date,time,destination,asset_pk))
        conn.commit()
        
        return redirect('dashboard')

    if request.method=="GET":
        if session['my_role'] == "Facility Officer":
            return redirect('/classified')
        else:
            sql2 = "SELECT asset_tag,facility_fk FROM Assets,facilities WHERE current_location=facility_pk;"
            cur.execute(sql2)
            session['asset_fac_list'] = cur.fetchall()
            return render_template('transfer_req.html',data=session['asset_list'])

@app.route('/approve_req')
def approve_req():
    return render_template('approve.html')

@app.route('/update_transit')
def update_transit():
    return render_template('update_transit.html')





@app.route('/dashboard', methods=['GET'])
def dashboard():
    session['report'] = ""
    if session['my_role'] == "Facility Officer":
        return render_template('dashboard_fac.html',data=session['mytext'])
    else:
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

@app.route('/invalid_request')
def invalid_request():
    return render_template('invalid_req.html',data=session['error'])

@app.route('/no_requests')
def no_requests():
    return render_template('no_req.html')

@app.route('/logout')
def logout():
    session['mytext']= ""
    return redirect('/login')
