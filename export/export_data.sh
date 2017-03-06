

if [ "$#" -ne 1 ]; then
    echo "Usage: ./export_data.sh <database> <output dir>"
    exit;
fi


#psql $1 -f create_tables.sql?
psql $1

#add directory destination into below
#del dir if it exists, makdir if it doesn't
Copy (SELECT * FROM Login_info) To '/tmp/users.csv' With CSV DELIMITER ',';
Copy (SELECT * FROM facilities) To '/tmp/facilities.csv' With CSV DELIMITER ',';
Copy (SELECT * FROM Assets) To '/tmp/assets.csv' With CSV DELIMITER ',';
Copy (SELECT * FROM request) To '/tmp/transfers.csv' With CSV DELIMITER ',';
