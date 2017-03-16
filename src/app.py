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
    return redirect('/login')
    #return render_template('index.html',dbname=dbname, dbhost=dbhost,dbport=dbport)

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
            sql = "SELECT username FROM login_info WHERE username = %s AND password = %s AND active = 't';"
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

@app.route('/activate_user', methods=['POST','GET'])
def activate_user():
    if request.method=='POST' and 'mytext' in request.form:
        name = request.form['mytext']
        password = request.form['pass']
        role = request.form['role']
        active ='t'
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
        print('bb')
        cur.execute(sql,(name,))
        res = cur.fetchone()
        if res == None:
            new = "INSERT INTO login_info (username, password, role, active) VALUES (%s,%s,%s,%s);"
            cur.execute(new,(name,password,role,active,))
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
            sql3 = "UPDATE Login_info SET (password,active) = (%s,%s) WHERE username = %s"
            cur.execute(sql3,(password,active,name,))
            conn.commit()
            sql4 = "SELECT username FROM Login_info WHERE username = %s AND role = 'Logistics Officer';"
            cur.execute(sql4,(session['mytext'],))
            res3 = cur.fetchone()
            if res3 == None:
                session['my_role'] = "Facility Officer"
                return redirect('/dashboard')
            else:
                session['my_role'] = "Logistics Officer"
                return redirect('/dashboard')
    if request.method=='GET':
        return render_template('create_user.html')
###########################################################
@app.route('/revoke_user', methods=['POST','GET'])
def revoke_user():
    if request.method=='POST' and 'mytext' in request.form:
        name = request.form['mytext']
        sql = "SELECT username FROM Login_info WHERE username = %s;"
        cur.execute(sql,(name,))
        res = cur.fetchone()
        if res == None:
            return redirect('/dashboard')
        sql2 = "UPDATE Login_info SET active = 'f' WHERE username = %s;"
        cur.execute(sql2,(name,))
        conn.commit()
        return redirect('dashboard')

    if request.method=='GET':
        return render_template('revoke_user.html')


###########################################################
@app.route('/add_facility', methods=['POST','GET'])
def add_facility():
    if request.method=='POST' and 'text' in request.form:
        name = request.form['text']
        fcode = request.form['fcode']
        if len(name) < 33:
            if len(fcode) < 7:
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
        nam = "Disposed"
        sqlx = "SELECT facility_pk FROM facilities WHERE facility_fk = %s;"
        cur.execute(sqlx,(nam,))
        resul = cur.fetchone()
        if resul == None:
            session['disposed'] = None
        else:
            sqly = "SELECT facility_pk FROM facilities WHERE facility_fk = %s;"
            cur.execute(sqly,(nam,))
            session['disposed'] = cur.fetchone()
        sql = "SELECT asset_tag FROM Assets WHERE current_location != %s;"
        cur.execute(sql,(session['disposed'],))
        res = cur.fetchall()
        session['asset_list'] = res
        sql2 = "SELECT facility_fk FROM facilities WHERE facility_fk != %s;"
        nam = 'Disposed'
        cur.execute(sql2,(nam,))
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
                sqlz = "SELECT facility_pk FROM facilities WHERE facility_fk = %s;"
                nam = 'Disposed'
                cur.execute(sqlz,(nam,))
                session['disposed'] = cur.fetchone()

                if session['disposed'] == None:
                    sqlx = "INSERT INTO facilities (facility_fk,fcode) VALUES (%s,%s);"
                    dis = "Disposed"
                    code = 666666
                    cur.execute(sqlx,(dis,code))
                    conn.commit()

                sqly = "SELECT facility_pk FROM facilities WHERE facility_fk = %s;"
                cur.execute(sqly,(nam,))
                disp_pk = cur.fetchone()

                sql3 = "SELECT asset_tag FROM Assets WHERE asset_tag = %s AND current_location = %s;"
                cur.execute(sql3,(name,session['disposed'],))
                res3 = cur.fetchone()

                
                if res3 == None:
                    sql4 = "UPDATE Assets SET current_location = %s WHERE asset_tag = %s"
                    sql5 = "UPDATE Assets SET disposal_date = %s WHERE asset_tag = %s"
                    cur.execute(sql4,(session['disposed'],name,))
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
        session['bug'] = asset_fac.split(',')[0][1::].strip("'")
        asset=session['bug']
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
        boole = False
        sql3 = "INSERT INTO request (log_officer,submit_date,submit_time,destination,asset,approved) VALUES (%s,%s,%s,%s,%s,%s);"
        cur.execute(sql3,(log_officer,date,time,destination,asset_pk,boole))
        conn.commit()        
        return redirect('/request_made')

    if request.method=="GET":
        if session['my_role'] == "Facility Officer":
            return redirect('/classified')
        else:
            sql2 = "SELECT asset_tag,facility_fk FROM Assets,facilities WHERE current_location=facility_pk AND facility_pk != %s;"
            cur.execute(sql2,(session['disposed'],))
            session['asset_fac_list'] = cur.fetchall()
            return render_template('transfer_req.html',data=session['asset_list'])
