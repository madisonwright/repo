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
           # os.system('./test.sh '+str(dat[1]))
            sql = "INSERT INTO Login_info (username,password,role,active) VALUES (%s,%s,%s,%s);"
            #cur.execute(sql,(dat[1],dat[2],dat[3],dat[4]))
            #conn.commit()
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
            #os.system('./test.sh '+str(dat[1]))    
            sql2 = "INSERT INTO facilities (facility_fk,code) VALUES (%s,%s);"
            #cur.execute(sql2,(dat[1],dat[2],))
             #conn.commit()

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
            #os.system('./test.sh '+str(dat[1]))   
            sql3 = "INSERT INTO Assets (asset_tag,description,arrived,disposal_date) VALUES (%s,%s.%s,%s);"
        #cur.execute(sql3,(dat[1],dat[2],dat[3],dat[4],dat[5],))
        #conn.commit()

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
            #os.system('./test.sh '+str(dat[1]))
            sql4 = "INSERT INTO request (log_officer,fac_officer,submit_date,approved_date,load_time,unload_time,destination,asset) VALUES (%s,%s.%s,%s,%s,%s,%s,%s);"
            #cur.execute(sql4,(dat[1],dat[3],dat[2],dat[4],dat[7],dat[8],dat[6],dat[0],))
            #conn.commit()
            sql5 = "UPDATE request SET approved = 't' WHERE approved_date IS NOT NULL"
            #cur.execute(sql5)
            #conn.commit()

    return


users()
assets()
facilities()
transfers()

