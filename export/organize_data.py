#! /usr/bin/python3

import sys
import csv
import os



address_u = sys.argv[1] + '/users.csv'
address_f = sys.argv[1] + '/facilities.csv'
address_a = sys.argv[1] + '/assets.csv'
address_t = sys.argv[1] + '/transfers.csv'
new_rows = []

def users():
    with open(address_u,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=' ',quotechar='|')
        data = []
        title_row = ['username','password','role','active']
        data.append(title_row)
        whole = ''
        count = 0
        for row in reader:
            for i in row:
                whole += i
                whole += " "
            new_row = whole.split(',')
            data.append(new_row[1::])
            whole = ''
    with open(address_u,'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def facilities():
    with open(address_f,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=' ',quotechar='|')
        data = []
        title_row = ['fcode','common_name']
        data.append(title_row)
        whole = ''
        count = 0
        for row in reader:
            for i in row:
                whole += i
                whole += " "
            new_row = whole.split(',')
            reverse = new_row[1::]
            data.append(reverse[::-1])
            whole = ''
    with open(address_f,'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def assets():
    with open(address_a,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=' ',quotechar='|')
        data = []
        title_row = ['asset_tag','description','facility','acquired','disposed']
        data.append(title_row)
        whole = ''
        count = 0
        for row in reader:
            for i in row:
                whole += i
                whole += " "
            new_row = whole.split(',')
            data.append(new_row[1::])
            whole = ''
    with open(address_a,'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def transfers():
    with open(address_t,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=' ',quotechar='|')
        data = []
        title_row = ['asset_tag','request_by','request_dt','approve_by','approve_dt','source','destination','load_dt','unload_dt']
        data.append(title_row)
        whole = ''
        count = 0
        for row in reader:
            export = []
            for i in row:
                whole += i
                whole += " "
            n = whole.split(',')
            export = [n[10],n[1],n[3],n[2],n[5],None,n[9],n[7],n[8]]
            data.append(export)
            whole = ''
    with open(address_t,'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)








users()
facilities()
assets()
transfers()
