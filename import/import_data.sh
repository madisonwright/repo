

if [ "$#" -ne 2 ]; then
    echo "Usage: ./import_data.sh <database> <input dir>"
    exit;
fi

chmod a+x import_data.py
./import_data.py $1 $2


