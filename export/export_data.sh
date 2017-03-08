

if [ "$#" -ne 2 ]; then
    echo "Usage: ./export_data.sh <database> <output dir>"
    exit;
fi


#delete directory if it's there then make a new one
rm -rf $2
mkdir $2

#the current path you are in, so it will save to wherever you are
ourpath="$(pwd)"
psql $1 -c "Copy (SELECT * FROM Login_info) To '$ourpath/users.csv' With CSV DELIMITER ',';"
psql $1 -c "Copy (SELECT * FROM facilities) To '$ourpath/facilities.csv' With CSV DELIMITER ',';"
psql $1 -c "Copy (SELECT * FROM Assets) To '$ourpath/assets.csv' With CSV DELIMITER ',';"
psql $1 -c "Copy (SELECT * FROM request) To '$ourpath/transfers.csv' With CSV DELIMITER ',';"

#copy the files to the destination
cp users.csv $2
cp assets.csv $2
cp facilities.csv $2
cp transfers.csv $2
cp test.sh $2

#clean the current workspace
rm users.csv
rm assets.csv
rm facilities.csv
rm transfers.csv

#go to the export folder of the git repo you just pulled down, copy py file to the destination too
cd $HOME/repo/export
cp organize_data.py $2

#go to the destination and sort the csv files into proper format
cd $2
chmod a+x organize_data.py
./organize_data.py $2


