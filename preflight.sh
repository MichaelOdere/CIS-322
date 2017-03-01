#! /usr/bin/bash

### Usage: bash ./preflight.sh lost
### This script is called after postgres server is running and db is created
### in order to:
###     1) Create tables needed by DB
###     2) Load data into db
###     3) Load mod_wsgi

### Check arguements
if [ "$#" -ne 1 ]; then
        echo "Usage: bash ./preflight.sh <dbname>"
        exit;
fi

# Create tables in db
psql $1 -f sql/create_tables.sql

# Install the wsgi files
cp -R src/* $HOME/wsgi