#####################################################
@app.route('/approve_req', methods=['GET','POST'])
def approve_req():
    if request.method=="POST" and "accept" in request.form:
        request_num = request.form['request'] 
        dat = datetime.date.today()
        date = str(dat.month)+'-'+str(dat.day)+'-'+str(dat.year)
        time = str(datetime.datetime.now().time())
        boole = True;
        sql14 = "SELECT login_pk FROM Login_info WHERE username = %s"
        cur.execute(sql14,(session['mytext'],))
        name = cur.fetchone()
        sql11= "UPDATE request SET (approved_date,approved_time,approved,fac_officer) = (%s,%s,%s,%s) WHERE request_pk = %s;"
        cur.execute(sql11,(date,time,boole,name,request_num))
        conn.commit()

        return redirect('dashboard')

    if request.method=="POST" and "deny" in request.form:
        request_num = request.form['request']
        sql10 = "DELETE FROM request WHERE request_pk = %s;"
        cur.execute(sql10,(request_num,))
        conn.commit()
        return redirect('dashboard')

    if request.method=="GET":
        if session['my_role'] == "Logistics Officer":
            return redirect('/classified')
        else:
            sql = "SELECT * FROM request;"
            cur.execute(sql)
            res = cur.fetchone()
            if res == None:
                return redirect('/no_requests')
            else:
                asset_list = []
                current_loc_list = []
                destination_list = []
                request_num_list = []

                sql9 = "SELECT request_pk FROM request WHERE approved = 'f';"
                cur.execute(sql9)
                requests = cur.fetchall()
                for item2 in requests:
                    request_num_list.append(item2)
                
                sql3 = "SELECT asset FROM request WHERE approved = 'f';"
                cur.execute(sql3)
                assets = cur.fetchall()
                for item in assets:
                    sql6 = "SELECT asset_tag FROM Assets WHERE asset_pk = %s AND current_location != %s;"
                    cur.execute(sql6,(item,session['disposed'],))
                    asset_list.append(cur.fetchone())
                    
                    sql7 = "SELECT current_location FROM Assets WHERE asset_pk = %s AND current_location != %s;"
                    cur.execute(sql7,(item,session['disposed'],))
                    fac = cur.fetchone()
                    sql13 = "SELECT facility_fk FROM facilities WHERE facility_pk = %s AND facility_fk != 'Disposed';"
                    cur.execute(sql13,(fac,))
                    current_loc_list.append(cur.fetchone())

                sql4 = "SELECT destination from request WHERE approved = 'f';"
                cur.execute(sql4)
                destinations = cur.fetchall()
                for item3 in destinations:
                    sql8 = "SELECT facility_fk FROM facilities WHERE facility_pk = %s;"
                    cur.execute(sql8,(item3,))
                    destination_list.append(cur.fetchone())

                request_list = []
                reques = ''
                for i in range(len(asset_list)):
                    reques = "request number: " + str(request_num_list[i]) + "    " + str(asset_list[i]) + " at location: " + str(current_loc_list[i]) + " requested to be moved to: " + str(destination_list[i])
                    request_list.append(reques)
                session['request_list'] = request_num_list
                return render_template('approve.html',data=request_list)
#######################################################

@app.route('/update_transit',methods=['GET','POST'])
def update_transit():
    if request.method=="POST" and "request_num" in request.form:
        num = request.form['request_num']
        load = request.form['load']
        unload = request.form['unload']
        sql4 = "UPDATE request SET (load_time,unload_time) = (%s,%s) WHERE request_pk = %s;"
        cur.execute(sql4,(load,unload,num,))
        conn.commit()
        return redirect('dashboard')

    if request.method=="GET":
        if session['my_role'] == "Facility Officer":
            return redirect('/classified')
        else:
            approved_req_list = []
            approved_req_num = []
            sql = "SELECT * FROM request WHERE approved = 't' AND load_time IS NULL;"
            cur.execute(sql)
            approved = cur.fetchall()
            if len(approved) < 1:
                return redirect('/no_requests')
            for item in approved:
                asset = item[10]
                destination = item[9]
                req_num = item[0]
                sql2 = "SELECT asset_tag FROM Assets WHERE asset_pk = %s"
                sql3 = "SELECT facility_fk FROM facilities WHERE facility_pk = %s"
                cur.execute(sql2,(asset,))
                asset_name = cur.fetchone()
                cur.execute(sql3,(destination,))
                dest = cur.fetchone()
                approved_req = "Request number: " + str(req_num) + "  Asset: " + str(asset_name) + " approved to travel to destination: " + str(dest)
                approved_req_list.append(approved_req)
                approved_req_num.append(item[0])
            session['approved_req_list'] = approved_req_list
            session['approved_req_num'] = approved_req_num
            


            return render_template('update_transit.html',data=session['approved_req_list'])





@app.route('/dashboard', methods=['GET'])
def dashboard():
    session['report'] = ""
    if session['my_role'] == "Facility Officer":
        sql = "SELECT request_pk FROM request WHERE approved = %s;"
        boole = False
        cur.execute(sql,(boole,))
        res = cur.fetchall()
        length = len(res)
        session['requests'] = length
        return render_template('dashboard_fac.html',data=session['mytext'],data2=session['requests'])
    else:
        sql2 = "SELECT request_pk FROM request WHERE approved = 't' AND load_time IS NULL;"
        cur.execute(sql2)
        res2 = cur.fetchall()
        length2 = len(res2)
        session['req_updates'] = length2
        return render_template('dashboard.html',data=session['mytext'],data2=session['req_updates'])

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
    return render_template('classified.html', data=session['mytext'],data2=session['my_role'])

@app.route('/request_made')
def request_made():
    return render_template('request_made.html')

@app.route('/no_requests')
def no_requests():
    return render_template('no_requests.html')

@app.route('/logout')
def logout():
    session['mytext']= ""
    return redirect('/login')
