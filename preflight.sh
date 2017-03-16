#! /usr/bin/bash

# This script handles the setup that must occur prior to running LOST
# Specifically this script:
#    1. creates the database
#    2. imports the legacy data
#    3. copies the required source to $HOME/wsgi

if [ "$#" -ne 1 ]; then
    echo "Usage: ./preflight.sh <database>"
    exit;
fi

# Database prep
cd sql
psql $1 -f create_tables.sql


#Download class csv files for import_data.sh
curl -O https://classes.cs.uoregon.edu//17W/cis322/files/lost_data.tar.gz
tar -xzf lost_data.tar.gz
cd ..
##lines to import data with import_data.sh
#cd import
#./import_data.sh lost $HOME/repo/sql


# Install the wsgi files
cp -R src/* $HOME/wsgi

