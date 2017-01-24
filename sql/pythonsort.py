import psycopg2
import sys
import csv


conn = psycopg2.connect(dbname=sys.argv[1],host=host='127.0.0.1',port=int(sys.argv[2]))
cur = conn.cursor()


def make_products():
	with open('/home/osnapdev/repo/sql/osnap_legacy/product_list.csv','r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	    for row in spamreader:
	    	print(row)
			#cur.execute("INSERT INTO roles (rolename) VALUES (%s)",(role,))
			#cur.execute("SELECT role_pk FROM roles WHERE rolename=%s",(role,))


		#reader = csv.DictReader(csvfile)
		#for row in reader:
			
		#	name = row['name']
		#	print(name)
		#	unit_price = row['unit price']
		#	print(unit_price)
		#	cur.execute("INSERT INTO roles (rolename) VALUES (%s)",(role,))
		#	cur.execute("SELECT role_pk FROM roles WHERE rolename=%s",(role,))
		#	roles[role] = cur.fetchone()[0]


	return


#	conn.commit()
#	cur.close()
#	conn.clow()
