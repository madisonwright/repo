#! /usr/bin/python3

import sys
import csv
import os



address = sys.argv[1] + '/users.csv'
new_rows = []

def users():
    with open(address,'r') as csvfile:
        reader = csv.reader(csvfile,delimiter=' ',quotechar='|')
        #reader = csv.reader(csvfile)
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

    with open(address,'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

users()
