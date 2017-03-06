import psycopg2
import sys
import csv

conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=5432)
cur = conn.cursor()



def users():
    #assuming we download the csv files with the git pull, and into a dir called data
    with open('$HOME/repo/data/users.csv','r') as csvfile:
        reader = csv.reader(csvfile,delimiter=' ',quotechar='|')

        #get the data clean

        #psql cur.execute statements to insert the data
        #currently ignore last csv bit because it is user active/not active which I don't have yet
        sql = "INSERT INTO Login_info (username,password,role) VALUES (%s,%s,%s);"
        cur.execute(sql,(1,2,3,))
        conn.commit()

    return


def facilities():
    with open('$HOME/repo/data/facilities.csv','r') as csvfile:
        reader = csv.reader(csvfile,delimiter=' ',quotechar='|')

        #get the data clean

        #psql cur.execute statements to insert the data
        #cvs file should be fcode then common name? so 2 then 1
        sql2 = "INSERT INTO facilities (facility_fk,code) VALUES (%s,%s);"
        cur.execute(sql2,(2,1,))
        conn.commit()

    return


idef Assets():
    with open('$HOME/repo/data/assets.csv','r') as csvfile:
        reader = csv.reader(csvfile,delimiter=' ',quotechar='|')

        #get the data clean

        #psql cur.execute statements to insert the data
        #all in order with assginment and my table
        sql2 = "INSERT INTO Assets (asset_tag,description,current_location,arrived,disposal_date) VALUES (%s,%s.%s,%s,%s);"
        cur.execute(sql2,(1,2,3,4,5,))
        conn.commit()

    return


def Transfers():
    with open('$HOME/repo/data/transfers.csv','r') as csvfile:
        reader = csv.reader(csvfile,delimiter=' ',quotechar='|')

        #get the data clean

        #psql cur.execute statements to insert the data
        #if not all cells are filled, I'll probably have to do this one column or row at a time and fill in what's provided
            #remember to use update after the first insert
        sql2 = "INSERT INTO request (log_officer,fac_officer,submit_date,submit_time,approved_date,approved_time,load_time,unload_time,destination,asset,approved) VALUES (%s,%s.%s,%s,%s);"
        cur.execute(sql2,(1,2,3,4,5,6,7,8,9,10,11,))
        conn.commit()

    return


