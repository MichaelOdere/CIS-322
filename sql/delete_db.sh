#bin/bash

#pg_ctl -D /home/osnapdev/data/ -l logfile stop
#pg_ctl -D /home/osnapdev/data/ -l logfile start
#sleep 1s 
echo "deleting old  db..."
dropdb lost_db
echo "creating new db..."
createdb lost_db
psql -d lost_db -a -f create_tables.sql
#python product_insert.py lost_db 5432
#psql lost_db
