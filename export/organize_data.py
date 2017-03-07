#! /usr/bin/python3

import sys
import csv



address = str(sys.argv[1]) + '/users.csv'
new_rows = []

def users():
    with open(address,'rb') as csvfile:
        #reader = csv.reader(csvfile,delimiter=' ',quotechar='|')
        reader = csv.reader(csvfile)
        for row in reader:
            new_rows.append(row[2])
            new_rows.append(row[3])
            new_rows.append(row[4])
            new_rows.append(row[5])

    with open(adderess,'wb') as csvfile:
        writer = csv.writer(csvfiel)
        writer.writerrows(new_rows)

