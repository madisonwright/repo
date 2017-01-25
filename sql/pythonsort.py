#! /usr/bin/python3
import psycopg2
import sys
import csv

print(sys.argv)
conn = psycopg2.connect(dbname=sys.argv[1],host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()
diction = dict()
product_list_data = []
acquisitions_data = []
convoy_data = []
DC_inventory_data = []
HQ_inventory_data = []
MB005_inventory_data = []
SPNV_inventory_data = []
NC_inventory_data = []
security_compartments_data = []
security_levels_data = []
transit_data = []
vendor_data = []






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

def assets():
	#asset_pk
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

		productfk = diction()
		for dat in data:
			#product_fk, asset_tag, description,alt_description
			cur.execute("INSERT INTO assets (product_fk, asset_tag, description,alt_description) VALUES (%s,%s,%s,%s)",(dat[4],dat[2],dat[0]))
			cur.execute("SELECT asset_pk FROM assets WHERE asset_tag=%s",(dat[4],))
			diction[dat[4],dat[2],dat[0]] = cur.fetchone()[0]
		
	return
def vehicles():
	#vehicle_pk
	#asset_fk
	return
def facilities():
	#facility_pk
	#fcode, common_name, location
	return
def asset_at():
	#asset_fk,facility_fk,arrive_dt,depart_dt
	return
def convoys():
	#convoy_pk
	#request, source_fk, dest_fk, depart2_dt, arrive2_dt
	return
def used_by():
	#vehicle_fk, convoy_fk
	return
def asset_on():
	#asset_fk, convoy_fk, load_dt, unload_dt
	return
def users():
	#user_pk
	#username, active
	return
def roles():
	#role_pk
	#title
	return
def user_is():
	#user_fk, role_fk
	return
def user_supports():
	#user_fk, facility_fk
	return
def levels():
	#level_pk
	#abbrv, comment
	return
def compartments():
	#compartment_pk
	#abbrv, comment
	return
def security_tags():
	#tag_pk
	#level_fk, compartment_fk, user_fk, products_fk, asset_fk
	return

def open_files():

	with open('/home/osnapdev/repo/sql/osnap_legacy/product_list.csv','r') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		whole = ''
		count = 0
		for row in reader:
			if count > 0:
				for i in row:
					whole += i
					whole += " "
				new_row = whole.split(',')
				product_list_data.append(new_row)
				whole = ''
			count+=1
	with open('/home/osnapdev/repo/sql/osnap_legacy/acquisitions.csv','r') as csvfile:
			reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			whole = ''
			count = 0
			for row in reader:
				if count > 0:
					for i in row:
						whole += i
						whole += " "
					new_row = whole.split(',')
					acquisitions_data.append(new_row)
					whole = ''
				count+=1
	with open('/home/osnapdev/repo/sql/osnap_legacy/convoy.csv','r') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		whole = ''
		count = 0
		for row in reader:
			if count > 0:
				for i in row:
					whole += i
					whole += " "
				new_row = whole.split(',')
				convoy_data.append(new_row)
				whole = ''
			count+=1
	with open('/home/osnapdev/repo/sql/osnap_legacy/DC_inventory.csv','r') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		whole = ''
		count = 0
		for row in reader:
			if count > 0:
				for i in row:
					whole += i
					whole += " "
				new_row = whole.split(',')
				DC_inventory_data.append(new_row)
				whole = ''
			count+=1
	with open('/home/osnapdev/repo/sql/osnap_legacy/HQ_inventory.csv','r') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		whole = ''
		count = 0
		for row in reader:
			if count > 0:
				for i in row:
					whole += i
					whole += " "
				new_row = whole.split(',')
				HQ_inventory_data.append(new_row)
				whole = ''
			count+=1
	with open('/home/osnapdev/repo/sql/osnap_legacy/MB005_inventory.csv','r') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		whole = ''
		count = 0
		for row in reader:
			if count > 0:
				for i in row:
					whole += i
					whole += " "
				new_row = whole.split(',')
				MB005_inventory_data.append(new_row)
				whole = ''
			count+=1
	with open('/home/osnapdev/repo/sql/osnap_legacy/NC_inventory.csv','r') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		whole = ''
		count = 0
		for row in reader:
			if count > 0:
				for i in row:
					whole += i
					whole += " "
				new_row = whole.split(',')
				NC_inventory_data.append(new_row)
				whole = ''
			count+=1
	with open('/home/osnapdev/repo/sql/osnap_legacy/SPNV_inventory.csv','r') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		whole = ''
		count = 0
		for row in reader:
			if count > 0:
				for i in row:
					whole += i
					whole += " "
				new_row = whole.split(',')
				SPNV_inventory_data.append(new_row)
				whole = ''
			count+=1
	with open('/home/osnapdev/repo/sql/osnap_legacy/security_compartments.csv','r') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		whole = ''
		count = 0
		for row in reader:
			if count > 0:
				for i in row:
					whole += i
					whole += " "
				new_row = whole.split(',')
				security_compartments_data.append(new_row)
				whole = ''
			count+=1
	with open('/home/osnapdev/repo/sql/osnap_legacy/security_levels.csv','r') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		whole = ''
		count = 0
		for row in reader:
			if count > 0:
				for i in row:
					whole += i
					whole += " "
				new_row = whole.split(',')
				security_levels_data.append(new_row)
				whole = ''
			count+=1
	with open('/home/osnapdev/repo/sql/osnap_legacy/transit.csv','r') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
		whole = ''
		count = 0
		for row in reader:
			if count > 0:
				for i in row:
					whole += i
					whole += " "
				new_row = whole.split(',')
				transit_data.append(new_row)
				whole = ''
			count+=1
	with open('/home/osnapdev/repo/sql/osnap_legacy/vendors.csv','r') as csvfile:
			reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			whole = ''
			count = 0
			for row in reader:
				if count > 0:
					for i in row:
						whole += i
						whole += " "
					new_row = whole.split(',')
					vendor_data.append(new_row)
					whole = ''
				count+=1

	return





#products()
open_files()
print(convoy_data,vendor_data, product_list_data)

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