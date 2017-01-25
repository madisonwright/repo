#! /usr/bin/python3
import psycopg2
import sys
import csv

print(sys.argv)
conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()
diction = dict()


def products():
	with open('/home/osnapdev/repo/sql/osnap_legacy/product_list.csv','r') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
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
			#vendor, description, alt_description
			cur.execute("INSERT INTO products (vendor, description, alt_description) VALUES (%s,%s,%s)",(dat[4],dat[2],dat[0]))
			cur.execute("SELECT product_pk FROM products WHERE vendor=%s",(dat[4],))
			diction[dat[4],dat[2],dat[0]] = cur.fetchone()[0]
			
		print(diction)
	return




def make_products():
	with open('/home/osnapdev/repo/sql/osnap_legacy/product_list.csv','r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in spamreader:
			first = row[0]
			first_list = first.split(',')
			
			print(first_list[0])
			if first_list[0] != 'name':
				print(first_list[0])  #here the list is slilt at we see only the name column
				cur.execute("INSERT INTO products (description) VALUES (%s)",(first_list[0],))
				cur.execute("SELECT product_pk FROM products WHERE description=%s",(first_list[0],))
				diction[first_list[0]] = cur.fetchone()[0]
	
	return

#make_products()
products()

conn.commit()
"""productpk = row[0]
	    	vendr = row[5]
	    	desc = row[3]
	    	alt_desc = row[2]
	    	#use the cur.execute to input this data into the database
	    	#I don't know where rolename came from in the example code
	    	#find the equivalent for the asset table
			#cur.execute("INSERT INTO roles (rolename) VALUES (%s)",(role,))
			#cur.execute("SELECT role_pk FROM roles WHERE rolename=%s",(role,))
			#roles[role] = cur.fetchone()[0]
	with open('/home/osnapdev/repo/sql/osnap_legacy/?asset_at?.csv','r') as csvfile:
		spamreader2 = csv.reader(csvfile, delimiter=' ', quotechar='|')
	    for roww in spamreader2:
	    	assefk = roww[]
	    	facilfk = roww[]
	    	arrive = roww[]
	    	depart = row[]
	    	#do like above but for the asset_at table

	with open('/home/osnapdev/repo/sql/osnap_legacy/?facilities?.csv','r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	    for rowa in spamreader:
	    	facilpk = rowa[]
	    	fcod = rowa[]
	    	commnom = rowa[]
	    	loca = rowa[]
	    	#do like above but for the facility table

	#don't know if I'm supposed to do this once or after every execute
	conn.commit()

	#clean up the work
	cur.close()
	conn.clow()
	#end the program
	return





	#extrafor later

		#reader = csv.DictReader(csvfile)
		#for row in reader:	
		#	name = row['name']
		#	print(name)
		#	unit_price = row['unit price']
		#	print(unit_price)
		#	cur.execute("INSERT INTO roles (rolename) VALUES (%s)",(role,))
		#	cur.execute("SELECT role_pk FROM roles WHERE rolename=%s",(role,))
		#	roles[role] = cur.fetchone()[0]


"""