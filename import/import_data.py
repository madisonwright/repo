#! /usr/bin/python3

import psycopg2
import sys
import csv
import os

conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=5432)
cur = conn.cursor()

#os.system("./test.sh first")


address_u = sys.argv[2] + '/users.csv'
address_f = sys.argv[2] + '/facilities.csv'
address_a = sys.argv[2] + '/assets.csv'
address_t = sys.argv[2] + '/transfers.csv'


def users():
    with open(address_u,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=' ',quotechar='|')
        data = []
        whole = ''
        count = 0
        for row in reader:
            if count > 0:
                for i in row:
                    whole += i
                    whole += " "
                new_row = whole.split(',')
                data.append(new_row)
                whole = ''
            count+=1
        for dat in data:
            sql = "INSERT INTO Login_info (username,password,role,active) VALUES (%s,%s,%s,%s);"
            cur.execute(sql,(dat[0],dat[1],dat[2],dat[3]))
            conn.commit()
    return  

def facilities():
    with open(address_f,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=' ',quotechar='|')
        data = []
        whole = ''
        count = 0
        for row in reader:
            if count > 0:
                for i in row:
                    whole += i
                    whole += " "
                new_row = whole.split(',')
                data.append(new_row)
                whole = ''
            count+=1
        for dat in data:   
            sql2 = "INSERT INTO facilities (facility_fk,code) VALUES (%s,%s);"
            cur.execute(sql2,(dat[1],dat[0],))
            conn.commit()
    return


def assets():
    with open(address_a,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=' ',quotechar='|')
        data = []
        whole = ''
        count = 0
        for row in reader:
            if count > 0:
                for i in row:
                    whole += i
                    whole += " "
                new_row = whole.split(',')
                data.append(new_row)
                whole = ''
            count+=1
        for dat in data:   
            sql3 = "INSERT INTO Assets (asset_tag,description,arrived,disposal_date) VALUES (%s,%s,%s,%s);"
            cur.execute(sql3,(dat[0],dat[1],str(dat[3]),str(dat[4]),))
            conn.commit()
    return

def transfers():
    with open(address_t,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=' ',quotechar='|')
        data = []
        whole = ''
        count = 0
        for row in reader:
            if count > 0:
                for i in row:
                    whole += i
                    whole += " "
                new_row = whole.split(',')
                data.append(new_row)
                whole = ''
            count+=1
        for dat in data:
            sql4 = "INSERT INTO request (log_officer,fac_officer,submit_date,submit_time,approved_date,approved_time,load_time,unload_time,destination,asset) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            sql5 = "SELECT facility_pk FROM facilities WHERE code = %s"
            sql6 = "SELECT login_pk FROM Login_info WHERE username = %s"
            sql7 = "SELECT asset_pk FROM Assets WHERE asset_tag = %s"
            cur.execute(sql5,(dat[6],))
            dest = cur.fetchone()
            cur.execute(sql6,(dat[1],))
            user1 = cur.fetchone()
            cur.execute(sql6,(dat[3],))
            user2 = cur.fetchone()
            cur.execute(sql7,(str(dat[0]),))
            asset = cur.fetchone()
            sub_dt = str(dat[2]).split(' ')
            app_dt = str(dat[4]).split(' ')
            cur.execute(sql4,(user1,user2,sub_dt[0],sub_dt[1],app_dt[0],app_dt[1],str(dat[7]),str(dat[8]),dest,asset,))
            conn.commit()
            sql5 = "UPDATE request SET approved = 't' WHERE approved_date IS NOT NULL"
            cur.execute(sql5)
            conn.commit()
    return


users()
facilities()
assets()
transfers()

